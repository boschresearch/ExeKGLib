# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

import ast
import itertools
import os
import pickle
from io import TextIOWrapper
from pathlib import Path
from typing import Callable, Dict, Union

import pandas as pd
from rdflib import XSD, Graph, Literal, URIRef

from exe_kg_lib.classes.data_entity import DataEntity
from exe_kg_lib.classes.entity import Entity
from exe_kg_lib.classes.exe_kg_mixins.exe_kg_construction_mixin import \
    ExeKGConstructionMixin
from exe_kg_lib.classes.kg_schema import KGSchema
from exe_kg_lib.classes.method import Method
from exe_kg_lib.classes.task import Task
from exe_kg_lib.classes.tasks import ml_tasks, statistic_tasks, visual_tasks
from exe_kg_lib.utils.kg_creation_utils import load_exe_kg, save_exe_kg
from exe_kg_lib.utils.kg_edit_utils import update_metric_values
from exe_kg_lib.utils.kg_validation_utils import check_kg_executability
from exe_kg_lib.utils.query_utils import (NoResultsError,
                                          get_converted_module_hierarchy_chain,
                                          get_first_query_result_if_exists,
                                          get_method_by_task_iri,
                                          get_pipeline_and_first_task_iri,
                                          query_data_entity_reference_iri,
                                          query_input_triples,
                                          query_instance_parent_iri,
                                          query_method_params,
                                          query_output_triples,
                                          query_parameters_triples,
                                          query_top_level_task_iri)
from exe_kg_lib.utils.string_utils import property_iri_to_field_name


class ExeKGExecutionMixin:
    # see exe_kg_lib/classes/exe_kg_base.py for the definition of these attributes
    input_kg: Graph
    exe_kg: Graph
    top_level_schema: KGSchema
    bottom_level_schemata: Dict[str, KGSchema]
    shacl_shapes_s: str
    # see exe_kg_lib/classes/exe_kg_mixins/exe_kg_construction_mixin.py for the definition of this attribute
    create_exe_kg_from_json: Callable[[ExeKGConstructionMixin, Union[Path, TextIOWrapper, str]], Graph]

    def _property_value_to_field_value(self, property_value: Union[str, Literal]) -> Union[str, DataEntity, Method]:
        """
        Converts a property value (from the KG) to a Python field value.

        Args:
            property_value (Union[str, Literal]): The property value to be converted.

        Returns:
            Union[str, DataEntity, Method]: The converted field value.

        Raises:
            NoResultsError: If the extra parent entity that is not a subclass of AtomicMethod cannot be retrieved.
        """
        if isinstance(property_value, Literal):
            return self._literal_to_field_value(property_value)

        property_value_s = str(property_value)

        # fetch type of entity with given IRI, assuming it's a DataEntity instance
        query_result = get_first_query_result_if_exists(
            query_instance_parent_iri,
            self.input_kg,
            property_value_s,
            self.top_level_schema.namespace.DataEntity,
        )
        if query_result is not None:
            data_entity_parent_iri = str(query_result[0])
            return self._parse_data_entity_by_iri(property_value_s, data_entity_parent_iri)

        # fetch type of entity with given IRI, assuming it's an AtomicMethod instance
        query_result = get_first_query_result_if_exists(
            query_instance_parent_iri,
            self.input_kg,
            property_value_s,
            self.top_level_schema.namespace.AtomicMethod,
        )

        if query_result is None:
            return property_value_s

        method_parent_iri = str(query_result[0])

        # fetch another type associated with the entity identified by the given IRI
        query_result = get_first_query_result_if_exists(
            query_instance_parent_iri,
            self.input_kg,
            property_value_s,
            self.top_level_schema.namespace.AtomicMethod,
            True,  # negation of inheritance, so the parent that does not inherit AtomicMethod is returned
        )
        method_extra_parent_iri = str(query_result[0]) if query_result is not None else None
        if method_extra_parent_iri is None:
            raise NoResultsError(
                f"For method with iri {property_value_s}, cannot retrieve extra parent entity that is not a subclass of AtomicMethod"
            )

        # NOTE: here we use the method_extra_parent_iri as the parent entity of the method
        #       this is important for correctly parsing each task's inputs during pipeline execution (see get_inputs() in Task class)
        method = Method(property_value_s, Entity(method_extra_parent_iri))

        method.module_chain = get_converted_module_hierarchy_chain(
            self.input_kg, self.top_level_schema.namespace_prefix, method_parent_iri
        )

        # triples for the parameters attached to the method of this task
        method_related_triples = list(
            query_parameters_triples(self.input_kg, self.top_level_schema.namespace_prefix, method.iri)
        )
        for s, p, o in method_related_triples:
            # parse property IRI and value
            field_name = property_iri_to_field_name(str(p))
            field_value = self._property_value_to_field_value(o)

            method.params_dict[field_name] = field_value

        return method

    def _literal_to_field_value(self, literal: Literal) -> Union[str, int, float, bool]:
        """
        Converts a Literal object to a Python object based on its datatype.

        Args:
            literal (Literal): The Literal object to be converted.

        Returns:
            Union[str, int, float, bool]: The converted Python object.

        Raises:
            ValueError: If the datatype of the literal is unsupported.
        """
        if literal.datatype == XSD.string:
            try:
                # try to convert string to Python object e.g. dict
                return ast.literal_eval(str(literal))
            except (ValueError, SyntaxError):
                # if conversion fails, return string
                return str(literal)
        elif literal.datatype == XSD.int:
            return int(literal)
        elif literal.datatype == XSD.float:
            return float(literal)
        elif literal.datatype == XSD.boolean:
            return bool(literal)

        raise ValueError(f"Unsupported datatype for literal: {literal}")

    def _parse_data_entity_by_iri(self, data_entity_instance_iri: str, data_entity_parent_iri: str) -> DataEntity:
        """
        Parses a data entity and stores the info in a DataEntity object.

        Args:
            data_entity_instance_iri (str): The IRI of the data entity instance to be parsed.
            data_entity_parent_iri (str): The IRI of the parent entity of the data entity.

        Returns:
            DataEntity: The parsed DataEntity object.
        """
        # fetch IRI of data entity that is referenced by the given entity
        query_result = get_first_query_result_if_exists(
            query_data_entity_reference_iri,
            self.input_kg,
            self.top_level_schema.namespace_prefix,
            data_entity_instance_iri,
        )

        if query_result is None:  # no referenced data entity found
            data_entity_ref_iri = data_entity_instance_iri
        else:
            data_entity_ref_iri = str(query_result[0])

        # create DataEntity object to store all the parsed properties
        data_entity = DataEntity(data_entity_instance_iri, Entity(data_entity_parent_iri))
        data_entity.reference = data_entity_ref_iri.split("#")[1]

        for s, p, o in self.input_kg.triples((URIRef(data_entity_ref_iri), None, None)):
            # parse property name and value
            field_name = property_iri_to_field_name(str(p))
            if not hasattr(data_entity, field_name) or field_name == "type":
                continue
            field_value = self._property_value_to_field_value(str(o))
            setattr(data_entity, field_name, field_value)  # set field value dynamically

        return data_entity

    def _parse_method_of_task(self, task_iri: str) -> Method:
        """
        Parses the method associated with a given task IRI.

        Args:
            task_iri (str): The IRI of the task.

        Returns:
            Method: The parsed method object.
        """
        method = get_method_by_task_iri(
            self.input_kg,
            self.top_level_schema.namespace_prefix,
            self.top_level_schema.namespace,
            task_iri,
        )

        method.module_chain = get_converted_module_hierarchy_chain(
            self.input_kg, self.top_level_schema.namespace_prefix, method.parent_entity.iri
        )

        return method

    def _parse_task_by_iri(
        self, task_iri: str, plots_output_dir: str, canvas_task: visual_tasks.CanvasCreation = None
    ) -> Task:
        """
        Parses a task and stores the info in an object of a sub-class of Task.
        The sub-class name and the object's fields are mapped dynamically based on the found KG components.

        Args:
            task_iri (str): The IRI of the task to be parsed.
            plots_output_dir (str): The directory where plots will be saved.
            canvas_task (visual_tasks.CanvasCreation, optional): The canvas task associated with the task, if applicable.

        Returns:
            Task: The parsed Task object.

        Raises:
            NoResultsError: If the given IRI does not belong to an instance of a sub-class of self.top_level_schema.namespace.AtomicTask.
        """
        # fetch type of entity with given IRI
        query_result = get_first_query_result_if_exists(
            query_instance_parent_iri,
            self.input_kg,
            task_iri,
            self.top_level_schema.namespace.AtomicTask,
        )

        if (
            query_result is None
        ):  # given IRI does not belong to an instance of a sub-class of self.top_level_schema.namespace.AtomicTask
            raise NoResultsError(f"Cannot retrieve parent of task with iri {task_iri}")

        task_parent_iri = str(query_result[0])

        query_result = get_first_query_result_if_exists(
            query_top_level_task_iri,
            self.input_kg,
            task_parent_iri,
            self.top_level_schema.namespace_prefix,
        )

        if (
            query_result is None
        ):  # given IRI does not belong to an instance of a sub-class of self.top_level_schema.namespace.AtomicTask
            task_top_level_parent_iri = task_parent_iri
        else:
            task_top_level_parent_iri = str(query_result[0])

        task_top_level_parent = Entity(task_top_level_parent_iri, None)

        # perform automatic mapping of KG task class to Python sub-class
        class_name = task_top_level_parent.name

        is_visu_task = True
        Class = getattr(visual_tasks, class_name, None)
        if Class is None:
            is_visu_task = False
            Class = getattr(statistic_tasks, class_name, None)
        if Class is None:
            is_visu_task = False
            Class = getattr(ml_tasks, class_name, None)

        # create Task sub-class object
        if is_visu_task and canvas_task:
            task = Class(task_iri, Task(task_parent_iri), plots_output_dir, canvas_task)
        else:
            task = Class(task_iri, Task(task_parent_iri))

        # fetch method of the task and store it in the task object
        method = self._parse_method_of_task(task_iri)
        task.method = method

        # input triples
        task_related_triples = list(
            query_input_triples(self.input_kg, self.top_level_schema.namespace_prefix, task_iri)
        )
        # output triples
        task_related_triples += list(
            query_output_triples(self.input_kg, self.top_level_schema.namespace_prefix, task_iri)
        )
        # triple connecting this task with the next one in the pipeline
        task_related_triples += list(
            self.input_kg.triples((URIRef(task_iri), self.top_level_schema.namespace.hasNextTask, None))
        )
        # triples for the parameters attached to the method of this task
        method_related_triples = (
            list(query_parameters_triples(self.input_kg, self.top_level_schema.namespace_prefix, method.iri))
            if method is not None
            else []
        )

        # data properties attached to the method's class
        method_class_data_properties = list(
            query_method_params(method.parent_entity.iri, self.top_level_schema.namespace_prefix, self.input_kg)
        )
        method_class_data_property_iris = None
        if method_class_data_properties:
            method_class_data_property_iris = [str(pair[0]) for pair in method_class_data_properties]
        for s, p, o in itertools.chain(task_related_triples, method_related_triples):
            # parse property IRI and value
            field_name = property_iri_to_field_name(str(p))
            field_value = self._property_value_to_field_value(o)
            # set field value dynamically
            if field_name.endswith("input"):
                getattr(task, "inputs").append(field_value)
            elif field_name.endswith("output"):
                getattr(task, "outputs").append(field_value)
            elif field_name == "next_task":
                setattr(task, field_name, field_value)
            else:  # method parameter
                # separate method class data properties from inherited ones
                if method_class_data_property_iris and str(p) in method_class_data_property_iris:
                    task.method.params_dict[field_name] = field_value
                else:
                    task.method.inherited_params_dict[field_name] = field_value

        return task

    def execute_pipeline(self, input_exe_kg_path: str) -> None:
        """
        Executes the pipeline by parsing the input ExeKG task-by-task.

        Args:
            input_exe_kg_path (str): The path to the input ExeKG file.

        Raises:
            ValueError: If the input data file format is not supported.

        Returns:
            None
        """
        self.exe_kg = load_exe_kg(
            input_exe_kg_path, self.create_exe_kg_from_json if input_exe_kg_path.endswith(".json") else None
        )

        self.input_kg += self.exe_kg
        check_kg_executability(self.input_kg, self.shacl_shapes_s)

        pipeline_iri, input_data_path, plots_output_dir, next_task_iri = get_pipeline_and_first_task_iri(
            self.input_kg, self.top_level_schema.namespace_prefix
        )
        if input_data_path.endswith(".csv"):
            input_data = pd.read_csv(input_data_path, delimiter=",", encoding="ISO-8859-1")
        elif input_data_path.endswith(".pq") or input_data_path.endswith(".parquet"):
            input_data = pd.read_parquet(input_data_path)
        else:
            raise ValueError(f"Unsupported file format for input data: {input_data_path}")

        canvas_task = None  # stores Task object that corresponds to a task of type CanvasTask
        task_output_dict = {}  # gradually filled with outputs of executed tasks
        while next_task_iri is not None:
            try:
                next_task = self._parse_task_by_iri(next_task_iri, plots_output_dir, canvas_task)
            except NoResultsError as e:
                raise RuntimeError(f"{e}\n\nParsing of task with IRI {next_task_iri} failed with the above exception")

            try:
                output = next_task.run_method(task_output_dict, input_data)
            except NotImplementedError as e:
                raise RuntimeError(
                    f"{e}\n\nExecution of method for task {next_task_iri} failed with the above exception"
                )

            if output:
                task_output_dict.update(output)

            if next_task.type == "CanvasCreation":
                canvas_task = next_task

            next_task_iri = next_task.next_task

        update_metric_values(
            self.exe_kg,
            task_output_dict,
            self.bottom_level_schemata["ml"].namespace,
            self.top_level_schema.namespace,
        )

        save_exe_kg(
            self.exe_kg,
            self.input_kg,
            self.shacl_shapes_s,
            None,
            os.path.dirname(input_exe_kg_path),
            pipeline_iri.split("#")[-1],
            check_executability=False,
            save_to_json=False,
        )
