# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

import os
import re
from io import TextIOWrapper
from pathlib import Path
from typing import Callable, Dict, List, Union

from rdflib import RDF, XSD, Graph, Literal, Namespace, URIRef

from exe_kg_lib.classes.exe_kg_serialization.method import \
    Method as MethodSerializable
from exe_kg_lib.classes.exe_kg_serialization.pipeline import Pipeline
from exe_kg_lib.classes.method import Method
from exe_kg_lib.utils.kg_validation_utils import check_kg_executability
from exe_kg_lib.utils.string_utils import (TASK_OUTPUT_NAME_REGEX,
                                           get_instance_name)

from ..classes.data_entity import DataEntity
from ..classes.entity import Entity
from ..classes.exe_kg_serialization.task import Task as TaskSerializable
from ..classes.task import Task


def add_instance(kg: Graph, entity_instance: Entity, extra_parent_iri: str = None) -> None:
    """
    Adds an instance of an entity to the knowledge graph.

    Parameters:
        kg (Graph): The knowledge graph to add the instance to.
        entity_instance (Entity): The entity instance to be added.
        extra_parent_iri (str): An extra parent IRI to add to the instance.

    Returns:
        None
    """
    kg.add((entity_instance.iri, RDF.type, entity_instance.parent_entity.iri))
    if extra_parent_iri:
        kg.add((entity_instance.iri, RDF.type, URIRef(extra_parent_iri)))


def add_relation(kg: Graph, from_entity: Entity, relation_iri: str, to_entity: Entity) -> None:
    """
    Adds a relation between two entities in the knowledge graph.

    Args:
        kg (Graph): The knowledge graph to add the relation to.
        from_entity (Entity): The entity from which the relation originates.
        relation_iri (str): The IRI of the relation.
        to_entity (Entity): The entity to which the relation points.

    Returns:
        None
    """
    kg.add(
        (
            from_entity.iri,
            URIRef(relation_iri),
            to_entity.iri,
        )
    )


def add_literal(kg: Graph, from_entity: Entity, relation_iri: str, literal: Literal) -> None:
    """
    Adds a literal value to the knowledge graph.

    Parameters:
        kg (Graph): The knowledge graph to add the literal to.
        from_entity (Entity): The entity from which the relation originates.
        relation_iri (str): The IRI of the relation.
        literal (Literal): The literal value to add.

    Returns:
        None
    """
    kg.add((from_entity.iri, URIRef(relation_iri), literal))


def add_instance_from_parent_with_relation(
    namespace: Namespace,
    kg: Graph,
    parent_entity: Entity,
    relation_iri: str,
    related_entity: Entity,
    instance_name: str,
    extra_parent_iri: str = None,
) -> Entity:
    """
    Adds an instance to the knowledge graph with a relation to a given entity.

    Args:
        namespace (Namespace): The namespace for the instance.
        kg (Graph): The knowledge graph.
        parent_entity (Entity): The parent entity of the instance.
        relation_iri (str): The IRI of the relation between the related entity and the instance.
        related_entity (Entity): The related entity.
        instance_name (str): The name of the instance.
        extra_parent_iri (str): An extra parent IRI to add to the instance.

    Returns:
        Entity: The created instance.
    """
    entity_iri = namespace + instance_name
    instance = Entity(entity_iri, parent_entity)

    add_instance(kg, instance, extra_parent_iri)
    add_relation(kg, related_entity, relation_iri, instance)

    return instance


def add_data_entity_instance(
    kg: Graph,
    data: Entity,
    top_level_kg: Graph,
    top_level_schema_namespace: Namespace,
    data_entity: DataEntity,
) -> None:
    """
    Adds a data entity instance to the knowledge graph.

    Args:
        kg (Graph): The knowledge graph to add the data entity instance to.
        data (Entity): The data entity instance to be added.
        top_level_kg (Graph): The top-level knowledge graph.
        top_level_schema_namespace (Namespace): The namespace for the top-level schema.
        data_entity (DataEntity): The data entity object.

    Returns:
        None
    """
    add_instance(kg, data_entity)

    if data_entity.source:
        # has_source_iri, range_iri = get_first_query_result_if_exists(
        #     get_method_params_plus_inherited, data_entity.parent_entity.iri, top_level_kg
        # )

        source_literal = Literal(
            lexical_or_value=data_entity.source,
            datatype=XSD.string,
        )

        add_literal(kg, data_entity, top_level_schema_namespace.hasSource, source_literal)

    if data_entity.data_structure:
        add_relation(
            kg,
            data_entity,
            RDF.type,
            Entity(data_entity.data_structure),
        )

    if data_entity.data_semantics:
        add_relation(
            kg,
            data_entity,
            RDF.type,
            Entity(data_entity.data_semantics),
        )

    if data_entity.reference:
        add_relation(
            kg,
            data_entity,
            top_level_schema_namespace.hasReference,
            Entity(data_entity.reference),
        )


def add_and_attach_data_entity(
    kg: Graph,
    data: Entity,
    top_level_kg: Graph,
    top_level_schema_namespace: Namespace,
    data_entity: DataEntity,
    relation: URIRef,
    task_entity: Task,
) -> None:
    """
    Adds a data entity to the knowledge graph and attaches it to a task entity using a specified relation.

    Args:
        kg (Graph): The knowledge graph to add the data entity to.
        data (Entity): The data entity to add.
        top_level_kg (Graph): The top-level knowledge graph.
        top_level_schema_namespace (Namespace): The namespace for the top-level schema.
        data_entity (DataEntity): The data entity to attach.
        relation (URIRef): The relation to use for attaching the data entity.
        task_entity (Task): The task entity to attach the data entity to.

    Returns:
        None
    """
    add_data_entity_instance(kg, data, top_level_kg, top_level_schema_namespace, data_entity)
    add_relation(kg, task_entity, relation, data_entity)


def create_pipeline_task(
    top_level_schema_namespace: Namespace,
    parent_entity: Entity,
    kg: Graph,
    pipeline_name: str,
    input_data_path: str,
    plots_output_dir: str,
) -> Task:
    """
    Create a pipeline task in the knowledge graph.

    Args:
        top_level_schema_namespace (Namespace): The top-level schema namespace.
        parent_entity (Entity): The parent entity of the pipeline task.
        kg (Graph): The knowledge graph.
        pipeline_name (str): The name of the pipeline.
        input_data_path (str): The path to the input data for the pipeline.
        plots_output_dir (str): The directory to store the output plots when executing the pipeline.

    Returns:
        Task: The created pipeline task.
    """
    pipeline = Task(top_level_schema_namespace + pipeline_name, parent_entity)
    add_instance(kg, pipeline)

    input_data_path_literal = Literal(lexical_or_value=input_data_path, datatype=XSD.string)
    add_literal(kg, pipeline, top_level_schema_namespace.hasInputDataPath, input_data_path_literal)

    plots_output_dir_literal = Literal(lexical_or_value=plots_output_dir, datatype=XSD.string)
    add_literal(kg, pipeline, top_level_schema_namespace.hasPlotsOutputDir, plots_output_dir_literal)

    return pipeline


def deserialize_input_entity_info_dict(
    input_entity_info_dict: Dict[str, Union[List[str], MethodSerializable]],
    data_entities_dict: Dict[str, DataEntity],
    task_output_dicts: Dict[str, TaskSerializable],
    pipeline_name: str,
    namespace: Namespace,
) -> Dict[str, Union[List[DataEntity], Method]]:
    """
    Deserializes the serialized input entity dictionary.

    Args:
        input_entity_info_dict (Dict[str, Union[List[str], MethodSerializable]]): The serialized input entity dictionary.
        data_entities_dict (Dict[str, DataEntity]): The dictionary of data entities.
        task_output_dicts (Dict[str, TaskSerializable]): The dictionary of task output objects.
        pipeline_name (str): The name of the pipeline.

    Returns:
        Dict[str, Union[List[DataEntity], Method]]: The deserialized input data entity dictionary.
    """
    input_entity_dict: Dict[str, List[DataEntity]] = {}
    for input_name, input_value in input_entity_info_dict.items():
        if isinstance(input_value, MethodSerializable):  # provided input is a method
            input_method = input_value
            input_entity_dict[input_name] = Method(
                namespace + input_method.method_type, parent_entity=None, params_dict=input_method.params_dict
            )
        elif isinstance(input_value, list) and all(
            isinstance(elem, str) for elem in input_value
        ):  # provided input is list of data entity names
            input_data_entity_names = input_value
            input_entity_dict[input_name] = []
            for data_entity_name in input_data_entity_names:
                match = re.match(TASK_OUTPUT_NAME_REGEX, data_entity_name)
                if match:
                    # input entity refers to a data entity that is an output of a previous task
                    prev_task_output_name = match.group(1)
                    prev_task_type = match.group(2)
                    prev_task_instance_number = int(match.group(3))

                    try:
                        # regex matched so assume that the data_entity_name is an output of a previous task
                        prev_task_name = get_instance_name(prev_task_type, prev_task_instance_number, pipeline_name)
                        input_entity_dict[input_name].append(task_output_dicts[prev_task_name][prev_task_output_name])
                    except KeyError:
                        # regex matched but the data_entity_name is NOT an output of a previous task
                        input_entity_dict[input_name].append(data_entities_dict[data_entity_name])
                else:
                    input_entity_dict[input_name].append(data_entities_dict[data_entity_name])

    return input_entity_dict


def load_exe_kg(input_path: str, exe_kg_from_json_method: Callable[[Union[Path, TextIOWrapper, str]], Graph]) -> Graph:
    """
    Loads the ExeKG from the specified input path.

    Args:
        input_path (str): The path to the ExeKG file.
        exe_kg_from_json_method (Callable[[str], Graph]): The method to convert a simplified serialized pipeline to ExeKG.

    Returns:
        Graph: The loaded ExeKG.
    """
    input_exe_kg = Graph(bind_namespaces="rdflib")
    if input_path.endswith(".ttl"):
        # parse ExeKG from Turtle file
        input_exe_kg.parse(input_path, format="n3")
    elif input_path.endswith(".json"):
        # convert simplified serialized pipeline to ExeKG
        input_exe_kg = exe_kg_from_json_method(input_path)

    return input_exe_kg


def field_value_to_literal(field_value: Union[str, int, float, bool]) -> Literal:
    """
    Converts a Python field value to a Literal object with the appropriate datatype.

    Args:
        field_value (Union[str, int, float, bool]): The value to be converted.

    Returns:
        Literal: The converted Literal object.

    """
    if isinstance(field_value, str):
        return Literal(field_value, datatype=XSD.string)
    elif isinstance(field_value, bool):
        return Literal(field_value, datatype=XSD.boolean)
    elif isinstance(field_value, int):
        return Literal(field_value, datatype=XSD.int)
    elif isinstance(field_value, float):
        return Literal(field_value, datatype=XSD.float)
    else:
        return Literal(str(field_value), datatype=XSD.string)


def save_exe_kg(
    exe_kg: Graph,
    input_kg: Graph,
    shacl_shapes_s: str,
    pipeline_serializable: Pipeline,
    dir_path: str,
    pipeline_name: str,
    check_executability: bool = True,
    save_to_ttl: bool = True,
    save_to_json: bool = True,
) -> None:
    if check_executability:
        check_kg_executability(exe_kg + input_kg, shacl_shapes_s)

    os.makedirs(dir_path, exist_ok=True)

    if save_to_ttl:
        # save the ExeKG in RDF/Turtle format
        ttl_file_path = os.path.join(dir_path, f"{pipeline_name}.ttl")
        exe_kg.serialize(destination=ttl_file_path)
        print(f"Executable KG saved in RDF/Turtle format at {ttl_file_path}.")

    if save_to_json:
        # save the simplified pipeline in JSON format
        json_file_path = os.path.join(dir_path, f"{pipeline_name}.json")
        with open(json_file_path, "w+") as json_file:
            json_file.write(pipeline_serializable.to_json())
        print(f"Pipeline (simplified) saved in JSON format to {json_file_path}.")
