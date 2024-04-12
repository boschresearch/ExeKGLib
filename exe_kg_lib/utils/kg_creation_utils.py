# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from rdflib import RDF, XSD, Graph, Literal, Namespace, URIRef

from ..classes.data_entity import DataEntity
from ..classes.entity import Entity
from ..classes.task import Task


def add_instance(kg: Graph, entity_instance: Entity) -> None:
    """
    Adds entity instance to KG
    Args:
        kg: Graph object to add to
        entity_instance: the entity instance to create
    """
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
    plots_output_dir: str,
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

    plots_output_dir_literal = Literal(lexical_or_value=plots_output_dir, datatype=XSD.string)
    add_literal(kg, pipeline, top_level_schema_namespace.hasPlotsOutputDir, plots_output_dir_literal)

    return pipeline
