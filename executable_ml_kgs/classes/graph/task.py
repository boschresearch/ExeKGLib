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

    def create_output_dict(self, string_value_dict: dict) -> dict:
        if len(self.has_output) == 0:
            # assume one output and use task name as key
            return {self.name: list(string_value_dict.values())[0]}

        output_names = [has_output_elem.name for has_output_elem in self.has_output]
        out_dict = {}
        for output_name in output_names:
            for key, value in string_value_dict.items():
                if key in output_name:
                    out_dict[output_name] = value

        return out_dict

    def get_inputs(
        self, other_task_output_dict: dict, input_data: pd.DataFrame
    ) -> list:
        input_names = [has_input_elem.name for has_input_elem in self.has_input]
        inputs_from_other_tasks = []
        for input_name in input_names:
            try:
                inputs_from_other_tasks.append(other_task_output_dict[input_name])
            except KeyError:
                continue

        # print("inputs from other tasks:", inputs_from_other_tasks)
        if len(inputs_from_other_tasks) == 0:
            return [input_data]

        return inputs_from_other_tasks

    @abstractmethod
    def run_method(self, *args):
        raise NotImplementedError
