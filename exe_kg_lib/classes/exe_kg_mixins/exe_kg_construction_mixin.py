# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

import os
from typing import Callable, Dict, List, Union

from rdflib import XSD, Graph, Literal, Namespace

from exe_kg_lib.classes.data_entity import DataEntity
from exe_kg_lib.classes.entity import Entity
from exe_kg_lib.classes.kg_schema import KGSchema
from exe_kg_lib.classes.task import Task
from exe_kg_lib.utils.cli_utils import (get_input_for_existing_data_entities,
                                        get_input_for_new_data_entities)
from exe_kg_lib.utils.kg_creation_utils import (
    add_and_attach_data_entity, add_data_entity_instance,
    add_instance_from_parent_with_relation, add_literal, create_pipeline_task)
from exe_kg_lib.utils.query_utils import (
    get_grouped_data_properties_plus_inherited_by_entity_iri,
    get_grouped_inherited_inputs, get_grouped_inherited_outputs,
    get_method_properties_and_methods)


class ExeKGConstructionMixin:
    output_kg: Graph
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

    def create_pipeline_task(self, pipeline_name: str, input_data_path: str, plots_output_dir: str) -> Task:
        """
        Instantiates and adds a new pipeline task entity to self.output_kg
        Args:
            pipeline_name: name for the pipeline
            input_data_path: path for the input data to be used by the pipeline's tasks

        Returns:
            Task: created pipeline
        """
        pipeline = create_pipeline_task(
            self.top_level_schema.namespace,
            self.pipeline,
            self.output_kg,
            pipeline_name,
            input_data_path,
            plots_output_dir,
        )
        self.last_created_task = pipeline
        return pipeline

    def create_data_entity(
        self,
        name: str,
        source_value: str,
        data_semantics_name: str,
        data_structure_name: str,
    ) -> DataEntity:
        """
        Creates a DataEntity object
        Args:
            name: name of the data entity
            source_value: name of the data source corresponding to a column of the data
            data_semantics_name: name of the data semantics entity
            data_structure_name: name of the data structure entity

        Returns:
            DataEntity: object initialized with the given parameter values
        """
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
        Instantiates and adds a new task entity to self.output_kg
        Components attached to the task during creation: input and output data entities, and a method with properties
        Args:
            kg_schema_short: abbreviated name of the KG schema in which the task and method belong
            task: task name
            input_data_entity_dict: keys -> input names of the specified task
                                    values -> lists of DataEntity objects to be added as input to the task
            method: method name
            properties_dict: keys -> property names of the specified method
                             values -> values to be added as parameters to the method

        Returns:
            Task: object of the created task
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
        self._add_outputs_to_task(task_instance, method)

        # if no method is given, return the task without adding a method
        if method is None:
            self.last_created_task = task_instance  # store created taskq
            return task_instance

        # fetch compatible methods and their properties from KG schema
        results = list(
            get_method_properties_and_methods(
                self.input_kg,
                self.top_level_schema.namespace_prefix,
                task_instance.parent_entity.iri,
            )
        )
        chosen_property_method = next(
            filter(lambda pair: pair[1].split("#")[1] == method, results), None
        )  # match given method_type with query result
        # print(chosen_property_method)

        if chosen_property_method is None:
            print(f"Property connecting task of type {task} with method of type {method} not found")
            exit(1)

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
        property_list = get_grouped_data_properties_plus_inherited_by_entity_iri(method_parent.iri, self.input_kg)
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

        return task_instance

    def _add_inputs_to_task(
        self,
        namespace: Namespace,
        task_instance: Task,
        input_data_entity_dict: Dict[str, List[DataEntity]] = None,
    ) -> None:
        """
        Instantiates and adds given input data entities to the given task of self.output_kg
        if input_data_entity_dict is None, user is asked to specify input data entities
        Args:
            task_entity: the task to add the input to
            input_data_entity_dict: keys -> input entity names corresponding to the given task as defined in the chosen bottom-level KG schema
                                    values -> list of corresponding data entities to be added as input to the task
        """

        use_cli = input_data_entity_dict is None

        # fetch compatible inputs from KG schema
        results = list(
            get_grouped_inherited_inputs(
                self.input_kg,
                self.top_level_schema.namespace_prefix,
                task_instance.parent_entity.iri,
            )
        )

        # task_type_index was incremented when creating the task entity
        # reset the index to match the currently created task's index
        task_type_index = self.task_type_dict[task_instance.type] - 1
        for input_entity_iri, data_structure_iris in results:
            input_entity_name = input_entity_iri.split("#")[1]
            data_structure_names = [iri.split("#")[1] for iri in data_structure_iris]

            if not use_cli:
                input_data_entity_list = input_data_entity_dict[input_entity_name]
            else:
                # use CLI
                print(f"Specify input corresponding to {input_entity_name} with data structures {data_structure_names}")
                input_data_entity_list = get_input_for_existing_data_entities(self.existing_data_entity_list)
                input_data_entity_list += get_input_for_new_data_entities(
                    self.data_semantics_list,
                    self.data_structure_list,
                    namespace,
                    self.data_entity,
                )

            same_input_index = 1
            for input_data_entity in input_data_entity_list:
                # instantiate data entity corresponding to the found input_entity_name
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
                    self.top_level_schema.namespace.hasInput,
                    task_instance,
                )
                task_instance.input_dict[input_entity_name] = data_entity
                same_input_index += 1

                # if use_cli:
                #     check_kg_executability(self.output_kg)

    def _add_outputs_to_task(self, task_instance: Task, method_instance_type: str) -> None:
        """
        Instantiates and adds output data entities to the given task of self.output_kg, based on the task's definition in the KG schema
        Args:
            task_entity: the task to add the output to
        """
        # fetch compatible outputs from KG schema
        results = list(
            get_grouped_inherited_outputs(
                self.input_kg,
                self.top_level_schema.namespace_prefix,
                task_instance.parent_entity.iri,
            )
        )

        # task_type_index was incremented when creating the task entity
        # reset the index to match the currently created task's index
        task_type_index = self.task_type_dict[task_instance.type] - 1
        for output_parent_entity_iri, data_structure_iris in results:
            # instantiate and add data entity
            output_data_entity_iri = (
                output_parent_entity_iri + method_instance_type
                if method_instance_type is not None
                else output_parent_entity_iri + str(task_type_index)
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
                    self.top_level_schema.namespace.hasOutput,
                    task_instance,
                )
            task_instance.output_dict[output_parent_entity_iri.split("#")[1]] = output_data_entity
            self.existing_data_entity_list.append(output_data_entity)

    def _create_next_task_cli(self) -> Union[None, Task]:
        """
        Instantiates and adds task (without method) based on user input to self.output_kg
        Adds task's output data entities to self.existing_data_entity_list
        Returns:
            None: in case user wants to end the pipeline creation
            Task: object of the created task
        """
        print("Please choose the next task")
        for i, t in enumerate(self.atomic_task_list):
            if not self.canvas_task_created and t.name == "PlotTask":
                continue
            if self.canvas_task_created and t.name == "CanvasTask":
                continue
            print(f"\t{str(i)}. {t.name}")
        print(f"\t{str(-1)}. End pipeline")
        next_task_id = int(input())
        if next_task_id == -1:
            return None

        next_task_parent = self.atomic_task_list[next_task_id]
        relation_iri = (
            self.top_level_schema.namespace.hasNextTask
            if self.last_created_task.type != "Pipeline"
            else self.top_level_schema.namespace.hasStartTask
        )  # use relation depending on the previous task

        # instantiate task and link it with the previous one
        task_entity = add_instance_from_parent_with_relation(
            next_task_parent.namespace,
            self.output_kg,
            next_task_parent,
            relation_iri,
            self.last_created_task,
            self.name_instance(next_task_parent),
        )

        task_entity = Task(task_entity.iri, task_entity.parent_entity)  # create Task object from Entity object's info

        self.last_created_task = task_entity
        if task_entity.type == "CanvasTask":
            self.canvas_task_created = True

        return task_entity

    def _create_method(self, task_to_attach_to: Entity) -> None:
        """
        Instantiate and attach method to task of self.output_kg
        Args:
            task_to_attach_to: the task to attach the created method to
        """
        print(f"Please choose a method for {task_to_attach_to.type}:")

        # fetch compatible methods and their properties from KG schema
        results = list(
            get_method_properties_and_methods(
                self.input_kg,
                self.top_level_schema.namespace_prefix,
                task_to_attach_to.parent_entity.iri,
            )
        )
        for i, pair in enumerate(results):
            tmp_method = pair[1].split("#")[1]
            print(f"\t{str(i)}. {tmp_method}")

        method_id = int(input())
        selected_property_and_method = results[method_id]
        method_parent = next(
            filter(
                lambda m: m.iri == selected_property_and_method[1],
                self.atomic_method_list,
            ),
            None,
        )
        # instantiate method and link it with the task using the appropriate selected_property_and_method[0] relation
        method_instance = add_instance_from_parent_with_relation(
            task_to_attach_to.namespace,
            self.output_kg,
            method_parent,
            selected_property_and_method[0],
            task_to_attach_to,
            self.name_instance(method_parent),
        )

        # fetch compatible data properties from KG schema
        property_list = get_grouped_data_properties_plus_inherited_by_entity_iri(method_parent.iri, self.input_kg)

        if property_list:
            print(f"Please enter requested properties for {method_parent.name}:")
            # add data properties to the task with given values
            for property_iri, property_range_iris in property_list:
                property_name = property_iri.split("#")[1]
                ranges = [range_iri.split("#")[1] for range_iri in property_range_iris]

                input_value_s = input("\t{} in range({}): ".format(property_name, ", ".join(ranges)))
                if input_value_s == "":
                    continue

                try:
                    input_value = eval(input_value_s)
                except SyntaxError:
                    input_value = input_value_s

                literal = self._field_value_to_literal(input_value)
                add_literal(self.output_kg, method_instance, property_iri, literal)

        # check_kg_executability(self.output_kg)

        return method_instance

    def _field_value_to_literal(self, field_value: Union[str, int, float, bool]) -> Literal:
        """
        Converts a Python class field value to a Literal
        Args:
            field_value: field value to convert

        Returns:
            Literal: object containing the given field value
        """
        if isinstance(field_value, str):
            return Literal(field_value, datatype=XSD.string)
        elif isinstance(field_value, int):
            return Literal(field_value, datatype=XSD.integer)
        elif isinstance(field_value, float):
            return Literal(field_value, datatype=XSD.float)
        elif isinstance(field_value, bool):
            return Literal(field_value, datatype=XSD.boolean)
        else:
            return field_value

    def start_pipeline_creation(self, pipeline_name: str, input_data_path: str, input_plots_output_dir: str) -> None:
        """
        Handles the pipeline creation through CLI
        Args:
            pipeline_name: name for the pipeline
            input_data_path: path for the input data to be used by the pipeline's tasks
        """
        pipeline = create_pipeline_task(
            self.top_level_schema.namespace,
            self.pipeline,
            self.output_kg,
            pipeline_name,
            input_data_path,
            input_plots_output_dir,
        )

        self.last_created_task = pipeline

        while True:
            next_task = self._create_next_task_cli()
            if next_task is None:
                break

            method_instance = self._create_method(next_task)

            # instantiate and add input data entities to the task based on user input
            self._add_inputs_to_task(next_task.parent_entity.namespace, next_task)
            # instantiate and add output data entities to the task, as specified in the KG schema
            self._add_outputs_to_task(next_task, method_instance)

    def save_created_kg(self, file_path: str) -> None:
        """
        Saves self.output_kg to a file
        Args:
            file_path: path of the output file
        """
        # check_kg_executability(self.output_kg)

        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        self.output_kg.serialize(destination=file_path)
        print(f"Executable KG saved in {file_path}")

    def name_instance(
        self,
        parent_entity: Entity,
    ) -> Union[None, str]:
        """
        Creates a unique name for a new instance by concatenating the parent entity's name (which is the instance type) with a number
        Also increments the relevant number of the corresponding dict
        Args:
            task_type_dict: contains pairs of task types and numbers
            method_type_dict: contains pairs of method types and numbers
            parent_entity: instance's parent entity

        Returns:
            str: name to be given to the new instance
            None: if the type of the given parent entity is not equal with "AtomicTask" or "AtomicMethod"
        """
        if parent_entity.type == "AtomicTask":
            entity_type_dict = self.task_type_dict
        elif parent_entity.type == "AtomicMethod":
            entity_type_dict = self.method_type_dict
        else:
            print("Error: Invalid parent entity type")
            return None

        instance_name = parent_entity.name + str(entity_type_dict[parent_entity.name])
        entity_type_dict[parent_entity.name] += 1
        return instance_name
