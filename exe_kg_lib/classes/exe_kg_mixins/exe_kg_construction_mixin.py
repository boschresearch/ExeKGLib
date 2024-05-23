# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

import os
from io import TextIOWrapper
from pathlib import Path
from typing import Dict, List, Union

from rdflib import XSD, Graph, Literal, Namespace

from exe_kg_lib.classes.data_entity import DataEntity
from exe_kg_lib.classes.entity import Entity
from exe_kg_lib.classes.exe_kg_serialization.pipeline import Pipeline
from exe_kg_lib.classes.kg_schema import KGSchema
from exe_kg_lib.classes.task import Task
from exe_kg_lib.utils.kg_creation_utils import (
    add_and_attach_data_entity, add_data_entity_instance,
    add_instance_from_parent_with_relation, add_literal, create_pipeline_task,
    deserialize_input_data_entity_dict)
from exe_kg_lib.utils.kg_validation_utils import check_kg_executability
from exe_kg_lib.utils.query_utils import (
    NoResultsError, get_grouped_inherited_inputs,
    get_grouped_inherited_outputs, get_method_grouped_params_plus_inherited,
    query_method_properties_and_methods)
from exe_kg_lib.utils.string_utils import (get_instance_name,
                                           get_task_output_name)


class ExeKGConstructionMixin:
    # see exe_kg_lib/classes/exe_kg_base.py for the definition of these attributes
    output_kg: Graph
    pipeline_instance: Entity
    pipeline_serializable: Pipeline
    top_level_schema: KGSchema
    bottom_level_schemata: Dict[str, KGSchema]
    atomic_task: Entity
    task: Entity
    atomic_method: Entity
    data_entity: Entity
    pipeline: Entity
    data: Entity
    data_semantics: Entity
    data_structure: Entity
    input_kg: Graph
    task_type_dict: Dict[str, int]
    method_type_dict: Dict[str, int]
    atomic_task_list: List[Entity]
    atomic_method_list: List[Entity]
    data_type_list: List[Entity]
    data_semantics_list: List[Entity]
    data_structure_list: List[Entity]
    existing_data_entity_list: List[DataEntity]
    last_created_task: Union[None, Task]
    canvas_task_created: bool
    shacl_shapes_s: str

    def create_pipeline_task(self, pipeline_name: str, input_data_path: str, plots_output_dir: str) -> Task:
        """
        Creates a pipeline task with the given parameters and adds it to the output KG.

        Args:
            pipeline_name (str): The name of the pipeline.
            input_data_path (str): The path to the input data for the pipeline.
            plots_output_dir (str): The directory to save the plots when executing the pipeline.

        Returns:
            Task: The created pipeline task.
        """
        self.pipeline_instance = create_pipeline_task(
            self.top_level_schema.namespace,
            self.pipeline,
            self.output_kg,
            pipeline_name,
            input_data_path,
            plots_output_dir,
        )
        self.last_created_task = self.pipeline_instance

        # update the serializable simplified pipeline
        self.pipeline_serializable.name = pipeline_name
        self.pipeline_serializable.input_data_path = str(input_data_path)
        self.pipeline_serializable.output_plots_dir = str(plots_output_dir)

        return self.pipeline_instance

    def create_data_entity(
        self,
        name: str,
        source_value: str,
        data_semantics_name: str,
        data_structure_name: str,
    ) -> DataEntity:
        """
        Creates a DataEntity object with the given parameters.

        Args:
            name (str): The name of the data entity.
            source_value (str): The source value of the data entity (e.g. column name from the input dataset).
            data_semantics_name (str): The name of the data semantics.
            data_structure_name (str): The name of the data structure.

        Returns:
            DataEntity: The created DataEntity object.
        """
        # add data entity to the serializable simplified pipeline
        self.pipeline_serializable.add_data_entity(name, source_value, data_semantics_name, data_structure_name)

        return DataEntity(
            self.top_level_schema.namespace + name,
            self.data_entity,
            source_value,
            self.top_level_schema.namespace + data_semantics_name,
            self.top_level_schema.namespace + data_structure_name,
        )

    def add_task(
        self,
        kg_schema_short: str,
        input_data_entity_dict: Dict[str, List[DataEntity]],
        method_params_dict: Dict[str, Union[str, int, float]],
        task: str = None,
        method: str = None,
    ) -> Task:
        """
        Instantiates and adds a new task entity to the output KG.
        Components attached to the task during creation: input and output data entities, and a method with properties.

        Args:
            kg_schema_short (str): The short name of the KG schema to use (e.g. ml, visu, etc.).
            input_data_entity_dict (Dict[str, List[DataEntity]]): A dictionary containing input data entities for the task.
            method_params_dict (Dict[str, Union[str, int, float]]): A dictionary containing method parameters.
            task (str, optional): The type of the task. Defaults to None.
            method (str, optional): The type of the method. Defaults to None.

        Returns:
            Task: The created task object.

        Raises:
            NoResultsError: If the property connecting the task and method is not found.
        """

        kg_schema_to_use = self.bottom_level_schemata[kg_schema_short]

        relation_iri = (
            self.top_level_schema.namespace.hasNextTask
            if self.last_created_task.type != "Pipeline"
            else self.top_level_schema.namespace.hasStartTask
        )  # use relation depending on the previous task

        # instantiate task and link it with the previous one
        task_class = Task(kg_schema_to_use.namespace + task, self.atomic_task)
        added_entity = add_instance_from_parent_with_relation(
            kg_schema_to_use.namespace,
            self.output_kg,
            task_class,
            relation_iri,
            self.last_created_task,
            self.name_instance(task_class),
        )
        task_instance = Task.from_entity(added_entity)  # create Task object from Entity object

        # instantiate and add given input data entities to the task
        self._add_inputs_to_task(kg_schema_to_use.namespace, task_instance, input_data_entity_dict)
        # instantiate and add output data entities to the task, as specified in the KG schema
        output_names = self._add_outputs_to_task(task_instance, method)

        # if no method is given, return the task without adding a method
        if method is None:
            self.last_created_task = task_instance  # store created task
            return task_instance

        # fetch compatible methods and their properties from KG schema
        results = list(
            query_method_properties_and_methods(
                self.input_kg,
                self.top_level_schema.namespace_prefix,
                task_instance.parent_entity.iri,
            )
        )
        chosen_property_method = next(
            filter(lambda pair: pair[1].split("#")[1] == method, results), None
        )  # match given method_type with query result

        if chosen_property_method is None:
            raise NoResultsError(f"Property connecting task of type {task} with method of type {method} not found")

        method_parent = Entity(kg_schema_to_use.namespace + method, self.atomic_method)
        # instantiate method and link it with the task using the appropriate chosen_property_method[0] relation
        method_instance = add_instance_from_parent_with_relation(
            kg_schema_to_use.namespace,
            self.output_kg,
            method_parent,
            chosen_property_method[0],
            task_instance,
            self.name_instance(method_parent),
        )

        # fetch compatible data properties from KG schema
        property_list = get_method_grouped_params_plus_inherited(
            method_parent.iri, self.top_level_schema.namespace_prefix, self.input_kg
        )
        # add data properties to the task with given values
        for property_iri, _ in property_list:
            property_name = property_iri.split("#")[1]
            # param_name = property_name_to_field_name(property_name)
            if property_name not in method_params_dict:
                continue

            input_value = method_params_dict[property_name]
            literal = self._field_value_to_literal(input_value)

            add_literal(self.output_kg, method_instance, property_iri, literal)

        self.last_created_task = task_instance  # store created task

        # add task to the serializable simplified pipeline
        self.pipeline_serializable.add_task(
            kg_schema_short,
            task,
            method,
            method_params_dict,
            input_data_entity_dict,
            output_names,
        )

        return task_instance

    def _add_inputs_to_task(
        self,
        namespace: Namespace,
        task_instance: Task,
        input_data_entity_dict: Dict[str, List[DataEntity]],
    ) -> None:
        """
        Instantiates and adds given input data entities to the given task of the output KG.

        Args:
            namespace (Namespace): The namespace of the task instance.
            task_instance (Task): The task instance to add inputs to.
            input_data_entity_dict (Dict[str, List[DataEntity]], optional): A dictionary mapping input entity names to a list of DataEntity instances.
        """

        results = list(
            get_grouped_inherited_inputs(
                self.input_kg,
                self.top_level_schema.namespace_prefix,
                task_instance.parent_entity.iri,
            )
        )

        for input_entity_iri, info_l in results:
            input_property_iri = info_l[0][1]
            input_entity_list = input_data_entity_dict[input_entity_iri.split("#")[1]]

            self._add_input_data_entities_to_task(
                input_entity_iri, input_entity_list, input_property_iri, task_instance
            )

    def _add_input_data_entities_to_task(
        self,
        input_entity_iri: str,
        input_data_entity_list: List[DataEntity],
        input_property_iri: str,
        task_instance: Task,
    ) -> None:
        input_entity_name = input_entity_iri.split("#")[1]
        same_input_index = 1
        for input_data_entity in input_data_entity_list:
            # instantiate data entity corresponding to the given input_entity_name
            data_entity_iri = input_entity_iri + "_" + task_instance.name + "_" + str(same_input_index)
            # instantiate given data entity
            add_data_entity_instance(
                self.output_kg,
                self.data,
                self.top_level_schema.kg,
                self.top_level_schema.namespace,
                input_data_entity,
            )
            # instantiate and attach data entity with reference to the given data entit
            data_entity = DataEntity(
                data_entity_iri,
                DataEntity(input_entity_iri, self.data_entity),
                reference=input_data_entity.iri,
                # data_structure_iri=input_data_entity.data_structure,
            )
            add_and_attach_data_entity(
                self.output_kg,
                self.data,
                self.top_level_schema.kg,
                self.top_level_schema.namespace,
                data_entity,
                input_property_iri,
                task_instance,
            )
            task_instance.input_dict[input_entity_name] = data_entity
            same_input_index += 1

    def _add_outputs_to_task(self, task_instance: Task, method_instance_type: str) -> List[str]:
        """
        Instantiates and adds output data entities to the given task of the output KG.

        Args:
            task_instance (Task): The task instance to add outputs to.
            method_instance_type (str): The type of the method instance.
                                        If not None, it will be appended to the output data entity IRI.
                                        If None, the task type index will be appended instead.

        Returns:
            List[str]: The names of the output data entities.
        """

        # fetch compatible outputs from KG schema
        results = list(
            get_grouped_inherited_outputs(
                self.input_kg,
                self.top_level_schema.namespace_prefix,
                task_instance.parent_entity.iri,
            )
        )

        output_names = []
        for output_parent_entity_iri, info_l in results:
            data_structure_iris = [pair[0] for pair in info_l]
            output_property_iri = info_l[0][1]  # common input property for all data structures
            output_names.append(output_parent_entity_iri.split("#")[1])
            # instantiate and add data entity
            output_data_entity_iri = get_task_output_name(
                output_parent_entity_iri, task_instance.name, method_instance_type
            )

            # add and attach output data entity to the task
            # attach all compatible data structures to the data entity
            for data_structure_iri in data_structure_iris:
                output_data_entity = DataEntity(
                    output_data_entity_iri,
                    DataEntity(output_parent_entity_iri, self.data_entity),
                    data_structure_iri=data_structure_iri,
                )
                add_and_attach_data_entity(
                    self.output_kg,
                    self.data,
                    self.top_level_schema.kg,
                    self.top_level_schema.namespace,
                    output_data_entity,
                    output_property_iri,
                    task_instance,
                )
            task_instance.output_dict[output_parent_entity_iri.split("#")[1]] = output_data_entity
            self.existing_data_entity_list.append(output_data_entity)

        return output_names

    def _field_value_to_literal(self, field_value: Union[str, int, float, bool]) -> Literal:
        """
        Converts a Python field value to a Literal object with the appropriate datatype.

        Args:
            field_value (Union[str, int, float, bool]): The value to be converted.

        Returns:
            Literal: The converted Literal object.

        """
        if isinstance(field_value, str):
            return Literal(field_value, datatype=XSD.string)
        elif isinstance(field_value, int):
            return Literal(field_value, datatype=XSD.int)
        elif isinstance(field_value, float):
            return Literal(field_value, datatype=XSD.float)
        elif isinstance(field_value, bool):
            return Literal(field_value, datatype=XSD.boolean)
        else:
            return field_value

    def save_created_kg(self, dir_path: str) -> None:
        """
        Save the created ExeKG and simplified pipeline.

        Args:
            dir_path (str): The directory path where the files will be saved.
        """

        check_kg_executability(self.output_kg + self.input_kg, self.shacl_shapes_s)

        os.makedirs(dir_path, exist_ok=True)

        # save the ExeKG in RDF/Turtle format
        ttl_file_path = os.path.join(dir_path, f"{self.pipeline_instance.name}.ttl")
        self.output_kg.serialize(destination=ttl_file_path)
        print(f"Executable KG saved in RDF/Turtle format at {ttl_file_path}.")

        # save the simplified pipeline in JSON format
        json_file_path = os.path.join(dir_path, f"{self.pipeline_instance.name}.json")
        with open(json_file_path, "w+") as json_file:
            json_file.write(self.pipeline_serializable.to_json())
        print(f"Pipeline (simplified) saved in JSON format to {json_file_path}.")

    def name_instance(
        self,
        parent_entity: Entity,
    ) -> Union[None, str]:
        """
        Generates a unique name for an instance based on its given parent entity.

        Args:
            parent_entity (Entity): The parent entity for which the instance name is generated.

        Returns:
            Union[None, str]: The generated instance name.

        Raises:
            ValueError: If the parent entity type is invalid.
        """

        if parent_entity.type == "AtomicTask":
            entity_type_dict = self.task_type_dict
        elif parent_entity.type == "AtomicMethod":
            entity_type_dict = self.method_type_dict
        else:
            raise ValueError(f"Cannot create instance's name due to invalid parent entity type: {parent_entity.type}")

        instance_name = get_instance_name(parent_entity.name, entity_type_dict[parent_entity.name])
        entity_type_dict[parent_entity.name] += 1
        return instance_name

    def create_exe_kg_from_json(self, source: Union[Path, TextIOWrapper, str]) -> Graph:
        """
        Creates an ExeKG from a JSON source that represents a pipeline.

        Args:
            source (Union[Path, TextIOWrapper, str]): The JSON source containing the pipeline.

        Returns:
            Graph: The created ExeKG.
        """

        pipeline_serializable = Pipeline.from_json(source)

        # create data entities
        data_entities_dict = {}
        for data_entity in pipeline_serializable.data_entities:
            data_entities_dict[data_entity.name] = self.create_data_entity(
                data_entity.name,
                data_entity.source,
                data_entity.data_semantics,
                data_entity.data_structure,
            )

        # create pipeline task
        self.create_pipeline_task(
            pipeline_serializable.name,
            pipeline_serializable.input_data_path,
            pipeline_serializable.output_plots_dir,
        )

        # create tasks
        pos_per_task_type: Dict[str, int] = {}
        task_output_dicts: Dict[str, Dict[str, DataEntity]] = {}
        for task in pipeline_serializable.tasks:
            # replace input data entity names with DataEntity objects
            input_data_entity_dict = deserialize_input_data_entity_dict(
                task.input_data_entity_dict, data_entities_dict, task_output_dicts
            )
            # add task to the KG
            added_task = self.add_task(
                kg_schema_short=task.kg_schema_short,
                task=task.task_type,
                method=task.method_type,
                method_params_dict=task.method_params_dict,
                input_data_entity_dict=input_data_entity_dict,
            )
            pos = pos_per_task_type.get(task.task_type, 1)
            # store output data entities of the added task
            task_output_dicts[get_instance_name(task.task_type, pos)] = added_task.output_dict

            pos_per_task_type[task.task_type] = pos + 1

        check_kg_executability(self.output_kg + self.input_kg, self.shacl_shapes_s)

        return self.output_kg
