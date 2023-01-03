from typing import Union, Dict

from rdflib import RDF, URIRef, Literal, Graph, Namespace, XSD

from classes.data_entity import DataEntity
from classes.entity import Entity
from classes.task import Task
from utils.query_utils import (
    get_first_query_result_if_exists,
    get_data_properties_by_entity_iri,
)


def add_instance(kg: Graph, entity_instance: Entity) -> None:
    if entity_instance.parent_entity and (entity_instance.iri, None, None) not in kg:
        kg.add((entity_instance.iri, RDF.type, entity_instance.parent_entity.iri))


def add_relation(
    kg: Graph, from_entity: Entity, relation_iri: str, to_entity: Entity
) -> None:
    kg.add(
        (
            from_entity.iri,
            URIRef(relation_iri),
            to_entity.iri,
        )
    )


def add_literal(
    kg: Graph, from_entity: Entity, relation_iri: str, literal: Literal
) -> None:
    kg.add((from_entity.iri, URIRef(relation_iri), literal))


def add_instance_from_parent_with_relation(
    namespace: Namespace,
    kg: Graph,
    parent_entity: Entity,
    relation_iri: str,
    related_entity: Entity,
    instance_name: str,
) -> Entity:
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
    add_data_entity_instance(
        kg, data, top_level_kg, top_level_schema_namespace, data_entity
    )
    add_relation(kg, task_entity, relation, data_entity)


def create_pipeline_task(
    top_level_namespace,
    bottom_level_schema_namespace,
    pipeline1,
    output_kg,
    pipeline_name: str,
    input_data_path: str,
) -> Task:
    pipeline = Task(
        bottom_level_schema_namespace + pipeline_name,
        pipeline1,
    )
    add_instance(output_kg, pipeline)

    input_data_path_literal = Literal(
        lexical_or_value=input_data_path,
        datatype=XSD.string,
    )
    add_literal(
        output_kg,
        pipeline,
        top_level_namespace.hasInputDataPath,
        input_data_path_literal,
    )

    return pipeline
