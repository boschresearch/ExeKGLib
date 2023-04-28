# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from typing import Dict, Union

from rdflib import RDF, XSD, Graph, Literal, Namespace, URIRef

from ..classes.data_entity import DataEntity
from ..classes.entity import Entity
from ..classes.task import Task
from .query_utils import (get_data_properties_by_entity_iri,
                          get_first_query_result_if_exists)


def add_instance(kg: Graph, entity_instance: Entity) -> None:
    """
    Adds entity instance to KG only if its parent entity exists and there is no instance with the same IRI
    Args:
        kg: Graph object to add to
        entity_instance: the entity instance to create
    """
    if entity_instance.parent_entity and (entity_instance.iri, None, None) not in kg:
        kg.add((entity_instance.iri, RDF.type, entity_instance.parent_entity.iri))


def add_relation(kg: Graph, from_entity: Entity, relation_iri: str, to_entity: Entity) -> None:
    """
    Adds relation between 2 given entities to KG
    Args:
        kg: Graph object to add to
        from_entity: relation source
        relation_iri: IRI that connects the 2 given entities
        to_entity: relation destination
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
    Adds relation between a given entity and a given literal to KG
    Args:
        kg: Graph object to add to
        from_entity: relation source
        relation_iri: IRI that connects the given entity with the given literal
        literal: literal to add to Graph object
    """
    kg.add((from_entity.iri, URIRef(relation_iri), literal))


def add_instance_from_parent_with_relation(
    namespace: Namespace,
    kg: Graph,
    parent_entity: Entity,
    relation_iri: str,
    related_entity: Entity,
    instance_name: str,
) -> Entity:
    """
    Creates an entity object based on the arguments and calls add_instance() and add_relation() to create a new entity instance and relation
    Args:
        namespace: namespace for the new instance
        kg: Graph object to add to
        parent_entity: parent entity for the new instance
        relation_iri: IRI that connects the given related_entity with the new instance
        related_entity: relation source
        instance_name: name for the new instance

    Returns:
        Entity: object containing the new entity instance's basic info
    """
    entity_iri = namespace + instance_name
    instance = Entity(entity_iri, parent_entity)

    add_instance(kg, instance)
    add_relation(kg, related_entity, relation_iri, instance)

    return instance


def name_instance(
    task_type_dict: Dict[str, int],
    method_type_dict: Dict[str, int],
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
        entity_type_dict = task_type_dict
    elif parent_entity.type == "AtomicMethod":
        entity_type_dict = method_type_dict
    else:
        print("Error: Invalid parent entity type")
        return None

    instance_name = parent_entity.name + str(entity_type_dict[parent_entity.name])
    entity_type_dict[parent_entity.name] += 1
    return instance_name


def add_data_entity_instance(
    kg: Graph,
    data: Entity,
    top_level_kg: Graph,
    top_level_schema_namespace: Namespace,
    data_entity: DataEntity,
) -> None:
    """
    Adds data entity instance to kg with the necessary relations
    Args:
        kg: Graph object to add to
        data: object representing top-level DataEntity class in KG
        top_level_kg: KG corresponding to the top-level KG schema
        top_level_schema_namespace: namespace of the top-level KG schema
        data_entity: data entity to add
    """
    add_instance(kg, data_entity)

    if data_entity.has_source:
        has_source_iri, range_iri = get_first_query_result_if_exists(
            get_data_properties_by_entity_iri, data.iri, top_level_kg
        )

        source_literal = Literal(
            lexical_or_value=data_entity.has_source,
            datatype=range_iri,
        )

        add_literal(kg, data_entity, has_source_iri, source_literal)

    if data_entity.has_data_structure:
        add_relation(
            kg,
            data_entity,
            top_level_schema_namespace.hasDataStructure,
            Entity(data_entity.has_data_structure),
        )

    if data_entity.has_data_semantics:
        add_relation(
            kg,
            data_entity,
            top_level_schema_namespace.hasDataSemantics,
            Entity(data_entity.has_data_semantics),
        )

    if data_entity.has_reference:
        add_relation(
            kg,
            data_entity,
            top_level_schema_namespace.hasReference,
            Entity(data_entity.has_reference),
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
    Adds data entity instance to kg with the necessary relations, and attaches it to the given task
    Args:
        kg: Graph object to add to
        data: object representing top-level DataEntity class in KG
        top_level_kg: KG corresponding to the top-level KG schema
        top_level_schema_namespace: namespace of the top-level KG schema
        data_entity: data entity to add
        relation: IRI of relation to add
        task_entity: task to attach the data entity to
    """
    add_data_entity_instance(kg, data, top_level_kg, top_level_schema_namespace, data_entity)
    add_relation(kg, task_entity, relation, data_entity)


def create_pipeline_task(
    top_level_schema_namespace: Namespace,
    parent_entity: Entity,
    kg: Graph,
    pipeline_name: str,
    input_data_path: str,
) -> Task:
    """
    Adds instance of pipeline task to kg
    Args:
        top_level_schema_namespace: namespace of the top-level KG schema
        parent_entity: parent entity of pipeline instance
        kg: Graph object to add to
        pipeline_name: name for the pipeline
        input_data_path: path for the input data to be used by the pipeline's tasks

    Returns:
        Task: created pipeline task
    """
    pipeline = Task(top_level_schema_namespace + pipeline_name, parent_entity)
    add_instance(kg, pipeline)

    input_data_path_literal = Literal(lexical_or_value=input_data_path, datatype=XSD.string)
    add_literal(kg, pipeline, top_level_schema_namespace.hasInputDataPath, input_data_path_literal)

    return pipeline
