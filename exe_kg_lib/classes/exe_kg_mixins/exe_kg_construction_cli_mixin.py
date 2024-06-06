# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from typing import Callable, Dict, List, Union

from rdflib import Graph, Namespace

from exe_kg_lib.classes.data_entity import DataEntity
from exe_kg_lib.classes.entity import Entity
from exe_kg_lib.classes.kg_schema import KGSchema
from exe_kg_lib.classes.task import Task
from exe_kg_lib.utils.cli_utils import (get_input_for_existing_data_entities,
                                        get_input_for_new_data_entities)
from exe_kg_lib.utils.kg_creation_utils import (
    add_instance_from_parent_with_relation, add_literal, create_pipeline_task)
from exe_kg_lib.utils.kg_validation_utils import check_kg_executability
from exe_kg_lib.utils.query_utils import (get_grouped_inherited_inputs,
                                          get_method_grouped_params,
                                          query_method_properties_and_methods)


class ExeKGConstructionCLIMixin:
    # see exe_kg_lib/classes/exe_kg_base.py for the definition of these attributes
    output_kg: Graph
    top_level_schema: KGSchema
    bottom_level_schemata: Dict[str, KGSchema]
    data_entity: Entity
    pipeline: Entity
    input_kg: Graph
    atomic_task_list: List[Entity]
    atomic_method_list: List[Entity]
    data_type_list: List[Entity]
    data_semantics_list: List[Entity]
    data_structure_list: List[Entity]
    existing_data_entity_list: List[DataEntity]
    last_created_task: Union[None, Task]
    canvas_task_created: bool
    shacl_shapes_s: str
    _add_outputs_to_task: Callable[[Task, Entity], None]

    def start_pipeline_creation_cli(
        self, pipeline_name: str, input_data_path: str, input_plots_output_dir: str
    ) -> None:
        """
        Starts the creation of a pipeline in the form of ExeKG via CLI.

        Args:
            pipeline_name (str): The name of the pipeline.
            input_data_path (str): The path to the input data.
            input_plots_output_dir (str): The directory to output the input plots.

        Returns:
            None
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

            method_instance = self._create_method_cli(next_task)

            # instantiate and add input data entities to the task based on user input
            self._add_inputs_to_task_cli(next_task.parent_entity.namespace, next_task)
            # instantiate and add output data entities to the task, as specified in the KG schema
            self._add_outputs_to_task(next_task, method_instance)

    def _create_next_task_cli(self) -> Union[None, Task]:
        """
        Prompts the user to choose the next task and creates a Task object based on the user's input.
        Adds the task to the output KG and adds its output data entities to self.existing_data_entity_list.

        Returns:
            Union[None, Task]: The created Task object or None if the user chooses to end the pipeline.
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

    def _add_inputs_to_task_cli(
        self,
        namespace: Namespace,
        task_instance: Task,
    ) -> None:
        """
        Prompts user to create input data entities.
        Adds the data entities as inputs to the given task of the output KG.

        Args:
            namespace (Namespace): The namespace of the task instance.
            task_instance (Task): The task instance to add inputs to.

        Returns:
            None
        """

        # fetch compatible inputs from KG schema
        results = list(
            get_grouped_inherited_inputs(
                self.input_kg,
                self.top_level_schema.namespace_prefix,
                task_instance.parent_entity.iri,
            )
        )

        for input_entity_iri, info_l in results:
            data_structure_iris = [pair[0] for pair in info_l]
            input_property_iri = info_l[0][1]  # common input property for all data structures
            input_entity_name = input_entity_iri.split("#")[1]
            data_structure_names = [iri.split("#")[1] for iri in data_structure_iris]

            print(f"Specify input corresponding to {input_entity_name} with data structures {data_structure_names}")
            input_data_entity_list = get_input_for_existing_data_entities(self.existing_data_entity_list)
            input_data_entity_list += get_input_for_new_data_entities(
                self.data_semantics_list,
                self.data_structure_list,
                namespace,
                self.data_entity,
            )

            self._add_input_data_entities_to_task(
                input_entity_iri, input_data_entity_list, input_property_iri, task_instance
            )

    def _create_method_cli(self, task_to_attach_to: Entity) -> Entity:
        """
        Prompts the user to choose a method to attach to the given task.
        Links the method to the given task in the output KG and adds method parameters as literals.

        Args:
            task_to_attach_to (Entity): The task entity to attach the method to.

        Returns:
            method_instance (Entity): The instance of the selected method linked to the task.
        """
        print(f"Please choose a method for {task_to_attach_to.type}:")

        # fetch compatible methods and their properties from KG schema
        results = list(
            query_method_properties_and_methods(
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
        property_list = get_method_grouped_params(
            method_parent.iri,
            self.top_level_schema.namespace_prefix,
            self.input_kg,
            inherited=method_parent.namespace == str(self.bottom_level_schemata["visu"].namespace),
        )

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
                except (SyntaxError, NameError):
                    input_value = input_value_s

                literal = self._field_value_to_literal(input_value)
                add_literal(self.output_kg, method_instance, property_iri, literal)

        # check_kg_executability(self.output_kg)

        return method_instance
