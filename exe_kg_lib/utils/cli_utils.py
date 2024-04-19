# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from typing import List, Tuple

from rdflib import Namespace

from ..classes.data_entity import DataEntity
from ..classes.entity import Entity


def get_input_for_existing_data_entities(
    existing_data_entity_list: List[DataEntity],
) -> List[DataEntity]:
    """
    Prompts the user to choose input for a task from a list of existing data entities.

    Args:
        existing_data_entity_list (List[DataEntity]): A list of existing data entities.

    Returns:
        List[DataEntity]: A list of chosen data entities.
    """
    if not existing_data_entity_list:
        return []

    chosen_data_entity_list = []
    print("Choose input for the task from existing data entities:")
    while True:
        for i, data_entity in enumerate(existing_data_entity_list):
            print(f"\t{str(i)}. {data_entity.name}")
        print(f"\t{str(-1)}. Continue")
        chosen_data_entity_i = int(input())
        if chosen_data_entity_i == -1:
            break

        chosen_data_entity_list.append(existing_data_entity_list[chosen_data_entity_i])

    return chosen_data_entity_list


def get_input_for_new_data_entities(
    data_semantics_list: List[Entity], data_structure_list: List[Entity], namespace: Namespace, data_entity: Entity
) -> List[DataEntity]:
    """
    Prompts the user to enter input columns and their corresponding data semantics and data structure.

    Args:
        data_semantics_list (List[Entity]): A list of available data semantics.
        data_structure_list (List[Entity]): A list of available data structures.
        namespace (Namespace): The namespace for the new data entities.
        data_entity (Entity): The data entity to which the new data entities belong.

    Returns:
        List[DataEntity]: A list of newly created data entities.
    """
    data_entities = []

    prompt = "Enter input columns, then 'quit' when done: "
    source = input(prompt)
    while source != "quit":
        new_data_entity = DataEntity(namespace + source, data_entity, source)

        print(f"Choose data semantics for {source}:")
        for i, t in enumerate(data_semantics_list):
            print(f"\t{str(i)}. {t.name}")
        chosen_data_semantics_id = int(input())
        new_data_entity.data_semantics = data_semantics_list[chosen_data_semantics_id].iri

        print(f"Choose data structure for {source}:")
        for i, t in enumerate(data_structure_list):
            print(f"\t{str(i)}. {t.name}")
        chosen_data_structure_id = int(input())
        new_data_entity.data_structure = data_structure_list[chosen_data_structure_id].iri

        data_entities.append(new_data_entity)

        source = input(prompt)

    return data_entities


def input_pipeline_info() -> Tuple[str, str, str]:
    """
    Prompts the user to enter information about the pipeline.

    Returns:
        A tuple containing the pipeline name, input data path, and output directory for saving plots.
    """
    pipeline_name = input("Enter a name for the pipeline: ")
    input_data_path = input("Enter a path for the input data: ")
    input_plots_output_dir = input("Enter a path for saving the plots: ")

    return pipeline_name, input_data_path, input_plots_output_dir
