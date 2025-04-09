# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from typing import Dict, List, Union

from exe_kg_lib.classes.exe_kg_serialization.method import \
    Method as MethodSerializable


class Task:
    """
    Represents a simplified version of a pipeline's task for serialization purposes.
    """

    def __init__(
        self,
        kg_schema_short: str = "",
        task_type: str = "",
        method_type: str = "",
        method_params_dict: Dict[str, Union[str, int, float, dict]] = None,
        output_names: List[str] = None,
        input_entity_info_dict: Dict[str, Union[List[str], MethodSerializable]] = None,
    ):
        self.kg_schema_short = kg_schema_short
        self.task_type = task_type
        self.method_type = method_type

        if method_params_dict is None:
            method_params_dict = {}
        self.method_params_dict = method_params_dict

        if input_entity_info_dict is None:
            input_entity_info_dict = {}
        self.input_entity_info_dict = (
            input_entity_info_dict  # contains input names as keys and lists of data entity names as values
        )

        if output_names is None:
            output_names = []
        self.output_names = output_names

    @classmethod
    def from_dict(cls, task_dict: dict):
        return cls(
            kg_schema_short=task_dict["kg_schema_short"],
            task_type=task_dict["task_type"],
            method_type=task_dict["method_type"],
            method_params_dict=task_dict["method_params_dict"],
            input_entity_info_dict={
                input_name: (
                    MethodSerializable(input_value["method_type"], input_value["params_dict"])
                    if "method_type" in input_value and "params_dict" in input_value
                    else input_value
                )
                for input_name, input_value in task_dict["input_entity_info_dict"].items()
            },
            output_names=task_dict.get("output_names", None),
        )

    def to_dict(self):
        return {
            "kg_schema_short": self.kg_schema_short,
            "task_type": self.task_type,
            "method_type": self.method_type,
            "method_params_dict": self.method_params_dict,
            "input_entity_info_dict": {
                input_name: input_value.__dict__ if isinstance(input_value, MethodSerializable) else input_value
                for input_name, input_value in self.input_entity_info_dict.items()
            },
            "output_names": self.output_names,
        }
