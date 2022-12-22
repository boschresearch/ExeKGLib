from typing import List, Union, Tuple

from classes.data_entity import DataEntity
from classes.entity import Entity


def get_input_for_existing_data_entities(
    existing_data_entity_list: List[DataEntity],
) -> Union[None, List[DataEntity]]:
    chosen_data_entity_list = []
    print("Select input for the task from existing data entities:")
    while True:
        for i, data_entity in enumerate(existing_data_entity_list):
            print("\t{}. {}".format(str(i), data_entity.name))
        print("\t{}. Continue to choose new input columns".format(str(-1)))
        chosen_data_entity_i = int(input())
        if chosen_data_entity_i == -1:
            break

        chosen_data_entity_list.append(existing_data_entity_list[chosen_data_entity_i])

    return chosen_data_entity_list


def get_input_for_new_data_entities(
    data_semantics_list: List[Entity], data_structure_list: List[Entity]
) -> Tuple[list, list, list]:
    source_list = []
    data_semantics_iri_list = []
    data_structure_iri_list = []

    prompt = "Enter input columns for the task, enter 'quit' to stop input: "
    source = input(prompt)
    while source != "quit":
        source_list.append(source)

        print(f"Choose data semantics for {source}:")
        for i, t in enumerate(data_semantics_list):
            print("\t{}. {}".format(str(i), t.name))
        chosen_data_semantics_id = int(input())
        data_semantics_iri_list.append(
            data_semantics_list[chosen_data_semantics_id].iri
        )

        print(f"Choose data structure for {source}:")
        for i, t in enumerate(data_structure_list):
            print("\t{}. {}".format(str(i), t.name))
        chosen_data_structure_id = int(input())
        data_structure_iri_list.append(
            data_structure_list[chosen_data_structure_id].iri
        )

        source = input(prompt)

    return source_list, data_semantics_iri_list, data_structure_iri_list
