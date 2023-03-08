# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from ...utils.task_utils.statistic_utils import *
from ..entity import Entity
from ..task import Task

"""
❗ Important for contributors: See the package's README.md before extending the code's functionality.
"""


class TrendCalculationTaskTrendCalculationMethod(Task):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)

    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame) -> dict:
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        input_data = list(input_dict.values())[0]  # one input expected
        trend_calculation_result = trend_calculation(input_data)

        return self.create_output_dict({"DataOutTrendCalculation": trend_calculation_result})


class ScatteringCalculationTaskScatteringCalculationMethod(Task):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)

    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame) -> dict:
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        input_data = list(input_dict.values())[0]  # one input expected
        scattering_calculation_result = scattering_calculation(input_data)

        return self.create_output_dict({"DataOutScatteringCalculation": scattering_calculation_result})


class NormalizationTaskNormalizationMethod(Task):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)

    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame) -> dict:
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        input_data = list(input_dict.values())[0]  # one input expected
        normalization_result = normalization(input_data)

        return self.create_output_dict({"DataOutNormalization": normalization_result})
