from pathlib import Path
from typing import Union

import rdflib
from pyshacl import validate

HERE = Path(__file__).parent


class KGValidationError(Exception):
    pass


def check_kg_executability(kg: Union[rdflib.Graph, str], shacl_shapes_s: str) -> None:
    """Checks if the given KG is executable as an ML pipeline, based on a pre-defined SHACL shape graph

    Args:
        kg (rdflib.Graph or str): object or path of graph to check
    """
    r = validate(data_graph=kg, shacl_graph=shacl_shapes_s)
    conforms, _, results_text = r
    if not conforms:
        print(results_text)
        raise KGValidationError(
            "The KG is not executable. To ensure executability of the KG as an ML pipeline, please fix the above error(s) and try again."
        )
    return
