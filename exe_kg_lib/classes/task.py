# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

import importlib
from abc import abstractmethod
from typing import Any, Dict

import numpy as np
import pandas as pd

from exe_kg_lib.utils.string_utils import camel_to_snake

from .entity import Entity


class Task(Entity):
    """
    Abstraction of owl:class ds:Task.

    ❗ Important for contributors: See Section "Naming conventions" in README.md of "classes.tasks" package before extending the code's functionality.
    """

    def __init__(
        self,
        iri: str,
        parent_entity: Entity = None,
    ):
        super().__init__(iri, parent_entity)
        self.next_task = None
        self.method_module_chain = (
            []
        )  # e.g. ['sklearn','model_selection', 'StratifiedShuffleSplit'] Used for resolving the Python module that contains the method to be executed
        self.method_params_dict = {}  # used for storing method parameters during KG execution
        self.method_inherited_params_dict = {}  # used for storing inherited method parameters during KG execution
        self.inputs = []  # used for storing input DataEntity objects during KG execution
        self.outputs = []  # used for storing output DataEntity objects during KG execution
        self.input_dict = {}  # used for storing input DataEntity objects during KG creation
        self.output_dict = {}  # used for storing output DataEntity objects during KG creation

    @classmethod
    def from_entity(cls, entity: Entity):
        return cls(entity.iri, entity.parent_entity)

    def create_output_dict(self, keyword_value_dict: dict) -> dict:
        """
        For each key in keyword_value_dict, checks if the key exists in an output name of the Task.
        If yes, adds the output name with its value to out_dict.
        Args:
            keyword_value_dict: key-value pairs where key is a keyword to find in an output name of the Task
                                  and value is the value corresponding to that output name

        Returns:
            dict: pairs of Task's output names and corresponding output values
        """
        if len(self.outputs) == 0:
            # assume one output and use task name as key
            return {self.name: list(keyword_value_dict.values())[0]}

        output_names = [has_output_elem.name for has_output_elem in self.outputs]
        out_dict = {}
        for output_name in output_names:
            for key, value in keyword_value_dict.items():
                if key in output_name:
                    out_dict[output_name] = value

        return out_dict

    def get_inputs(self, dict_to_search: dict, fallback_df: pd.DataFrame) -> Dict[str, Dict[str, pd.DataFrame]]:
        """
        Tries to match the Task's input reference names with the keys of dict_to_search and fills input_dict list with their names and values.
        If the matching fail, it retrieves columns of the provided fallback_df
        Args:
            dict_to_search: contains key-value pairs where key is a possible input name and value is its corresponding value
            fallback_df: contains data to return as an alternative

        Returns:
            Dict[str, Dict[str, pd.DataFrame]]: dictionary with input types as keys and dictionaries with input reference names and values as values
        """
        input_dict = {}
        inputs_sorted = sorted(self.inputs, key=lambda x: x.name)
        for input in inputs_sorted:
            if input.type not in input_dict:
                input_dict[input.type] = []

            try:
                input_value = dict_to_search[input.reference]
            except KeyError:
                input_value = fallback_df.loc[:, [input.source]]

            input_dict[input.type].append({"name": input.reference, "value": input_value})

        return input_dict

    def resolve_module(self, module_name_to_snakecase=False) -> Any:
        """
        Resolves and returns the Python module specified by the method module chain.

        Args:
            module_name_to_snakecase (bool, optional): Whether to convert the last module name to snake case.
                                                      Defaults to False.

        Returns:
            Any: The resolved module.

        Raises:
            NotImplementedError: If the method module chain is not defined for the task.
        """
        if not self.method_module_chain:
            raise NotImplementedError(f"Method module chain not defined for task {self.name}.")

        method_module_chain = self.method_module_chain
        if module_name_to_snakecase:
            method_module_chain = self.method_module_chain[:-1] + [camel_to_snake(self.method_module_chain[-1])]

        method_module_chain_parents = ".".join(method_module_chain[:-1])
        method_module_chain_child = method_module_chain[-1]
        module_container = importlib.import_module(method_module_chain_parents)
        module = getattr(module_container, method_module_chain_child)
        return module

    @abstractmethod
    def run_method(self, *args):
        """
        Abstract method to be implemented by Task sub-classes that are in the bottom of the hierarchy.
        Executes the logic that is needed to fulfill the Task.

        Args:
            *args: defined by sub-classes
        """
        raise NotImplementedError
