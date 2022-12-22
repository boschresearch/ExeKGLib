import re


def camel_to_snake(name: str) -> str:
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def property_name_to_field_name(property_name: str) -> str:
    return camel_to_snake(property_name.split("#")[1])
