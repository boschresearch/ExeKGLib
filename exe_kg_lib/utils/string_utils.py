# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

import re


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


def property_name_to_field_name(property_name: str) -> str:
    """
    Extracts property name from IRI and converts it to snake-case
    Args:
        property_name: IRI to parse

    Returns:
        str: converted string
    """
    return camel_to_snake(property_name.split("#")[1])
