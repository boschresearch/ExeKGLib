# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from abc import abstractmethod
from typing import Dict, Union

import pandas as pd

from exe_kg_lib.classes.data_entity import DataEntity
from exe_kg_lib.classes.method import Method

from .entity import Entity


class Task(Entity):
    """
    Abstraction of owl:class ds:AtomicTask.

    ❗ Important for contributors: See Section "Naming conventions" in README.md of "classes.tasks" package before extending the code's functionality.
    """

    def __init__(
        self,
        iri: str,
        parent_entity: Entity = None,
    ):
        super().__init__(iri, parent_entity)
        self.next_task = None  # used for storing the next Task in the pipeline
        self.method = None  # used for storing the method of the Task
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

    def get_inputs(
        self, dict_to_search: dict, fallback_df: pd.DataFrame
    ) -> Dict[str, Dict[str, Union[pd.DataFrame, Method]]]:
        """
        For each input of the Task:
            - If the input is a DataEntity: Searches for the input reference name in dict_to_search. If not found, uses fallback_df.
            - If the input is a Method: Uses the input type as the input name and the input itself as the input value.

        Args:
            dict_to_search: contains key-value pairs where key is a possible input name and value is its corresponding value
            fallback_df: contains data to return as an alternative

        Returns:
            Dict[str, Dict[str, Union[pd.DataFrame, Method]]]: dictionary with input types as keys and dictionaries with input names and values as values
        """
        input_dict = {}
        inputs_sorted = sorted(self.inputs, key=lambda x: x.name)
        for input in inputs_sorted:
            if input.type not in input_dict:
                input_dict[input.type] = []
            if isinstance(input, DataEntity):
                input_name = input.reference
                try:
                    input_value = dict_to_search[input.reference]
                except KeyError:
                    input_value = fallback_df.loc[:, [input.source]]
            elif isinstance(input, Method):
                input_name = input.type
                input_value = input

            input_dict[input.type].append({"name": input_name, "value": input_value})

        return input_dict

    @abstractmethod
    def run_method(self, *args):
        """
        Abstract method to be implemented by Task sub-classes that are in the bottom of the hierarchy.
        Executes the logic that is needed to fulfill the Task.
        Args:
            *args: defined by sub-classes
        """
        raise NotImplementedError
