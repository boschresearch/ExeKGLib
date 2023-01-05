from typing import List

from rdflib import Namespace

from classes.data_entity import DataEntity
from classes.entity import Entity


def get_input_for_existing_data_entities(
        existing_data_entity_list: List[DataEntity],
) -> List[DataEntity]:
    if not existing_data_entity_list:
        return []

    chosen_data_entity_list = []
    print("Choose input for the task from existing data entities:")
    while True:
        for i, data_entity in enumerate(existing_data_entity_list):
            print("\t{}. {}".format(str(i), data_entity.name))
        print("\t{}. Continue".format(str(-1)))
        chosen_data_entity_i = int(input())
        if chosen_data_entity_i == -1:
            break

        chosen_data_entity_list.append(existing_data_entity_list[chosen_data_entity_i])

    return chosen_data_entity_list


def get_input_for_new_data_entities(
        data_semantics_list: List[Entity], data_structure_list: List[Entity], namespace: Namespace, data_entity: Entity
) -> List[DataEntity]:
    data_entities = []

    prompt = "Enter input columns, then 'quit' when done: "
    source = input(prompt)
    while source != "quit":
        new_data_entity = DataEntity(
            namespace + source,
            data_entity,
            source
        )

        print(f"Choose data semantics for {source}:")
        for i, t in enumerate(data_semantics_list):
            print("\t{}. {}".format(str(i), t.name))
        chosen_data_semantics_id = int(input())
        new_data_entity.has_data_semantics = data_semantics_list[chosen_data_semantics_id].iri

        print(f"Choose data structure for {source}:")
        for i, t in enumerate(data_structure_list):
            print("\t{}. {}".format(str(i), t.name))
        chosen_data_structure_id = int(input())
        new_data_entity.has_data_structure = data_structure_list[chosen_data_structure_id].iri

        data_entities.append(new_data_entity)

        source = input(prompt)

    return data_entities


def input_pipeline_info():
    pipeline_name = input("Enter a name for the pipeline: ")
    input_data_path = input("Enter a path for the input data: ")

    return pipeline_name, input_data_path
