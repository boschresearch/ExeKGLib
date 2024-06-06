# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from abc import abstractmethod
from typing import Any, Dict

import pandas as pd

from ..task import Task

"""
❗ Important for contributors: See the package's README.md before extending the code's functionality.
"""


class StatisticCalculation(Task):
    """
    Abstraction of owl:class stats:StatisticCalculation.

    This class represents a task for calculating a statistic.
    """

    @abstractmethod
    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculates a statistic. The data to use are determined by self.inputs.
        Expects one input data value with name "DataInStatisticCalculation".

        Args:
            other_task_output_dict (dict): A dictionary containing the output of other tasks.
            input_data (pd.DataFrame): The input data of the ExeKG's pipeline.

        Returns:
            Dict[str, Any]: A dictionary containing the calculated statistic with the key "DataOutStatisticCalculation".

        Raises:
            NotImplementedError: If the statistic is not supported.
        """
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        input_data = input_dict["DataInStatisticCalculation"]
        input = input_data[0]["value"]  # assume one input

        method_module = self.method.resolve_module(module_name_to_snakecase=True)
        if "numpy" in method_module.__module__:
            statistic_result = method_module(input, **self.method.params_dict)
            return self.create_output_dict({"DataOutStatisticCalculation": statistic_result})
        else:
            raise NotImplementedError("Only numpy library is supported for now")
