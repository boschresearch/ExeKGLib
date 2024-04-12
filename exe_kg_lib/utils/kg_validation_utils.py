import os
from typing import Union

import rdflib
from pyshacl import validate

CURRENT_DIR = os.path.dirname(__file__)
SHACL_SHAPE_GRAPH_PATH = os.path.join(CURRENT_DIR, "..", "shacl", "shacl_shape_graph.ttl")


class KGValidationError(Exception):
    pass


def check_kg_executability(kg: Union[rdflib.Graph, str]) -> None:
    """Checks if the given KG is executable as an ML pipeline, based on a pre-defined SHACL shape graph

    Args:
        kg (rdflib.Graph or str): object or path of graph to check
    """
    r = validate(data_graph=kg, shacl_graph=SHACL_SHAPE_GRAPH_PATH)
    conforms, _, results_text = r
    if not conforms:
        print(results_text)
        raise KGValidationError(
            "The KG is not executable. To ensure executability of the KG as an ML pipeline, please fix the above error(s) and try again."
        )
    return
