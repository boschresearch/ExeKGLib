# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

import importlib
from abc import abstractmethod
from typing import Any, Dict

import pandas as pd

from ..entity import Entity
from ..task import Task

"""
❗ Important for contributors: See the package's README.md before extending the code's functionality.
"""


class Train(Task):
    """
    Abstraction of owl:class ml:Train.

    This class represents a training task for machine learning models.
    """

    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame):
        """
        Trains the machine learning model determined by self.method.module_chain.
        The data to use are determined by self.inputs. Parameters to use for the model are in self.method.params_dict.
        Expects one input data value with name "DataInTrainX" and one with name "DataInTrainY".

        Args:
            other_task_output_dict (dict): A dictionary containing the output of other tasks.
            input_data (pd.DataFrame): The input data of the ExeKG's pipeline.

        Returns:
            dict: A dictionary containing the trained model with the key "DataOutTrainModel".

        Raises:
            NotImplementedError: If the model is not supported.
        """
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        input_x = input_dict["DataInTrainX"][0]["value"]
        input_y = input_dict["DataInTrainY"][0]["value"]
        input_model_as_method = None
        # check if input dict contains a method representing an ML model to be optimized
        if "InputModelAsMethod" in input_dict:
            input_model_as_method = input_dict["InputModelAsMethod"][0]["value"]
            input_model_as_method_module = input_model_as_method.resolve_module()

        method_module = self.method.resolve_module()
        if "sklearn" in method_module.__module__:
            assert isinstance(method_module, type), "The method_module should be a class"
            if input_model_as_method:
                # HPO (e.g. GridSearchCV) or Boosting (e.g. AdaBoostClassifier)
                model = method_module(
                    input_model_as_method_module(**input_model_as_method.params_dict),
                    **self.method.params_dict,
                )
            else:
                # normal training
                model = method_module(**self.method.params_dict)

            if not isinstance(input_x, list):
                model.fit(input_x, input_y)
            else:
                # multiple splits
                for x, y in zip(input_x, input_y):
                    model.fit(x, y)

            print(f"{model.__class__.__name__} training finished")
        else:
            raise NotImplementedError("Only sklearn models are supported for now")

        return self.create_output_dict({"DataOutTrainModel": model})


class Test(Task):
    """
    Abstraction of owl:class ml:Test.

    This class represents a test task for machine learning models.
    """

    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame):
        """
        Tests the machine learning model.
        The model and data to use are determined by self.inputs.
        Expects one input data value with name "DataInTestModel" and one with name "DataInTestX".

        Args:
            other_task_output_dict (dict): A dictionary containing the output of other tasks.
            input_data (pd.DataFrame): The input data of the ExeKG's pipeline.

        Returns:
            dict: A dictionary containing the predicted values with the key "DataOutPredictedValueTest".

        Raises:
            NotImplementedError: If the model is not supported.
        """
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        model = input_dict["DataInTestModel"][0]["value"]
        input_x = input_dict["DataInTestX"][0]["value"]

        # check if model belongs to sklearn library
        if "sklearn" in model.__module__:
            if not isinstance(input_x, list):
                predicted_y = model.predict(input_x)
            else:
                # multiple splits
                predicted_y = [model.predict(x) for x in input_x]
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
    """
    Abstraction of owl:class ml:PrepareTransformer.

    This class represents a task for preparing a data transformer.
    """

    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Prepares the transformer determined by self.method.module_chain.
        The data to use are determined by self.inputs. Parameters to use for the transformer are in self.method.params_dict.
        Expects one input data value with name "DataInToPrepareTransformer".

        Args:
            other_task_output_dict (dict): A dictionary containing the output of other tasks.
            input_data (pd.DataFrame): The input data of the ExeKG's pipeline.

        Returns:
            Dict[str, Any]: A dictionary containing the transformer with the key "DataOutTransformer".

        Raises:
            NotImplementedError: If the transformer is not supported.
        """
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        input = input_dict["DataInToPrepareTransformer"][0]["value"]

        method_module = self.method.resolve_module()
        if "sklearn" in method_module.__module__:
            assert isinstance(method_module, type), "The method_module should be a class"
            transformer = method_module(**self.method.params_dict)

            if not isinstance(input, list):
                transformer.fit(input)
            else:
                # multiple splits
                for input_part in input:
                    transformer.fit(input_part)

            print(f"{transformer.__class__.__name__} transforming finished")
        else:
            raise NotImplementedError("Only sklearn data transformers are supported for now")

        return self.create_output_dict({"DataOutTransformer": transformer})


class Transform(Task):
    """
    Abstraction of owl:class ml:Transform.

    This class represents a task for transforming data.
    """

    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Applies a transformation to the data.
        The model and data to use are determined by self.inputs.
        Expects one input data value with name "DataInTransformer" and one with name "DataInToTransform".

        Args:
            other_task_output_dict (dict): A dictionary containing the output of other tasks.
            input_data (pd.DataFrame): The input data of the ExeKG's pipeline.

        Returns:
            Dict[str, Any]: A dictionary containing the transformed data with the key "DataOutTransformed".

        Raises:
            NotImplementedError: If the transformer is not supported.
        """
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        transformer = input_dict["DataInTransformer"][0]["value"]
        input = input_dict["DataInToTransform"][0]["value"]

        # check if model belongs to sklearn library
        if "sklearn" in transformer.__module__:
            if not isinstance(input, list):
                transformed_input = transformer.transform(input)
            else:  # multiple splits
                transformed_input = [
                    transformer.transform(x) for x in input
                ]  # NOTE: it can be that the transformer will try to trasform unseen data, which will raise an error. e.g. if OneHotEncoder is used, one chunk of input may have a category that is not present in another chunk of input

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
    """
    Abstraction of owl:class ml:DataSplitting.

    This class represents a task for splitting data.
    """

    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Splits the data using the splitter determined by self.method.module_chain.
        The data to use are determined by self.inputs. Parameters to use for the splitter are in self.method.params_dict.
        Expects one input data value with name "DataInDataSplittingX" and one with name "DataInDataSplittingY".

        Args:
            other_task_output_dict (dict): A dictionary containing the output of other tasks.
            input_data (pd.DataFrame): The input data of the ExeKG's pipeline.

        Returns:
            Dict[str, Any]: A dictionary containing the splitted data with the keys "DataOutSplittedTrainDataX", "DataOutSplittedTrainDataY", "DataOutSplittedTestDataX", and "DataOutSplittedTestDataY".

        Raises:
            NotImplementedError: If the data splitter is not supported.
        """
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        input_x = input_dict["DataInDataSplittingX"][0]["value"]
        input_y = input_dict["DataInDataSplittingY"][0]["value"]

        if "TrainTestSplit" in self.method.module_chain:
            method_module = self.method.resolve_module(module_name_to_snakecase=True)
        else:
            method_module = self.method.resolve_module()

        # train_x, train_y, test_x, test_y = self.abstract_method(input_x, input_y)
        if "sklearn" in method_module.__module__:
            if method_module.__name__ == "train_test_split":
                train_x, test_x, train_y, test_y = method_module(input_x, input_y, **self.method.params_dict)
                print("train_test_split splitting finished")
                return self.create_output_dict(
                    {
                        "DataOutSplittedTrainDataX": train_x,
                        "DataOutSplittedTrainDataY": train_y,
                        "DataOutSplittedTestDataX": test_x,
                        "DataOutSplittedTestDataY": test_y,
                    }
                )
            else:
                assert isinstance(method_module, type), "The method_module should be a class"
                splitter = method_module(**self.method.params_dict)

                train_x_per_split = []
                valid_x_per_split = []
                train_y_per_split = []
                valid_y_per_split = []
                for train_index, valid_index in splitter.split(input_x, input_y):
                    train_x_per_split.append(input_x.iloc[train_index])
                    valid_x_per_split.append(input_x.iloc[valid_index])
                    train_y_per_split.append(input_y.iloc[train_index])
                    valid_y_per_split.append(input_y.iloc[valid_index])

                print(f"{splitter.__class__.__name__} splitting finished resulting in {len(train_x_per_split)} splits")
                return self.create_output_dict(
                    {
                        "DataOutSplittedTrainDataX": train_x_per_split,
                        "DataOutSplittedTrainDataY": train_y_per_split,
                        "DataOutSplittedTestDataX": valid_x_per_split,
                        "DataOutSplittedTestDataY": valid_y_per_split,
                    }
                )
        else:
            raise NotImplementedError("Only sklearn data splitters are supported for now")


class PerformanceCalculation(Task):
    """
    Abstraction of owl:class ml:PerformanceCalculation.

    This class represents a task for calculating the performance of a machine learning model.
    """

    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculates a score using a metric determined by self.method.module_chain.
        The data to use are determined by self.inputs. Parameters to use for the score calculation are in self.method.params_dict.
        Expects one input data value with name "DataInRealY" and one with name "DataInPredictedY".

        Args:
            other_task_output_dict (dict): A dictionary containing the output of other tasks.
            input_data (pd.DataFrame): The input data of the ExeKG's pipeline.

        Returns:
            Dict[str, Any]: A dictionary containing the calculated score with the key "DataOutScore".

        Raises:
            NotImplementedError: If the metric is not supported.
        """
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        # real_train_y = input_dict["DataInTrainRealY"]
        input_real_y = input_dict["DataInRealY"][0]["value"]
        # predicted_train_y = input_dict["DataInTrainPredictedY"]
        input_predicted_y = input_dict["DataInPredictedY"][0]["value"]

        method_module = self.method.resolve_module(module_name_to_snakecase=True)

        if "sklearn" in method_module.__module__:
            assert callable(method_module), "The method_module should be a function"
            if not isinstance(input_real_y, list):
                metric_value = method_module(input_real_y, input_predicted_y, **self.method.params_dict)
            else:
                # multiple splits
                metric_values = [
                    method_module(y, p, **self.method.params_dict) for y, p in zip(input_real_y, input_predicted_y)
                ]
                metric_value = sum(metric_values) / len(metric_values)
        else:
            raise NotImplementedError("Only sklearn metrics are supported for now")

        return self.create_output_dict({"DataOutScore": metric_value})


class Concatenation(Task):
    """
    Abstraction of owl:class ml:Concatenation.

    This class represents a task for concatenating data.
    """

    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Concatenates data. The data to use are determined by self.inputs.
        Expects multiple input data values with name "DataInConcatenation".

        Args:
            other_task_output_dict (dict): A dictionary containing the output of other tasks.
            input_data (pd.DataFrame): The input data of the ExeKG's pipeline.

        Returns:
            Dict[str, Any]: A dictionary containing the concatenated data with the key "DataOutConcatenatedData".
        """
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        inputs = input_dict["DataInConcatenation"]
        input_values = [input["value"] for input in inputs]

        concatenation_result = pd.concat(input_values, axis=1)

        return self.create_output_dict({"DataOutConcatenatedData": concatenation_result})
