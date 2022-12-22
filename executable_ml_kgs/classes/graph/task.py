from abc import abstractmethod

import pandas as pd

from .entity import Entity


class Task(Entity):
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

    def create_output_dict(self, keyword_value_dict: dict) -> dict:
        """
        For each key in keyword_value_dict, checks if the key exists in an output name of the Task.
        If yes, adds the output name with its value to out_dict.
        @param keyword_value_dict: key-value pairs where key is a keyword to find in an output name of the Task
                                  and value is the value corresponding to that output name
        @return: out_dict with key-value pairs where key is an output name of the Task and value its output value
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

    def get_inputs_from_dict(self, dict_to_search: dict) -> list:
        """
        Tries to match the Task's input names with the keys of dict_to_search
        and fills inputs_found_in_dict with their corresponding values.
        @param dict_to_search: contains key-value pairs where key is a possible input name and value is its corresponding value
        @return: list with the found inputs' values
        """
        input_names = [has_input_elem.name for has_input_elem in self.has_input]
        inputs_found_in_dict = []
        for input_name in input_names:
            try:
                inputs_found_in_dict.append(dict_to_search[input_name])
            except KeyError:
                continue

        return inputs_found_in_dict

    def get_one_input(
        self, dict_to_search: dict, fallback_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Tries to match the Task's first input name with the keys of dict_to_search and return its corresponding value.
        If the match fails, it returns the provided fallback_df
        @param dict_to_search: contains key-value pairs where key is a possible input name and value is its corresponding value
        @param fallback_df: data to return as an alternative
        @return: found input's value or fallback_df
        """
        try:
            return dict_to_search[self.has_input[0].name]
        except KeyError:
            return fallback_df

    @abstractmethod
    def run_method(self, *args):
        """
        Abstract method to be implemented by Task sub-classes that are in the bottom of the hierarchy.
        Executes the logic that is needed to fulfill the Task.
        @param args: defined by sub-classes
        """
        raise NotImplementedError
