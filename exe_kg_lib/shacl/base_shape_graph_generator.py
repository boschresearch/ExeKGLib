# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

"""
This script produces a SHACL shape graph based on the KG schemata and the generated KGs that represent the example pipelines.

NOTE: The shape graph produced by this script is NOT identical to "shacl_shape_graph.ttl" because the latter has been adapted to the special cases of ExeKGLib.
"""

from shexer.consts import SHACL_TURTLE, TURTLE
from shexer.shaper import Shaper

EXAMPLE_PIPELINES_PATH = "https://raw.githubusercontent.com/boschresearch/ExeKGLib/main/examples/pipelines/"
KG_SCHEMATA_PATH = "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/"

NAMESPACES_DICT = {
    "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/ds_exeKGOntology.ttl#": "ds",
    "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/visu_exeKGOntology.ttl#": "visu",
    "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/stats_exeKGOntology.ttl#": "stats",
    "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/ml_exeKGOntology.ttl#": "ml",
    "http://www.w3.org/2001/XMLSchema#": "xsd",
    "http://www.w3.org/2000/01/rdf-schema#": "rdfs",
    "http://www.w3.org/XML/1998/namespace": "xml",
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
    "http://www.w3.org/2002/07/owl#": "owl",
}

shaper = Shaper(
    graph_list_of_files_input=[
        KG_SCHEMATA_PATH + "ds_exeKGOntology.ttl",
        KG_SCHEMATA_PATH + "visu_exeKGOntology.ttl",
        KG_SCHEMATA_PATH + "stats_exeKGOntology.ttl",
        KG_SCHEMATA_PATH + "ml_exeKGOntology.ttl",
        EXAMPLE_PIPELINES_PATH + "MLPipeline.ttl",
        EXAMPLE_PIPELINES_PATH + "StatsPipeline.ttl",
        EXAMPLE_PIPELINES_PATH + "MLPipeline.ttl",
    ],
    input_format=TURTLE,
    namespaces_dict=NAMESPACES_DICT,
    all_classes_mode=True,
)

shaper.shex_graph(output_file="base_schacl_shape_graph.ttl", acceptance_threshold=0.1, output_format=SHACL_TURTLE)

print("Done!")
