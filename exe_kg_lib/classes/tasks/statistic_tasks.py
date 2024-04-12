# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from abc import abstractmethod

import pandas as pd

from ..task import Task

"""
❗ Important for contributors: See the package's README.md before extending the code's functionality.
"""


class StatisticCalculation(Task):
    @abstractmethod
    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame):
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        input_data = input_dict["DataInStatisticCalculation"]
        input = input_data[0]["value"]  # assume one input

        method_module = self.resolve_module(module_name_to_snakecase=True)
        if "numpy" in method_module.__module__:
            statistic_result = method_module(input, **self.method_params_dict)
            return self.create_output_dict({"DataOutStatisticCalculation": statistic_result})
        else:
            raise NotImplementedError("Only numpy library is supported for now")
