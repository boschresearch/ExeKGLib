from utils.statistic_utils import *
from .entity import Entity
from .task import Task


class TrendCalculationTaskTrendCalculationMethod(Task):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)

    def run_method(
        self, other_task_output_dict: dict, input_data: pd.DataFrame
    ) -> dict:
        input = self.get_one_input(other_task_output_dict, input_data)
        trend_calculation_result = trend_calculation(
            input, self.has_input[0].has_source
        )

        return self.create_output_dict({"Trend": trend_calculation_result})


class ScatteringCalculationTaskScatteringCalculationMethod(Task):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)

    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame):
        input = self.get_one_input(other_task_output_dict, input_data)
        scattering_calculation_result = scattering_calculation(
            input, self.has_input[0].has_source
        )

        return self.create_output_dict({"Scattering": scattering_calculation_result})


class NormalizationTaskNormalizationMethod(Task):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)

    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame):
        input = self.get_one_input(other_task_output_dict, input_data)
        normalization_result = normalization(input, self.has_input[0].has_source)

        return self.create_output_dict({"Normalization": normalization_result})
