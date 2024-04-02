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
        input_x = input_dict["DataInTrainX"][0]["value"]
        input_y = input_dict["DataInTrainY"][0]["value"]

        method_module = self.resolve_module()
        if "sklearn" in method_module.__module__:
            # module_name = self.method_module_chain.split(".")[-1]

            # self.method_module = getattr(module, module_name)
            assert isinstance(method_module, type), "The method_module should be a class"
            model = method_module(**self.method_params_dict)
            model.fit(input_x, input_y)

            print(f"{model.__class__.__name__} training finished")
        else:
            raise NotImplementedError("Only sklearn models are supported for now")

        return self.create_output_dict({"DataOutTrainModel": model})


class Test(Task):
    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame):
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        model = input_dict["DataInTestModel"][0]["value"]
        input_x = input_dict["DataInTestX"][0]["value"]

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
        input_x = input_dict["DataInTrainAndTestX"][0]["value"]
        input_y = input_dict["DataInTrainAndTestY"][0]["value"]

        model = Train.run_method(self, {"DataInTrainX": input_x, "DataInTrainY": input_y}, input_data)

        predicted_y = Test.run_method(self, {"DataInTestModel": model, "DataInTestX": input_x}, input_data)
        # predicted_y = self.abstract_test_method(model, input_x)

        return self.create_output_dict(
            {"DataOutTrainAndTestModel": model, "DataOutPredictedValueTrainAndTest": predicted_y}
        )


class PrepareTransformer(Task):
    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame):
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        input = input_dict["DataInToPrepareTransformer"][0]["value"]

        method_module = self.resolve_module()
        if "sklearn" in method_module.__module__:
            assert isinstance(method_module, type), "The method_module should be a class"
            transformer = method_module(**self.method_params_dict)
            transformer.fit(input)

            print(f"{transformer.__class__.__name__} transforming finished")
        else:
            raise NotImplementedError("Only sklearn data transformers are supported for now")

        return self.create_output_dict({"DataOutTransformer": transformer})


class Transform(Task):
    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame):
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        transformer = input_dict["DataInTransformer"][0]["value"]
        input = input_dict["DataInToTransform"][0]["value"]

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
        input = input_dict["DataInPrepareTransformAndTransform"][0]["value"]

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
        input_x = input_dict["DataInDataSplittingX"][0]["value"]
        input_y = input_dict["DataInDataSplittingY"][0]["value"]

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

                # TODO: handle sklearn's splitters like KFold, StratifiedKFold, etc. that allow for multiple splits via n_splits
                #       https://scikit-learn.org/stable/modules/cross_validation.html
                # NOTE: in this case, the model should be trained and tested for each split, and the metric value should be averaged
                #       https://www.askpython.com/python/examples/k-fold-cross-validation
                for train_index, test_index in splitter.split(input_x, input_y):
                    train_x, test_x = input_x.iloc[train_index], input_x.iloc[test_index]
                    train_y, test_y = input_y.iloc[train_index], input_y.iloc[test_index]

                print(f"{splitter.__class__.__name__} splitting finished")
        else:
            raise NotImplementedError("Only sklearn data splitters are supported for now")

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
        input_real_y = input_dict["DataInRealY"][0]["value"]
        # predicted_train_y = input_dict["DataInTrainPredictedY"]
        input_predicted_y = input_dict["DataInPredictedY"][0]["value"]

        method_module = self.resolve_module(module_name_to_snakecase=True)

        if "sklearn" in method_module.__module__:
            assert callable(method_module), "The method_module should be a function"
            metric_value = method_module(input_real_y, input_predicted_y, **self.method_params_dict)
        else:
            raise NotImplementedError("Only sklearn metrics are supported for now")

        return self.create_output_dict({"DataOutScore": metric_value})


class Concatenation(Task):
    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame) -> dict:
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        inputs = input_dict["DataInConcatenation"]
        input_values = [input["value"] for input in inputs]

        concatenation_result = concatenation(input_values)

        return self.create_output_dict({"DataOutConcatenatedData": concatenation_result})
