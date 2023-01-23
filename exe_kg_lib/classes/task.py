# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from abc import abstractmethod
from typing import Dict

import numpy as np
import pandas as pd

from .entity import Entity


class Task(Entity):
    """
    Abstraction of owl:class Task.

    ❗ Important for contributors ❗
    The fields that contain "_" are by convention the snake-case conversions of the equivalent camel-case property names in the KG.
    e.g. has_next_task field corresponds to hasNextTask property in the KG.
    This is necessary for automatically mapping KG properties to Python object fields while parsing the KG.
    """

    def __init__(
        self,
        iri: str,
        parent_entity: Entity = None,
    ):
        super().__init__(iri, parent_entity)
        self.has_next_task = None
        self.has_method = None
        self.has_input = []
        self.has_output = []
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
        if len(self.has_output) == 0:
            # assume one output and use task name as key
            return {self.name: list(keyword_value_dict.values())[0]}

        output_names = [has_output_elem.name for has_output_elem in self.has_output]
        out_dict = {}
        for output_name in output_names:
            for key, value in keyword_value_dict.items():
                if key in output_name:
                    out_dict[output_name] = value

        return out_dict

    def get_inputs(self, dict_to_search: dict, fallback_df: pd.DataFrame) -> Dict[str, np.ndarray]:
        """
        Tries to match the Task's input names with the keys of dict_to_search
        and fills input_dict list with their corresponding values.
        If the matches fail, it retrieves columns of the provided fallback_df
        Args:
            dict_to_search: contains key-value pairs where key is a possible input name and value is its corresponding value
            fallback_df: contains data to return as an alternative

        Returns:
            Dict[str, np.ndarray]: pairs of input entity types and corresponding input values
        """
        input_dict = {}
        for input in self.has_input:
            try:
                input_dict[input.type] = dict_to_search[input.has_reference]
            except KeyError:
                input_dict[input.type] = fallback_df[input.has_source]

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
