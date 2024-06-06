# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from pathlib import Path
from typing import Union

import rdflib
from pyshacl import validate

HERE = Path(__file__).parent


class KGValidationError(Exception):
    pass


def check_kg_executability(kg: Union[rdflib.Graph, str], shacl_shapes_s: str) -> None:
    """
    Checks the executability of a KG by validating it against a set of SHACL shapes.

    Args:
        kg (Union[rdflib.Graph, str]): The KG to be validated. It can be either an rdflib.Graph object or a string representing the path to the KG file.
        shacl_shapes_s (str): The SHACL shapes to validate the KG against.

    Raises:
        KGValidationError: If the KG is not executable, an exception is raised with an error message.

    Returns:
        None: This function does not return any value.
    """
    r = validate(data_graph=kg, shacl_graph=shacl_shapes_s)
    conforms, _, results_text = r
    if not conforms:
        raise KGValidationError(
            f"{results_text}\n\nThe KG is not executable. To ensure executability of the KG as an ML pipeline, please fix the above error(s) and try again."
        )
    return
