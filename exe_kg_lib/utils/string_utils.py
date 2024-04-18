# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

import re
from pathlib import Path
from typing import Union


def camel_to_snake(text: str) -> str:
    """
    Converts camel-case string to snake-case
    Args:
        text: string to convert

    Returns:
        str: converted string
    """
    text = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", text)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", text).lower()


def property_iri_to_field_name(property_name: str) -> str:
    """
    Extracts property name from IRI and converts it to a Python field name
    Args:
        property_name: IRI to parse

    Returns:
        str: converted string
    """
    snake_case = camel_to_snake(property_name.split("#")[1])
    return snake_case.replace("has_", "").replace("param_", "")


def class_name_to_module_name(class_name: str):
    """
    Converts a class name to a module name by removing the "Module" suffix and converting it to snake case.

    Args:
        class_name (str): The class name to convert.

    Returns:
        str: The converted module name.
    """
    name = re.sub("Module$", "", class_name)
    return camel_to_snake(name)


def class_name_to_method_name(class_name: str):
    """
    Converts a class name to a method name by removing the word "Method" from the end of the class name.

    Args:
        class_name (str): The class name to convert.

    Returns:
        str: The converted method name.
    """
    name = re.sub("Method$", "", class_name)
    return name


def concat_paths(*paths: Union[str, Path]) -> str:
    """
    Concatenates multiple paths into a single path.

    Args:
        *paths: Variable number of paths to be concatenated.

    Returns:
        str: The concatenated path.

    Example:
        >>> concat_paths('path1', 'path2', 'path3')
        'path1/path2/path3'
    """
    output_path = ""
    for path in paths:
        if not output_path:
            output_path = path
        else:
            output_path = (
                output_path / path
                if isinstance(output_path, Path) or isinstance(path, Path)
                else f"{output_path}/{path}"
            )

    return str(output_path)
