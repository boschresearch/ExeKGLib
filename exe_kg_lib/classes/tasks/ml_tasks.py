# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from ...utils.task_utils.ml_utils import *
from ..entity import Entity
from ..task import Task

"""
❗ Important for contributors: See the package's README.md before extending the code's functionality.
"""


class ConcatenationConcatenationMethod(Task):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)

    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame) -> dict:
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        concatenation_result = concatenation(list(input_dict.values()))
        return self.create_output_dict({"DataOutConcatenatedData": concatenation_result})


class DataSplittingDataSplittingMethod(Task):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)
        self.has_split_ratio = None

    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame) -> dict:
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        input_x = input_dict["DataInDataSplittingX"]
        input_y = input_dict["DataInDataSplittingY"]
        train_x, test_x, train_y, test_y = data_splitting(input_x, input_y, self.has_split_ratio)

        return self.create_output_dict(
            {
                "DataOutSplittedTrainDataX": train_x,
                "DataOutSplittedTestDataX": test_x,
                "DataOutSplittedTrainDataY": train_y,
                "DataOutSplittedTestDataY": test_y,
            }
        )


class TrainKNNTrain(Task):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)

    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame) -> dict:
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        input_x = input_dict["DataInTrainX"]
        input_y = input_dict["DataInTrainY"]
        model, predicted_y = k_nn_train(input_x, input_y)

        return self.create_output_dict({"DataOutTrainModel": model, "DataOutPredictedValueTrain": predicted_y})


class TestKNNTest(Task):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)

    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame) -> dict:
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        model = input_dict["DataInTestModel"]
        input_x = input_dict["DataInTestX"]

        predicted_y = k_nn_test(model, input_x)
        return self.create_output_dict({"DataOutPredictedValueTest": predicted_y})


class TrainLRTrain(Task):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)

    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame) -> dict:
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        input_x = input_dict["DataInTrainX"]
        input_y = input_dict["DataInTrainY"]

        model, predicted_y = lr_training(input_x, input_y)

        return self.create_output_dict({"DataOutModel": model, "DataOutPredictedValueTrain": predicted_y})


class TestLRTest(Task):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)

    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame) -> dict:
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        model = input_dict["DataInModel"]
        input_x = input_dict["DataInTestX"]

        predicted_y = lr_testing(model, input_x)
        return self.create_output_dict({"DataOutPredictedValueTest": predicted_y})


class TrainMLPTrain(Task):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)

    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame) -> dict:
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        input_x = input_dict["DataInTrainX"]
        input_y = input_dict["DataInTrainY"]

        model, predicted_y = mlp_train(input_x, input_y)

        return self.create_output_dict({"DataOutModel": model, "DataOutPredictedValueTrain": predicted_y})


class TestMLPTest(Task):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)

    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame) -> dict:
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        model = input_dict["DataInModel"]
        input_x = input_dict["DataInTestX"]

        predicted_y = mlp_test(model, input_x)
        return self.create_output_dict({"DataOutPredictedValueTest": predicted_y})


class PerformanceCalculationPerformanceCalculationMethod(Task):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)

    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame) -> dict:
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        real_train_y = input_dict["DataInTrainRealY"]
        real_test_y = input_dict["DataInTestRealY"]
        predicted_train_y = input_dict["DataInTrainPredictedY"]
        predicted_test_y = input_dict["DataInTestPredictedY"]

        train_error, test_error = ml_performance_calculation(
            real_train_y, real_test_y, predicted_train_y, predicted_test_y
        )

        return self.create_output_dict({"DataOutMLTrainErr": train_error, "DataOutMLTestErr": test_error})
