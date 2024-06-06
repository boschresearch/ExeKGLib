# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

import itertools
from typing import Callable, List, Optional, Tuple

from rdflib import Graph, Namespace, URIRef, query

from exe_kg_lib.classes.method import Method
from exe_kg_lib.utils.string_utils import (camel_to_snake,
                                           class_name_to_method_name,
                                           class_name_to_module_name)

from ..classes.entity import Entity


class NoResultsError(Exception):
    pass


def query_parent_classes(kg: Graph, entity_iri: str) -> query.Result:
    """
    Queries the knowledge graph to retrieve the parent classes of a given entity.

    Args:
        kg (Graph): The knowledge graph to query.
        entity_iri (str): The IRI of the entity.

    Returns:
        query.Result: The result of the query.
    """
    return kg.query(
        f"SELECT ?c WHERE {{ ?entity rdfs:subClassOf ?c . }}",
        initBindings={"entity": URIRef(entity_iri)},
    )


def query_instance_parent_iri(
    kg: Graph, entity_iri: str, upper_class_uri_ref: URIRef, negation_of_inheritance: bool = False
) -> query.Result:
    """
    Queries the knowledge graph to find the types of a given entity, that are subclasses of a given upper class.

    Args:
        kg (Graph): The knowledge graph to query.
        entity_iri (str): The IRI of the entity.
        upper_class_uri_ref (URIRef): The URI reference of the upper class.

    Returns:
        query.Result: The result of the query.
    """
    query_string = f"SELECT ?t WHERE {{ ?entity rdf:type ?t ."

    if negation_of_inheritance:
        query_string += f"FILTER NOT EXISTS {{ ?t rdfs:subClassOf* ?upper_class . }} }}"
    else:
        query_string += f"?t rdfs:subClassOf* ?upper_class . }}"

    return kg.query(
        query_string,
        initBindings={
            "entity": URIRef(entity_iri),
            "upper_class": upper_class_uri_ref,
        },
    )


def query_top_level_task_iri(kg: Graph, task_iri: str, namespace_prefix: str) -> query.Result:
    """
    Queries the knowledge graph to find the top-level task for a given task.

    Args:
        kg (Graph): The knowledge graph to query.
        task_iri (str): The IRI of the task.
        namespace_prefix (str): The namespace prefix used in the query.

    Returns:
        query.Result: The result of the query.
    """
    return kg.query(
        f"SELECT ?t2 WHERE {{ ?t1 rdfs:subClassOf* ?t2 ."
        f"                    ?t2 rdfs:subClassOf {namespace_prefix}:Task . "
        f"                    FILTER(?t2 != {namespace_prefix}:AtomicTask) . }}",
        initBindings={
            "t1": URIRef(task_iri),
        },
    )


def query_hierarchy_chain(kg: Graph, entity_iri: str) -> query.Result:
    """
    Queries the class hierarchy chain of a given entity in a knowledge graph.

    Args:
        kg (Graph): The knowledge graph to query.
        entity_iri (str): The IRI of the entity.

    Returns:
        query.Result: The result of the query.
    """
    return kg.query(
        f"SELECT ?m2 WHERE {{ ?m1 rdfs:subClassOf+ ?m2 . }}",
        initBindings={
            "m1": URIRef(entity_iri),
        },
    )


def query_module_iri_by_method_iri(
    kg: Graph,
    method_iri: str,
    namespace_prefix: str,
) -> query.Result:
    """
    Queries the knowledge graph to retrieve the module IRI associated with a given method IRI.

    Args:
        kg (Graph): The Knowledge Graph to query.
        method_iri (str): The IRI of the method.
        namespace_prefix (str): The namespace prefix used in the query.

    Returns:
        query.Result: The result of the query.
    """
    return kg.query(
        f"SELECT ?module WHERE {{ ?method rdfs:subClassOf ?module . "
        f"                        ?module rdfs:subClassOf+ {namespace_prefix}:Module . "
        f"                        FILTER NOT EXISTS {{ ?module rdfs:subClassOf+ {namespace_prefix}:Method . }} . }}",
        initBindings={"method": URIRef(method_iri)},
    )


def query_data_entity_reference_iri(kg: Graph, namespace_prefix, entity_iri: str) -> query.Result:
    """
    Queries the knowledge graph for the reference IRIs associated with a given entity.

    Args:
        kg (Graph): The knowledge graph to query.
        namespace_prefix (str): The namespace prefix used in the query.
        entity_iri (str): The IRI of the entity to query.

    Returns:
        query.Result: The result of the query.
    """
    return kg.query(
        f"SELECT ?r WHERE {{ ?entity {namespace_prefix}:hasReference ?r . }}",
        initBindings={
            "entity": URIRef(entity_iri),
        },
    )


def query_method_iri_by_task_iri(kg: Graph, namespace_prefix, task_iri: str) -> query.Result:
    """
    Queries the method IRI associated with a given task IRI.

    Args:
        kg (Graph): The RDF graph to query.
        namespace_prefix (str): The namespace prefix for the method property.
        task_iri (str): The IRI of the task.

    Returns:
        query.Result: The result of the query.
    """
    return kg.query(
        f"SELECT ?m WHERE {{ ?task ?m_property ?m ."
        f"                   ?m_property rdfs:subPropertyOf* {namespace_prefix}:hasMethod .}}",
        initBindings={"task": URIRef(task_iri)},
    )


def query_linked_task_and_property(kg: Graph, namespace_prefix, method_iri: str) -> query.Result:
    """
    Queries the linked task and linking property based on the given method IRI.

    Args:
        kg (Graph): The RDF graph to query.
        namespace_prefix (str): The namespace prefix for the AtomicTask.
        method_iri (str): The IRI of the method.

    Returns:
        query.Result: The result of the query.
    """
    return kg.query(
        f"SELECT ?task WHERE {{ ?task ?m_property ?m ."
        f"                      ?task rdfs:subPropertyOf* {namespace_prefix}:AtomicTask .}}",
        initBindings={"m": URIRef(method_iri)},
    )


def get_first_query_result_if_exists(query_method: Callable, *args) -> Optional[str]:
    """
    Executes the given query method with the provided arguments and returns the first result if it exists.

    Args:
        query_method (Callable): The query method to execute.
        *args: Variable number of arguments to pass to the query method.

    Returns:
        Optional[str]: The first query result if it exists, otherwise None.
    """
    query_result = next(
        iter(list(query_method(*args))),
        None,
    )

    if query_result is None:
        return None

    return query_result


def query_method_params(method_iri: str, namespace_prefix: str, kg: Graph) -> query.Result:
    """
    Queries the parameters and their ranges for a given method IRI.

    Args:
        method_iri (str): The IRI (Internationalized Resource Identifier) of the method.
        namespace_prefix (str): The namespace prefix used in the knowledge graph.
        kg (Graph): The knowledge graph to query.

    Returns:
        query.Result: The result of the query, containing the parameters of the method.
    """
    return kg.query(
        f"\nSELECT ?p ?r WHERE {{?p rdfs:domain ?task_iri . "
        f"?p rdfs:range ?r . "
        f"?p rdfs:subPropertyOf {namespace_prefix}:hasParameter . }}",
        initBindings={"task_iri": URIRef(method_iri)},
    )


def query_method_params_plus_inherited(
    method_iri: str, namespace_prefix: str, kg: Graph, inherited=False
) -> query.Result:
    """
    Queries the parameters and their ranges for a given method IRI, including inherited parameters.

    Args:
        method_iri (str): The IRI of the method.
        namespace_prefix (str): The namespace prefix for the `hasParameter` property.
        kg (Graph): The RDF graph to query.

    Returns:
        query.Result: The result of the query.
    """
    if inherited:
        return kg.query(
            f"\nSELECT ?p ?r WHERE {{?p rdfs:domain ?domain . "
            f"?method_iri rdfs:subClassOf* ?domain . "
            f"?p rdfs:range ?r . "
            f"?p rdfs:subPropertyOf {namespace_prefix}:hasParameter . }}",
            initBindings={"method_iri": URIRef(method_iri)},
        )

    return kg.query(
        f"\nSELECT ?p ?r WHERE {{?p rdfs:domain ?method_iri . "
        f"?p rdfs:range ?r . "
        f"?p rdfs:subPropertyOf {namespace_prefix}:hasParameter . }}",
        initBindings={"method_iri": URIRef(method_iri)},
    )


def query_method_properties_and_methods(input_kg: Graph, namespace_prefix: str, entity_parent_iri: str) -> query.Result:
    """
    Queries the input knowledge graph for methods and the properties that connect them to the given entity.

    Args:
        input_kg (Graph): The input knowledge graph to query.
        namespace_prefix (str): The namespace prefix used in the query.
        entity_parent_iri (str): The IRI of the parent entity.

    Returns:
        query.Result: The result of the query.
    """
    return input_kg.query(
        "\nSELECT ?p ?m WHERE {?p rdfs:domain ?entity_iri . "
        "?p rdfs:range ?m . "
        "?m rdfs:subClassOf " + namespace_prefix + ":AtomicMethod . }",
        initBindings={"entity_iri": URIRef(entity_parent_iri)},
    )


def query_inherited_inputs(input_kg: Graph, namespace_prefix: str, entity_iri: str) -> query.Result:
    """
    Queries the input knowledge graph to find (inherited) inputs, their structure and the properties that connect them to the given entity.

    Args:
        input_kg (Graph): The input knowledge graph.
        namespace_prefix (str): The namespace prefix used in the SPARQL query.
        entity_iri (str): The IRI of the entity for which inherited inputs are to be found.

    Returns:
        query.Result: The result of the SPARQL query.

    """
    return input_kg.query(
        "\nSELECT ?m ?s ?p WHERE {?entity_iri rdfs:subClassOf* ?parent . "
        "?p rdfs:domain ?parent ."
        "?p rdfs:range ?m ."
        "?p rdfs:subPropertyOf+ " + namespace_prefix + ":hasInput ."
        "OPTIONAL { ?m rdfs:subClassOf ?s . }"
        "OPTIONAL { ?s rdfs:subClassOf+ " + namespace_prefix + ":DataStructure . }"
        "FILTER(?s != " + namespace_prefix + ":DataEntity) . }",
        initBindings={"entity_iri": URIRef(entity_iri)},
    )


def query_inherited_outputs(input_kg: Graph, namespace_prefix: str, entity_iri: str) -> query.Result:
    """
    Queries the input knowledge graph to find (inherited) outputs, their structure and the properties that connect them to the given entity.

    Args:
        input_kg (Graph): The input knowledge graph.
        namespace_prefix (str): The namespace prefix used in the SPARQL query.
        entity_iri (str): The IRI of the entity for which inherited inputs are to be found.

    Returns:
        query.Result: The result of the SPARQL query.

    """
    return input_kg.query(
        "\nSELECT ?m ?s ?p WHERE {?entity_iri rdfs:subClassOf* ?parent . "
        "?p rdfs:domain ?parent ."
        "?p rdfs:range ?m ."
        "?p rdfs:subPropertyOf+ " + namespace_prefix + ":hasOutput ."
        "?m rdfs:subClassOf ?s ."
        "?s rdfs:subClassOf+ " + namespace_prefix + ":DataStructure . "
        "FILTER(?s != " + namespace_prefix + ":DataEntity) . }",
        initBindings={"entity_iri": URIRef(entity_iri)},
    )


def query_pipeline_info(kg: Graph, namespace_prefix: str) -> query.Result:
    """
    Queries the knowledge graph for pipeline information.

    Args:
        kg (Graph): The knowledge graph to query.
        namespace_prefix (str): The namespace prefix used in the query.

    Returns:
        query.Result: The result of the query.

    """
    return kg.query(
        f"\nSELECT ?p ?i ?o ?t WHERE {{?p rdf:type {namespace_prefix}:Pipeline ;"
        f"                          {namespace_prefix}:hasInputDataPath ?i ;"
        f"                          {namespace_prefix}:hasPlotsOutputDir ?o ;"
        f"                          {namespace_prefix}:hasStartTask ?t . }}"
    )


def query_subclasses_of(class_iri: str, kg: Graph) -> query.Result:
    """
    Queries the knowledge graph to retrieve the subclasses of a given class.

    Args:
        class_iri (str): The IRI of the class.
        kg (Graph): The knowledge graph to query.

    Returns:
        query.Result: The result of the query.
    """
    return kg.query(
        "\nSELECT ?t WHERE {?t rdfs:subClassOf ?class_iri . }",
        initBindings={"class_iri": class_iri},
    )


def query_input_triples(kg: Graph, namespace_prefix: str, entity_iri: str) -> query.Result:
    """
    Queries the triples that connect the given entity with its inputs.

    Args:
        kg (Graph): The knowledge graph to query.
        namespace_prefix (str): The namespace prefix used in the query.
        entity_iri (str): The IRI of the entity to query input triples for.

    Returns:
        query.Result: The result of the query.
    """
    return kg.query(
        f"""
        SELECT DISTINCT ?s ?p ?o
        WHERE {{
            {{ ?s ?p ?o . FILTER(?p = {namespace_prefix}:hasInput) }}
            UNION
            {{ ?s ?p ?o . ?p rdfs:subPropertyOf* {namespace_prefix}:hasInput . }}
        }}
        """,
        initBindings={"s": URIRef(entity_iri)},
    )


def query_output_triples(kg: Graph, namespace_prefix: str, entity_iri: str) -> query.Result:
    """
    Queries the triples that connect the given entity with its outputs.

    Args:
        kg (Graph): The knowledge graph to query.
        namespace_prefix (str): The namespace prefix used in the query.
        entity_iri (str): The IRI of the entity to query input triples for.

    Returns:
        query.Result: The result of the query.
    """
    return kg.query(
        f"""
        SELECT DISTINCT ?s ?p ?o
        WHERE {{
            {{ ?s ?p ?o . FILTER(?p = {namespace_prefix}:hasOutput) }}
            UNION
            {{ ?s ?p ?o . ?p rdfs:subPropertyOf* {namespace_prefix}:hasOutput . }}
        }}
        """,
        initBindings={"s": URIRef(entity_iri)},
    )


def query_parameters_triples(kg: Graph, namespace_prefix: str, entity_iri: str) -> query.Result:
    """
    Queries the triples that connect the given entity with its parameters.

    Args:
        kg (Graph): The knowledge graph to query.
        namespace_prefix (str): The namespace prefix used in the query.
        entity_iri (str): The IRI of the entity to query input triples for.

    Returns:
        query.Result: The result of the query.
    """
    return kg.query(
        f"""
        SELECT ?s ?p ?o
        WHERE {{
            {{ ?s ?p ?o . ?p rdfs:subPropertyOf* {namespace_prefix}:hasParameter . }}
        }}
        """,
        initBindings={"s": URIRef(entity_iri)},
    )


def get_pipeline_and_first_task_iri(kg: Graph, namespace_prefix: str) -> Tuple[str, str, str]:
    """
    Retrieves the pipeline and first task IRI from the knowledge graph.

    Args:
        kg (Graph): The knowledge graph to query.
        namespace_prefix (str): The namespace prefix used in the KG.

    Returns:
        Tuple[str, str, str]: A tuple containing the pipeline IRI, input data path, plots output directory, and task IRI.

    Raises:
        NoResultsError: If the pipeline info is not found in the KG.
    """

    # assume one pipeline per file
    query_result = get_first_query_result_if_exists(
        query_pipeline_info,
        kg,
        namespace_prefix,
    )
    if query_result is None:
        raise NoResultsError("Pipeline info not found in the KG")

    pipeline_iri, input_data_path, plots_output_dir, task_iri = query_result

    return str(pipeline_iri), str(input_data_path), str(plots_output_dir), str(task_iri)


def get_method_by_task_iri(
    kg: Graph,
    namespace_prefix: str,
    namespace: Namespace,
    task_iri: str,
) -> Optional[Method]:
    """
    Retrieves the method associated with a given task IRI from the knowledge graph.

    Args:
        kg (Graph): The knowledge graph.
        namespace_prefix (str): The namespace prefix.
        namespace (Namespace): The namespace.
        task_iri (str): The IRI of the task.

    Returns:
        Optional[Method]: The method object associated with the task IRI, or None if no method is found.

    Raises:
        NoResultsError: If the task with the given IRI is not connected with any method in the KG.
        NoResultsError: If the method with the retrieved IRI doesn't have a type that is a subclass of `namespace.AtomicMethod`.
    """

    query_result = get_first_query_result_if_exists(
        query_method_iri_by_task_iri,
        kg,
        namespace_prefix,
        task_iri,
    )
    if query_result is None:
        raise NoResultsError(f"Task with IRI {task_iri} isn't connected with any method in the KG")

    method_iri = str(query_result[0])

    query_result = get_first_query_result_if_exists(
        query_instance_parent_iri,
        kg,
        method_iri,
        namespace.AtomicMethod,
    )

    if query_result is None:
        raise NoResultsError(
            f"Method with IRI {method_iri} doesn't have a type that is a subclass of {str(namespace.AtomicMethod)}"
        )

    method_parent_iri = str(query_result[0])

    return Method(method_iri, Entity(method_parent_iri))


def get_module_hierarchy_chain(
    kg: Graph,
    namespace_prefix: str,
    method_iri: str,
) -> List:
    """
    Retrieves the hierarchy chain of the modules starting from the module connected to the given method IRI.

    Args:
        kg (Graph): The knowledge graph.
        namespace_prefix (str): The namespace prefix of the module.
        method_iri (str): The IRI of the method.

    Returns:
        List: The hierarchy chain of the module, represented as a list of module names.

    Raises:
        NoResultsError: If the method doesn't have a subclass that is a subclass of {namespace_prefix}:Module.
    """

    query_result = get_first_query_result_if_exists(
        query_module_iri_by_method_iri,
        kg,
        method_iri,
        namespace_prefix,
    )

    if query_result is None:
        raise NoResultsError(
            f"Method with IRI {method_iri} doesn't have a subclass that is subclass of {namespace_prefix}:Module"
        )

    module_iri = str(query_result[0])
    module_chain_query_res = list(query_hierarchy_chain(kg, module_iri))
    module_chain_query_res = [str(x[0]) for x in module_chain_query_res]
    module_chain_iris = [module_iri] + module_chain_query_res[:-1]
    module_chain_names = [iri.split("#")[-1] for iri in module_chain_iris]

    return module_chain_names


def get_converted_module_hierarchy_chain(
    kg: Graph,
    namespace_prefix: str,
    method_iri: str,
) -> List:
    """
    Retrieves the module hierarchy chain for a given method IRI and converts it to a list of module names.

    Args:
        kg (Graph): The knowledge graph to query.
        namespace_prefix (str): The namespace prefix to use in queries.
        method_iri (str): The IRI of the method.

    Returns:
        List: The list of module names in the module hierarchy chain, in the correct order.
    """
    module_chain_names = None
    try:
        module_chain_names = get_module_hierarchy_chain(kg, namespace_prefix, method_iri)
    except NoResultsError:
        print(f"Cannot retrieve module chain for method class: {method_iri}. Proceeding without it...")

    if module_chain_names:
        # convert KG class names to module names and reverse the module chain to store it in the correct order
        module_chain_names = [class_name_to_module_name(name) for name in module_chain_names]
        module_chain_names = [class_name_to_method_name(method_iri.split("#")[-1])] + module_chain_names
        module_chain_names.reverse()

    return module_chain_names


def get_method_grouped_params(
    method_iri: str, namespace_prefix: str, kg: Graph, inherited: bool = False
) -> List[Tuple[str, List[str]]]:
    """
    Retrieves the (inherited) parameters for a given method, grouped by property IRI.

    Args:
        method_iri (str): The IRI of the method.
        namespace_prefix (str): The namespace prefix.
        kg (Graph): The knowledge graph.

    Returns:
        List[Tuple[str, List[str]]]: A list of tuples, where each tuple contains a parameter name and a list of its values.
    """
    property_list = list(query_method_params_plus_inherited(method_iri, namespace_prefix, kg, inherited))
    property_list = sorted(property_list, key=lambda elem: elem[0])  # prepare for grouping
    property_list = [
        (key, [pair[1] for pair in group]) for key, group in itertools.groupby(property_list, lambda elem: elem[0])
    ]

    return property_list


def get_grouped_inherited_inputs(
    input_kg: Graph, namespace_prefix: str, entity_iri: str
) -> List[Tuple[str, List[str]]]:
    """
    Retrieves the inherited inputs for a given entity, grouped by data entity IRI.

    Args:
        input_kg (Graph): The input knowledge graph.
        namespace_prefix (str): The namespace prefix for the entity.
        entity_iri (str): The IRI of the entity.

    Returns:
        List[Tuple[str, List[str]]]: A list of tuples, where each tuple contains a property name and a list of input values.

    """
    property_list = list(query_inherited_inputs(input_kg, namespace_prefix, entity_iri))
    property_list = sorted(property_list, key=lambda elem: elem[0])  # prepare for grouping
    property_list = [
        (key, [(elem[1], elem[2]) for elem in group])
        for key, group in itertools.groupby(property_list, key=lambda elem: elem[0])
    ]

    return property_list


def get_grouped_inherited_outputs(
    input_kg: Graph, namespace_prefix: str, entity_iri: str
) -> List[Tuple[str, List[str]]]:
    """
    Retrieves the inherited outputs for a given entity, grouped by data entity IRI.

    Args:
        input_kg (Graph): The input knowledge graph.
        namespace_prefix (str): The namespace prefix for the entity.
        entity_iri (str): The IRI of the entity.

    Returns:
        List[Tuple[str, List[str]]]: A list of tuples, where each tuple contains a property name and a list of input values.
    """
    property_list = list(query_inherited_outputs(input_kg, namespace_prefix, entity_iri))
    property_list = sorted(property_list, key=lambda elem: elem[0])  # prepare for grouping
    property_list = [
        (key, [(elem[1], elem[2]) for elem in group])
        for key, group in itertools.groupby(property_list, key=lambda elem: elem[0])
    ]

    return property_list
