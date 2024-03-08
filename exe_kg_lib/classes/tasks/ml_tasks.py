# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

import importlib
from abc import abstractmethod

from ...utils.task_utils.ml_utils import *
from ..entity import Entity
from ..task import Task

"""
❗ Important for contributors: See the package's README.md before extending the code's functionality.
"""


class Train(Task):
    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame):
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        input_x = input_dict["DataInTrainX"]
        input_y = input_dict["DataInTrainY"]

        method_module = self.resolve_module()
        if "sklearn" in method_module.__module__:
            # module_name = self.method_module_chain.split(".")[-1]

            # self.method_module = getattr(module, module_name)
            assert isinstance(method_module, type), "The method_module should be a class"
            model = method_module(**self.method_params_dict)
            model.fit(input_x, input_y)

            print(f"{model.__class__.__name__} training finished")

        return self.create_output_dict({"DataOutTrainModel": model})


class Test(Task):
    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame):
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        model = input_dict["DataInTestModel"]
        input_x = input_dict["DataInTestX"]

        # check if model belongs to sklearn library
        if "sklearn" in model.__module__:
            predicted_y = model.predict(input_x)
        else:
            raise NotImplementedError("Only sklearn models are supported for now")

        print(f"{model.__class__.__name__} testing finished")

        return self.create_output_dict({"DataOutPredictedValueTest": predicted_y})


class TrainAndTest(Train, Test):
    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame):
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        input_x = input_dict["DataInTrainAndTestX"]
        input_y = input_dict["DataInTrainAndTestY"]

        model = Train.run_method(self, {"DataInTrainX": input_x, "DataInTrainY": input_y}, input_data)

        predicted_y = Test.run_method(self, {"DataInTestModel": model, "DataInTestX": input_x}, input_data)
        # predicted_y = self.abstract_test_method(model, input_x)

        return self.create_output_dict(
            {"DataOutTrainAndTestModel": model, "DataOutPredictedValueTrainAndTest": predicted_y}
        )


class PrepareTransformer(Task):
    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame):
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        input = input_dict["DataInToTransform"]

        method_module = self.resolve_module()
        if "sklearn" in method_module.__module__:
            assert isinstance(method_module, type), "The method_module should be a class"
            transformer = method_module(**self.method_params_dict)
            transformer.fit(input)

            print(f"{transformer.__class__.__name__} transforming finished")

        return self.create_output_dict({"DataOutTransformer": transformer})


class Transform(Task):
    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame):
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        transformer = input_dict["DataInTransformer"]
        input = input_dict["DataInToTransform"]

        # check if model belongs to sklearn library
        if "sklearn" in transformer.__module__:
            transformed_input = transformer.transform(input)
        else:
            raise NotImplementedError("Only sklearn data transformers are supported for now")

        print(f"{transformer.__class__.__name__} transforming finished")

        return self.create_output_dict({"DataOutTransformed": transformed_input})


class PrepareTransformerAndTransform(PrepareTransformer, Transform):
    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame):
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        input = input_dict["DataInPrepareTransformAndTransform"]

        prepared_transformer = PrepareTransformer.run_method(self, {"DataInToTransform": input}, input_data)
        transformed_input = Transform.run_method(
            self, {"DataInTransformer": prepared_transformer, "DataInToTransform": input}, input_data
        )

        return self.create_output_dict(
            {"DataOutTransformer": prepared_transformer, "DataOutTransformed": transformed_input}
        )


class DataSplitting(Task):
    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame) -> dict:
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        input_x = input_dict["DataInDataSplittingX"]
        input_y = input_dict["DataInDataSplittingY"]

        if "TrainTestSplit" in self.method_module_chain:
            method_module = self.resolve_module(module_name_to_snakecase=True)
        else:
            method_module = self.resolve_module()

        # train_x, train_y, test_x, test_y = self.abstract_method(input_x, input_y)
        if "sklearn" in method_module.__module__:
            if method_module.__name__ == "train_test_split":
                train_x, test_x, train_y, test_y = method_module(input_x, input_y, **self.method_params_dict)
                print("train_test_split splitting finished")
            else:
                assert isinstance(method_module, type), "The method_module should be a class"
                splitter = method_module(**self.method_params_dict)

                splits = splitter.split(input_x, input_y)
                for train_index, test_index in splits:
                    train_x = [input_x[i] for i in train_index]
                    train_y = [input_y[i] for i in train_index]
                    test_x = [input_x[i] for i in test_index]
                    test_y = [input_y[i] for i in test_index]

                print(f"{splitter.__class__.__name__} splitting finished")

        return self.create_output_dict(
            {
                "DataOutSplittedTrainDataX": train_x,
                "DataOutSplittedTrainDataY": train_y,
                "DataOutSplittedTestDataX": test_x,
                "DataOutSplittedTestDataY": test_y,
            }
        )


class PerformanceCalculation(Task):
    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame) -> dict:
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        # real_train_y = input_dict["DataInTrainRealY"]
        input_real_y = input_dict["DataInRealY"]
        # predicted_train_y = input_dict["DataInTrainPredictedY"]
        input_predicted_y = input_dict["DataInPredictedY"]

        method_module = self.resolve_module(module_name_to_snakecase=True)

        if "sklearn" in method_module.__module__:
            assert callable(method_module), "The method_module should be a function"
            metric_value = method_module(input_real_y, input_predicted_y, **self.method_params_dict)

        return self.create_output_dict({"DataOutScore": metric_value})


class Concatenation(Task):
    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame) -> dict:
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        concatenation_result = concatenation(list(input_dict.values()))
        return self.create_output_dict({"DataOutConcatenatedData": concatenation_result})
