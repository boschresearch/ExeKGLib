from utils.ml_utils import *
from .entity import Entity
from .task import Task


class ConcatenationConcatenationMethod(Task):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)

    def run_method(
        self, other_task_output_dict: dict, input_data: pd.DataFrame
    ) -> dict:
        data_sources = [has_input_elem.has_source for has_input_elem in self.has_input]
        concatenation_result = concatenation(input_data, data_sources)
        # assume one output
        output_name = self.has_output[0].name
        return {output_name: concatenation_result}


class DataSplittingDataSplittingMethod(Task):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)
        self.has_split_ratio = None

    def run_method(
        self, other_task_output_dict: dict, input_data: pd.DataFrame
    ) -> dict:
        # assume one input
        input_df = self.get_one_input(other_task_output_dict, input_data)
        train_data, test_data = data_splitting(input_df, self.has_split_ratio)

        return self.create_output_dict({"Train": train_data, "Test": test_data})


class TrainKNNTrain(Task):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)

    def run_method(
        self, other_task_output_dict: dict, input_data: pd.DataFrame
    ) -> dict:
        # assume one input
        input_x_y = self.get_one_input(other_task_output_dict, input_data)
        input_x = input_x_y[input_x_y.columns[:-1]]
        input_y = input_x_y[input_x_y.columns[-1]]
        model, predicted_y = k_nn_train(input_x, input_y)

        return self.create_output_dict({"Model": model, "Predicted": predicted_y})


class TestKNNTest(Task):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)

    def run_method(
        self, other_task_output_dict: dict, input_data: pd.DataFrame
    ) -> dict:
        model, input_x_y = self.get_inputs_from_dict(other_task_output_dict)
        input_x = input_x_y[input_x_y.columns[:-1]]

        predicted_y = k_nn_test(model, input_x)
        output_name = self.has_output[0].name  # assume one output
        return {output_name: predicted_y}


class TrainLRTrain(Task):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)

    def run_method(
        self, other_task_output_dict: dict, input_data: pd.DataFrame
    ) -> dict:
        # assume one input
        input_x_y = self.get_one_input(other_task_output_dict, input_data)

        input_x = input_x_y[input_x_y.columns[:-1]]
        input_y = input_x_y[input_x_y.columns[-1]]
        model, predicted_y = lr_training(input_x, input_y)

        return self.create_output_dict({"Model": model, "Predicted": predicted_y})


class TestLRTest(Task):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)

    def run_method(
        self, other_task_output_dict: dict, input_data: pd.DataFrame
    ) -> dict:
        model, input_x_y = self.get_inputs_from_dict(other_task_output_dict)
        input_x = input_x_y[input_x_y.columns[:-1]]

        predicted_y = lr_testing(model, input_x)
        output_name = self.has_output[0].name  # assume one output
        return {output_name: predicted_y}


class TrainMLPTrain(Task):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)

    def run_method(
        self, other_task_output_dict: dict, input_data: pd.DataFrame
    ) -> dict:
        # assume one input
        input_x_y = self.get_one_input(other_task_output_dict, input_data)

        input_x = input_x_y[input_x_y.columns[:-1]]
        input_y = input_x_y[input_x_y.columns[-1]]
        model, predicted_y = mlp_train(input_x, input_y)

        return self.create_output_dict({"Model": model, "Predicted": predicted_y})


class TestMLPTest(Task):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)

    def run_method(
        self, other_task_output_dict: dict, input_data: pd.DataFrame
    ) -> dict:
        model, input_x_y = self.get_inputs_from_dict(other_task_output_dict)
        input_x = input_x_y[input_x_y.columns[:-1]]

        predicted_y = mlp_test(model, input_x)
        output_name = self.has_output[0].name  # assume one output
        return {output_name: predicted_y}


class PerformanceCalculationPerformanceCalculationMethod(Task):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)

    def run_method(
        self, other_task_output_dict: dict, input_data: pd.DataFrame
    ) -> dict:
        (
            predicted_test,
            predicted_train,
            test_x_y,
            train_x_y,
        ) = self.get_inputs_from_dict(other_task_output_dict)
        real_test = test_x_y[test_x_y.columns[-1]]
        real_train = train_x_y[train_x_y.columns[-1]]

        train_error, test_error = ml_performance_calculation(
            real_train, real_test, predicted_train, predicted_test
        )

        return self.create_output_dict({"Train": train_error, "Test": test_error})
