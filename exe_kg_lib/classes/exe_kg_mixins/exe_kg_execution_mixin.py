# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

import itertools
from typing import Optional, Union

import pandas as pd
from rdflib import XSD, Graph, Literal, URIRef

from exe_kg_lib.classes.data_entity import DataEntity
from exe_kg_lib.classes.entity import Entity
from exe_kg_lib.classes.kg_schema import KGSchema
from exe_kg_lib.classes.task import Task
from exe_kg_lib.classes.tasks import ml_tasks, statistic_tasks, visual_tasks
from exe_kg_lib.utils.kg_validation_utils import check_kg_executability
from exe_kg_lib.utils.query_utils import (NoResultsError,
                                          get_first_query_result_if_exists,
                                          get_method_by_task_iri,
                                          get_module_hierarchy_chain,
                                          get_pipeline_and_first_task_iri,
                                          query_data_entity_reference_iri,
                                          query_input_triples,
                                          query_instance_parent_iri,
                                          query_method_params,
                                          query_output_triples,
                                          query_parameters_triples,
                                          query_top_level_task_iri)
from exe_kg_lib.utils.string_utils import (class_name_to_method_name,
                                           class_name_to_module_name,
                                           property_iri_to_field_name)


class ExeKGExecutionMixin:
    input_kg: Graph
    top_level_schema: KGSchema
    shacl_shapes_s: str

    def _property_value_to_field_value(self, property_value: Union[str, Literal]) -> Union[str, DataEntity]:
        """
        Converts a KG property value to a Python field value.

        Args:
            property_value (Union[str, Literal]): The property value to be converted.

        Returns:
            Union[str, DataEntity]: The converted field value.

        """
        property_value_s = str(property_value)
        if "#" in property_value_s:
            try:
                return self._parse_data_entity_by_iri(property_value_s)
            except NoResultsError:  # property_value_s isn't an IRI of a DataEntity instance
                if not isinstance(property_value, Literal):
                    return property_value
                return self._literal_to_field_value(property_value)

        if not isinstance(property_value, Literal):
            return property_value
        return self._literal_to_field_value(property_value)

    def _literal_to_field_value(self, literal: Literal) -> Union[str, int, float, bool]:
        """
        Converts a Literal object to a Python field value of the appropriate type.

        Args:
            literal (Literal): The Literal object to be converted.

        Returns:
            Union[str, int, float, bool]: The converted field value.

        """
        if literal.datatype == XSD.string:
            return str(literal)
        elif literal.datatype == XSD.integer:
            return int(literal)
        elif literal.datatype == XSD.float:
            return float(literal)
        elif literal.datatype == XSD.boolean:
            return bool(literal)
        else:
            return literal

    def _parse_data_entity_by_iri(self, in_out_data_entity_iri: str) -> DataEntity:
        """
        Parses an input or output data entity and stores the parsed info in a Python object.

        Args:
            in_out_data_entity_iri (str): The IRI of the data entity to parse.

        Returns:
            DataEntity: The parsed DataEntity object.

        Raises:
            NoResultsError: If the given IRI doesn't belong to an instance of a subclass of DataEntity.
        """
        # fetch type of entity with given IRI
        query_result = get_first_query_result_if_exists(
            query_instance_parent_iri,
            self.input_kg,
            in_out_data_entity_iri,
            self.top_level_schema.namespace.DataEntity,
        )
        if query_result is None:
            raise NoResultsError(
                f"Given IRI {in_out_data_entity_iri} doesn't belong to an instance of a subclass of {str(self.top_level_schema.namespace.DataEntity)}"
            )

        data_entity_parent_iri = str(query_result[0])

        # fetch IRI of data entity that is referenced by the given entity
        query_result = get_first_query_result_if_exists(
            query_data_entity_reference_iri,
            self.input_kg,
            self.top_level_schema.namespace_prefix,
            in_out_data_entity_iri,
        )

        if query_result is None:  # no referenced data entity found
            data_entity_ref_iri = in_out_data_entity_iri
        else:
            data_entity_ref_iri = str(query_result[0])

        # create DataEntity object to store all the parsed properties
        data_entity = DataEntity(in_out_data_entity_iri, Entity(data_entity_parent_iri))
        data_entity.reference = data_entity_ref_iri.split("#")[1]

        for s, p, o in self.input_kg.triples((URIRef(data_entity_ref_iri), None, None)):
            # parse property name and value
            field_name = property_iri_to_field_name(str(p))
            if not hasattr(data_entity, field_name) or field_name == "type":
                continue
            field_value = self._property_value_to_field_value(str(o))
            setattr(data_entity, field_name, field_value)  # set field value dynamically

        return data_entity

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

        method = get_method_by_task_iri(
            self.input_kg,
            self.top_level_schema.namespace_prefix,
            self.top_level_schema.namespace,
            task_iri,
        )
        # if method is None:
        #     print(f"Cannot retrieve method for task with iri: {task_iri}")

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

        module_chain_names = None
        try:
            module_chain_names = get_module_hierarchy_chain(
                self.input_kg, self.top_level_schema.namespace_prefix, method.parent_entity.iri
            )
        except NoResultsError:
            print(
                f"Cannot retrieve module chain for method class: {method.parent_entity.iri}. Proceeding without it..."
            )

        if module_chain_names:
            # convert KG class names to module names and reverse the module chain to store it in the correct order
            module_chain_names = [class_name_to_module_name(name) for name in module_chain_names]
            module_chain_names = [class_name_to_method_name(method.type)] + module_chain_names
            module_chain_names.reverse()
            task.method_module_chain = module_chain_names

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
                    task.method_params_dict[field_name] = field_value
                else:
                    task.method_inherited_params_dict[field_name] = field_value

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
        input_exe_kg = Graph(bind_namespaces="rdflib")
        input_exe_kg.parse(input_exe_kg_path, format="n3")  # parse input executable KG

        self.input_kg += input_exe_kg
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
                print(e)
                raise RuntimeError(f"Parsing of task with IRI {next_task_iri} failed with the above exception")

            try:
                output = next_task.run_method(task_output_dict, input_data)
            except NotImplementedError as e:
                print(e)
                raise RuntimeError(f"Execution of method for task {next_task_iri} failed with the above exception")

            if output:
                task_output_dict.update(output)

            if next_task.type == "CanvasCreation":
                canvas_task = next_task

            next_task_iri = next_task.next_task
