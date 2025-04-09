# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from typing import Dict, Union

from rdflib import Graph, Namespace, URIRef

from exe_kg_lib.utils.kg_creation_utils import field_value_to_literal


def update_metric_values(
    exe_kg: Graph,
    task_output_dict: Dict[str, Union[str, int, float, bool]],
    bottom_level_namespace: Namespace,
    top_level_namespace: Namespace,
) -> None:
    """
    Updates the metric values in the given ExeKG.

    Args:
        exe_kg (Graph): The knowledge graph to update.
        task_output_dict (Dict[str, Union[str, int, float, bool]]): A dictionary containing the task output names and values.
        bottom_level_namespace (Namespace): The bottom level namespace for the output entity IRI.
        top_level_namespace (Namespace): The top level namespace for the hasValue property.

    Returns:
        None
    """
    for task_output_name, task_output_value in task_output_dict.items():
        if "DataOutScore" in task_output_name:
            output_entity_iri = URIRef(bottom_level_namespace + task_output_name)
            exe_kg.remove(
                (
                    output_entity_iri,
                    URIRef(top_level_namespace.hasValue),
                    None,
                )
            )
            exe_kg.add(
                (
                    output_entity_iri,
                    URIRef(top_level_namespace.hasValue),
                    field_value_to_literal(task_output_value),
                )
            )


def update_pipeline_input_path(
    exe_kg: Graph,
    pipeline_iri: Union[str, URIRef],
    new_input_data_path: str,
    top_level_namespace: Namespace,
) -> None:
    """
    Updates the input data path of a pipeline in the given ExeKG.

    Args:
        exe_kg (Graph): The knowledge graph to update.
        pipeline_iri (Union[str, URIRef]): The IRI of the pipeline to update.
        new_input_data_path (str): The new input data path to set for the pipeline.
        top_level_namespace (Namespace): The namespace containing the relevant RDF predicates.

    Returns:
        None
    """
    exe_kg.remove(
        (
            URIRef(pipeline_iri),
            URIRef(top_level_namespace.hasInputDataPath),
            None,
        )
    )
    exe_kg.add(
        (
            URIRef(pipeline_iri),
            URIRef(top_level_namespace.hasInputDataPath),
            field_value_to_literal(new_input_data_path),
        )
    )
