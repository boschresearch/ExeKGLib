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
from exe_kg_lib.classes.method import Method
from exe_kg_lib.classes.task import Task
from exe_kg_lib.utils.kg_creation_utils import (
    add_and_attach_data_entity, add_data_entity_instance,
    add_instance_from_parent_with_relation, add_literal, create_pipeline_task,
    deserialize_input_entity_info_dict, field_value_to_literal, save_exe_kg)
from exe_kg_lib.utils.kg_validation_utils import check_kg_executability
from exe_kg_lib.utils.query_utils import (NoResultsError,
                                          get_grouped_inherited_inputs,
                                          get_grouped_inherited_outputs,
                                          get_method_grouped_params,
                                          query_method_properties_and_methods)
from exe_kg_lib.utils.string_utils import (get_instance_name,
                                           get_task_output_name)


class ExeKGConstructionMixin:
    # see exe_kg_lib/classes/exe_kg_base.py for the definition of these attributes
    exe_kg: Graph
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
            self.exe_kg,
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

    def create_method(self, method_type: str, params_dict: Dict[str, Union[str, int, float, dict]]) -> Method:
        """
        Creates a Method object with the specified method type and parameters.

        Args:
            method_type (str): The type of the method.
            params_dict (Dict[str, Union[str, int, float, dict]]): A dictionary containing the parameters for the method.

        Returns:
            Method: The created Method object.
        """
        return Method(
            self.top_level_schema.namespace + method_type,
            self.atomic_method,
            module_chain=None,
            params_dict=params_dict,
        )

    def _add_and_link_method(
        self,
        method_type: str,
        method_params_dict: Dict[str, Union[str, int, float, dict]],
        relation_iri: str,
        task_instance: Task,
        namespace_to_use: Namespace,
        method_extra_parent_iri: str = None,
    ) -> None:
        """
        Adds a method instance to the ExeKG and links it to the task instance.

        Args:
            method_type (str): The type of the method.
            method_params_dict (Dict[str, Union[str, int, float, dict]]): A dictionary containing the method parameters.
            relation_iri (str): The IRI of the relation between the method instance and the task instance.
            task_instance (Task): The task instance to link the method instance to.
            namespace_to_use (Namespace): The namespace to use for creating the method instance.
            method_extra_parent_iri (str, optional): The IRI of an additional parent for the method instance. Defaults to None.

        Returns:
            None

        Raises:
            ValueError: If any of the provided method parameters could not be added to the method instance.
        """
        method_parent = Entity(namespace_to_use + method_type, self.atomic_method)
        method_instance = add_instance_from_parent_with_relation(
            namespace_to_use,
            self.exe_kg,
            method_parent,
            relation_iri,
            task_instance,
            self.name_instance(method_parent),
            method_extra_parent_iri,
        )

        # fetch compatible data properties from KG schema
        property_list = get_method_grouped_params(
            method_parent.iri,
            self.top_level_schema.namespace_prefix,
            self.input_kg,
            inherited=method_parent.namespace == str(self.bottom_level_schemata["visu"].namespace),
        )

        method_params_dict_copy = method_params_dict.copy()
        # add data properties to the task with given values
        for property_iri, _ in property_list:
            property_name = property_iri.split("#")[1]
            # param_name = property_name_to_field_name(property_name)
            if property_name not in method_params_dict_copy:
                continue

            input_value = method_params_dict_copy.pop(property_name)
            literal = field_value_to_literal(input_value)

            add_literal(self.exe_kg, method_instance, property_iri, literal)

        if len(method_params_dict_copy) > 0:
            raise ValueError(
                f"Provided method parameters {method_params_dict_copy} could NOT be added to the method instance."
            )

    def add_task(
        self,
        kg_schema_short: str,
        input_entity_dict: Dict[str, Union[List[DataEntity], Method]],
        method_params_dict: Dict[str, Union[str, int, float, dict]],
        task_type: str,
        method_type: str,
    ) -> Task:
        """
        Instantiates and adds a new task entity to the output KG.
        Components attached to the task during creation: input and output data entities, and a method with properties.

        Args:
            kg_schema_short (str): The short name of the KG schema to use (e.g. ml, visu, etc.).
            input_entity_dict (Dict[str, Union[List[DataEntity], Method]]): A dictionary containing input data entities for the task.
            method_params_dict (Dict[str, Union[str, int, float, dict]]): A dictionary containing method parameters.
            task_type (str): The type of the task. Defaults to None.
            method_type (str): The type of the method. Defaults to None.

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
        task_class = Task(kg_schema_to_use.namespace + task_type, self.atomic_task)
        added_entity = add_instance_from_parent_with_relation(
            kg_schema_to_use.namespace,
            self.exe_kg,
            task_class,
            relation_iri,
            self.last_created_task,
            self.name_instance(task_class),
        )
        task_instance = Task.from_entity(added_entity)  # create Task object from Entity object

        # instantiate and add given input data entities to the task
        self._add_inputs_to_task(kg_schema_to_use.namespace, task_instance, input_entity_dict)
        # instantiate and add output data entities to the task, as specified in the KG schema
        output_names = self._add_outputs_to_task(task_instance, method_type)

        # if no method is given, return the task without adding a method
        if method_type is None:
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
            filter(lambda pair: pair[1].split("#")[1] == method_type, results), None
        )  # match given method_type with query result

        if chosen_property_method is None:
            raise NoResultsError(
                f"Property connecting task of type {task_type} with method of type {method_type} not found"
            )

        # instantiate method and link it with the task using the appropriate chosen_property_method[0] relation
        self._add_and_link_method(
            method_type, method_params_dict, chosen_property_method[0], task_instance, kg_schema_to_use.namespace
        )

        self.last_created_task = task_instance  # store created task

        # add task to the serializable simplified pipeline
        self.pipeline_serializable.add_task(
            kg_schema_short,
            task_type,
            method_type,
            method_params_dict,
            input_entity_dict,
            output_names,
        )

        return task_instance

    def _add_inputs_to_task(
        self,
        namespace: Namespace,
        task_instance: Task,
        input_entity_dict: Dict[str, Union[List[DataEntity], Method]],
    ) -> None:
        """
        Instantiates and adds given input data entities to the given task of the output KG.

        Args:
            namespace (Namespace): The namespace of the task instance.
            task_instance (Task): The task instance to add inputs to.
            input_entity_dict (Dict[str, Union[List[DataEntity], Method]]): A dictionary mapping input entity names to a list of DataEntity instances.
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
            input_data_structure_iris = [pair[0] for pair in info_l]
            input_entity_name = input_entity_iri.split("#")[1]

            if input_entity_name not in input_entity_dict:
                continue
            input_entity_value = input_entity_dict[input_entity_name]
            if isinstance(input_entity_value, Method):  # provided input is a method
                if all(iri is None for iri in input_data_structure_iris):
                    raise ValueError(f"Expecting a DataEntity, but got a Method for {input_entity_name}.")

                method = input_entity_value
                # instantiate and link method to the task
                self._add_and_link_method(
                    method.name,
                    method.params_dict,
                    input_property_iri,
                    task_instance,
                    task_instance.namespace,
                    method_extra_parent_iri=input_entity_iri,
                )
            elif isinstance(input_entity_value, list) and all(
                isinstance(elem, DataEntity) for elem in input_entity_value
            ):  # provided input is list of data entities
                self._add_input_data_entities_to_task(
                    input_entity_iri, input_entity_value, input_property_iri, task_instance
                )
            else:
                raise ValueError(
                    f"Expecting a DataEntity or a Method for {input_entity_name}, but got {type(input_entity_value)}."
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
                self.exe_kg,
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
                self.exe_kg,
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
                    self.exe_kg,
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

    def save_created_kg(self, dir_path: str, check_executability=True) -> None:
        """
        Save the created ExeKG and simplified pipeline.

        Args:
            dir_path (str): The directory path where the files will be saved.
        """

        save_exe_kg(
            self.exe_kg,
            self.input_kg,
            self.shacl_shapes_s,
            self.pipeline_serializable,
            dir_path,
            self.pipeline_serializable.name,
            check_executability,
        )

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

        if parent_entity.name not in entity_type_dict:
            raise ValueError(f"Parent entity name {parent_entity.name} not found in entity type dictionary.")

        instance_name = get_instance_name(
            parent_entity.name, entity_type_dict[parent_entity.name], self.pipeline_serializable.name
        )
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
            input_entity_dict = deserialize_input_entity_info_dict(
                task.input_entity_info_dict,
                data_entities_dict,
                task_output_dicts,
                pipeline_serializable.name,
                self.bottom_level_schemata[task.kg_schema_short].namespace,
            )
            # add task to the KG
            added_task = self.add_task(
                kg_schema_short=task.kg_schema_short,
                task_type=task.task_type,
                method_type=task.method_type,
                method_params_dict=task.method_params_dict,
                input_entity_dict=input_entity_dict,
            )
            pos = pos_per_task_type.get(task.task_type, 1)
            # store output data entities of the added task
            task_output_dicts[
                get_instance_name(task.task_type, pos, self.pipeline_serializable.name)
            ] = added_task.output_dict

            pos_per_task_type[task.task_type] = pos + 1

        check_kg_executability(self.exe_kg + self.input_kg, self.shacl_shapes_s)

        return self.exe_kg

    def clear_created_kg(self) -> None:
        """
        Clears the created ExeKG.
        """
        self.exe_kg = Graph(bind_namespaces="rdflib")
        self.exe_kg.bind(self.top_level_schema.namespace_prefix, self.top_level_schema.namespace)
        for bottom_level_kg_schema in self.bottom_level_schemata.values():
            self.exe_kg.bind(
                bottom_level_kg_schema.namespace_prefix,
                bottom_level_kg_schema.namespace,
            )

        self.pipeline_serializable = Pipeline()
        self.pipeline_instance = None

        self.existing_data_entity_list = []
        self.last_created_task = None
        self.canvas_task_created = False

        for task_type in self.task_type_dict:
            self.task_type_dict[task_type] = 1

        for method_type in self.method_type_dict:
            self.method_type_dict[method_type] = 1
