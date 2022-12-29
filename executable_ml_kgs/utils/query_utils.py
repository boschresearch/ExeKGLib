from typing import Optional, Callable, Tuple

from rdflib import URIRef, Graph, query, Namespace

from classes.entity import Entity


def query_method_parent_classes(kg, method_iri):
    return kg.query(
        f"SELECT ?c WHERE {{ ?method rdfs:subClassOf ?c . }}",
        initBindings={"method": URIRef(method_iri)},
    )


def query_entity_parent_iri(kg, entity_iri: str, upper_class_uri_ref: URIRef):
    return kg.query(
        f"SELECT ?t WHERE {{ ?entity rdf:type ?t ."
        f"                   ?t rdfs:subClassOf* ?upper_class .}}",
        initBindings={
            "entity": URIRef(entity_iri),
            "upper_class": upper_class_uri_ref,
        },
    )


def query_data_entity_reference_iri(kg, namespace_prefix, entity_iri: str):
    return kg.query(
        f"SELECT ?r WHERE {{ ?entity {namespace_prefix}:hasReference ?r . }}",
        initBindings={
            "entity": URIRef(entity_iri),
        },
    )


def query_method_iri_by_task_iri(kg, namespace_prefix, task_iri: str):
    return kg.query(
        f"SELECT ?m WHERE {{ ?task ?m_property ?m ."
        f"                   ?m_property rdfs:subPropertyOf* {namespace_prefix}:hasMethod .}}",
        initBindings={"task": URIRef(task_iri)},
    )


def get_first_query_result_if_exists(query_method: Callable, *args) -> Optional[str]:
    query_result = next(
        iter(list(query_method(*args))),
        None,
    )

    if query_result is None:
        return None

    return query_result


def get_data_properties_by_entity_iri(entity_iri: str, kg: Graph) -> query.Result:
    return kg.query(
        "\nSELECT ?p ?r WHERE {?p rdfs:domain ?entity_iri . "
        "?p rdfs:range ?r . "
        "?p rdf:type owl:DatatypeProperty . }",
        initBindings={"entity_iri": URIRef(entity_iri)},
    )


def get_method_properties_and_methods(
    input_kg, namespace_prefix, entity_parent_iri: str
) -> query.Result:
    return input_kg.query(
        "\nSELECT ?p ?m WHERE {?p rdfs:domain ?entity_iri . "
        "?p rdfs:range ?m . "
        "?m rdfs:subClassOf " + namespace_prefix + ":AtomicMethod . }",
        initBindings={"entity_iri": URIRef(entity_parent_iri)},
    )  # method property


def get_input_properties_and_inputs(
    input_kg, namespace_prefix, entity_parent_iri: str
) -> query.Result:
    return input_kg.query(
        "\nSELECT ?p ?m WHERE {?p rdfs:domain ?entity_iri . "
        "?p rdfs:range ?m ."
        "?p rdfs:subPropertyOf " + namespace_prefix + ":hasInput ."
        "?m rdfs:subClassOf " + namespace_prefix + ":DataEntity . }",
        initBindings={"entity_iri": URIRef(entity_parent_iri)},
    )


def get_output_properties_and_outputs(
    input_kg, namespace_prefix, entity_parent_iri: str
) -> query.Result:
    return input_kg.query(
        "\nSELECT ?p ?m WHERE {?p rdfs:domain ?entity_iri . "
        "?p rdfs:range ?m ."
        "?p rdfs:subPropertyOf " + namespace_prefix + ":hasOutput ."
        "?m rdfs:subClassOf " + namespace_prefix + ":DataEntity . }",
        initBindings={"entity_iri": URIRef(entity_parent_iri)},
    )


def query_pipeline_and_first_task_iri(kg, namespace_prefix):
    return kg.query(
        f"\nSELECT ?p ?t WHERE {{?p rdf:type {namespace_prefix}:Pipeline ;"
        f"                       {namespace_prefix}:hasStartTask ?t . }}"
    )


def get_subclasses_of(class_iri: str, kg: Graph) -> query.Result:
    return kg.query(
        "\nSELECT ?t WHERE {?t rdfs:subClassOf ?class_iri . }",
        initBindings={"class_iri": class_iri},
    )


def get_data_properties_plus_inherited_by_class_iri(input_kg, class_iri: str):
    property_list = list(get_data_properties_by_entity_iri(class_iri, input_kg))
    method_parent_classes = list(query_method_parent_classes(input_kg, class_iri))
    for method_class_result_row in method_parent_classes:
        property_list += list(
            get_data_properties_by_entity_iri(method_class_result_row[0], input_kg)
        )

    return property_list


def get_pipeline_and_first_task_iri(
    kg: Graph, namespace_prefix: str
) -> Tuple[str, str]:
    # assume one pipeline per file
    query_result = get_first_query_result_if_exists(
        query_pipeline_and_first_task_iri,
        kg,
        namespace_prefix,
    )
    if query_result is None:
        print("Error: Pipeline and first task not found")
        exit(1)

    pipeline_iri, task_iri = query_result

    return str(pipeline_iri), str(task_iri)


def get_method_by_task_iri(
    kg: Graph,
    namespace_prefix: str,
    namespace: Namespace,
    task_iri: str,
) -> Optional[Entity]:
    query_result = get_first_query_result_if_exists(
        query_method_iri_by_task_iri,
        kg,
        namespace_prefix,
        task_iri,
    )
    if query_result is None:
        return None

    method_iri = str(query_result[0])

    query_result = get_first_query_result_if_exists(
        query_entity_parent_iri,
        kg,
        method_iri,
        namespace.Method,
    )
    if query_result is None:
        return None

    method_parent_iri = str(query_result[0])

    return Entity(method_iri, Entity(method_parent_iri))
