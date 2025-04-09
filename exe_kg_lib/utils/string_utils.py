# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

import re
from pathlib import Path
from typing import Union

# example output name: "DataOutNameEx_TaskTypeEx1_PipelineName_MethodEx"
# - "DataOutNameEx" is the name of the output data entity.
# - "TaskTypeEx" is a placeholder for the type of the task that produced the output.
# - "1" represents the number of the instance for a task type in the pipeline.
# - "PipelineName" is the name of the pipeline.
# - "MethodEx" is a placeholder for the type of the method that produced the output.
TASK_OUTPUT_NAME_REGEX = r"(.*)_(.*)(\d)_(.*)_(.*)"


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
    snake_case = re.sub("^has_", "", snake_case)
    snake_case = re.sub("^param_", "", snake_case)
    return snake_case


def class_name_to_module_name(class_name: str) -> str:
    """
    Converts a class name to a module name by removing the "Module" suffix and converting it to snake case.

    Args:
        class_name (str): The class name to convert.

    Returns:
        str: The converted module name.
    """
    name = re.sub("Module$", "", class_name)
    return camel_to_snake(name)


def class_name_to_method_name(class_name: str) -> str:
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


def get_instance_name(instance_type: str, instance_number: int, pipeline_name: str) -> str:
    """
    Generates a unique instance name based on the instance type and number.

    Args:
        instance_type (str): The type of the instance.
        instance_number (int): The number of the instance for this type.
        pipeline_name (str): The name of the pipeline.

    Returns:
        str: The generated instance name.
    """
    return f"{instance_type}{str(instance_number)}_{pipeline_name}"


def get_task_output_name(output_type: str, task_instance_name: str, method_type: str) -> str:
    """
    Generates the name for a task's output based on the output type, task instance name, and method type.

    Args:
        output_type (str): The type of the output.
        task_instance_name (str): The name of the task instance.
        method_type (str): The type of the method.

    Returns:
        str: The generated task output name that follows the format "DataOutNameEx_TaskTypeEx1_PipelineName_MethodEx" (see TASK_OUTPUT_NAME_REGEX above for details).
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
        task_name = match.group(2)
        task_instance_number = match.group(3)
        method_type = match.group(5)

        return f"{task_name}{task_instance_number} {method_type} {task_output_name}"

    return data_entity_name
