# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

import re
from pathlib import Path
from typing import Union

TASK_OUTPUT_NAME_REGEX = r"(.*)_(.*)(\d)_(.*)"  # example: DataOutNameEx_TaskEx1_MethodEx


def camel_to_snake(text: str) -> str:
    """
    Converts a camel case string to snake case.

    Args:
        text (str): The camel case string to be converted.

    Returns:
        str: The snake case version of the input string.
    """
    text = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", text)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", text).lower()


def property_iri_to_field_name(property_iri: str) -> str:
    """
    Converts a property IRI to a Python field name.

    Args:
        property_iri (str): The property IRI.

    Returns:
        str: The converted field name.
    """
    snake_case = camel_to_snake(property_iri.split("#")[1])
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


def get_instance_name(instance_type: str, instance_count: int) -> str:
    """
    Generates a unique instance name based on the instance type and count.

    Args:
        instance_type (str): The type of the instance.
        instance_count (int): The count of the instance.

    Returns:
        str: The generated instance name.
    """
    return f"{instance_type}{str(instance_count)}"


def get_task_output_name(output_type: str, task_instance_name: str, method_type: str) -> str:
    """
    Generates the name for a task's output based on the output type, task instance name, and method type.

    Args:
        output_type (str): The type of the output.
        task_instance_name (str): The name of the task instance.
        method_type (str): The type of the method.

    Returns:
        str: The generated task output name.
    """
    return f"{output_type}_{task_instance_name}_{method_type}"


def prettify_data_entity_name(data_entity_name: str) -> str:
    """
    Prettifies the given data entity name by removing unnecessary prefixes and components.

    Args:
        data_entity_name (str): The name of the data entity.

    Returns:
        str: The prettified data entity name.
    """
    match = re.match(TASK_OUTPUT_NAME_REGEX, data_entity_name)
    if match:
        # data_entity_name refers to a data entity that is an output of a previous task
        task_output_name = match.group(1)
        task_output_name = re.sub(r"^DataOut", "", task_output_name)
        method_type = match.group(4)

        return f"{method_type} {task_output_name}"

    return data_entity_name
