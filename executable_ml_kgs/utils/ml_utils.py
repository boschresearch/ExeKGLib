from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor


def concatenation(input_data: pd.DataFrame, data_sources: list[str]) -> pd.DataFrame:
    filtered_columns = input_data[data_sources]
    return filtered_columns


def data_splitting(
    input_data: pd.DataFrame, split_ratio: str
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """split data into training and testing set"""
    # print('inside data splitting function #')
    # print('input_data = ', input_data)
    # training_data_name = None
    # test_data_name = None
    #
    # for i in output_data_sources:
    #     if "Train" in i:
    #         result = parse_entity(self.graph, i, self.dict_namespace)
    #         print(result)
    #         training_data_name = i  # result['exeKG:hasSource'][0]
    #     elif "Test" in i:
    #         result = parse_entity(self.graph, i, self.dict_namespace)
    #         print(result)
    #         test_data_name = i  # result['exeKG:hasSource'][0]
    #     else:
    #         pass

    splitting_point = int(float(split_ratio) * float(input_data.shape[0]))
    out_training = input_data.iloc[:splitting_point]
    out_test = input_data.iloc[splitting_point:]

    # self.extra_data_list[training_data_name] = out_training
    # self.extra_data_list[test_data_name] = out_test

    # print(self.extra_data_list)

    return out_training, out_test


def k_nn_train(
    input_x: np.ndarray, input_y: np.ndarray, n_neighbors: int = 3
) -> Tuple[KNeighborsRegressor, np.ndarray]:
    print("n_neighbors = ", n_neighbors)
    model = KNeighborsRegressor(n_neighbors=n_neighbors)
    model.fit(input_x, input_y)

    predicted_y = model.predict(input_x)

    # out_names = task_pos["exeKG:hasOutput"]
    # for name in out_names:
    #     if "Predict" in name:
    #         self.extra_data_list[name] = predicted_y

    print("KNN training finished")

    return model, predicted_y


def k_nn_test(model: KNeighborsRegressor, input_x: np.ndarray) -> np.ndarray:
    # assert isinstance(knn, KNeighborsRegressor)

    predicted_y = model.predict(input_x)

    # out_names = task_pos["exeKG:hasOutput"]
    # for name in out_names:
    #     if "Predict" in name:
    #         self.extra_data_list[name] = predicted_y

    print("KNN testing finished")

    return predicted_y


def lr_training(
    input_x: np.ndarray, input_y: np.ndarray
) -> Tuple[LinearRegression, np.ndarray]:
    model = LinearRegression()
    model.fit(input_x, input_y)
    predicted_y = model.predict(input_x)
    # print('input_x = ', input_x)
    # print('predicted_y = ', len(predicted_y))
    # print('input_y = ', len(input_y))
    # plt.plot(predicted_y, label = 'predicted')
    # plt.plot(input_y, label = 'input')

    # out_names = task_pos["exeKG:hasOutput"]
    # for name in out_names:
    #     if "Predict" in name:
    #         self.extra_data_list[name] = predicted_y

    # plt.legend()
    # plt.show()
    print("LR training finished")
    return model, predicted_y


def lr_testing(model: LinearRegression, input_x: np.ndarray):
    # assert not reg is None
    # assert isinstance(reg, LinearRegression)
    predict_y = model.predict(input_x)
    # plt.plot(input_y.index ,predict_y, label = 'predict')
    # plt.plot(input_y.index, input_y, label = 'input_y')

    # out_names = task_pos["exeKG:hasOutput"]
    # for name in out_names:
    #     if "Predict" in name:
    #         self.extra_data_list[name] = predict_y

    # print(self.extra_data_list)

    # plt.legend()
    # plt.show()

    return predict_y


# def mlp_train(self, input_x, input_y, task_pos, solver="adam"):
#     mlp = MLPRegressor(solver=solver)
#     mlp.fit(input_x, input_y)
#
#     self.model = mlp
#     predicted_y = mlp.predict(input_x)
#
#     out_names = task_pos["exeKG:hasOutput"]
#     for name in out_names:
#         if "Predict" in name:
#             self.extra_data_list[name] = predicted_y
#
#     print("MLP training finished")
#
#
# def mlp_test(self, input_x, input_y, task_pos):
#     mlp = self.model
#     assert isinstance(mlp, MLPRegressor)
#
#     predicted_y = mlp.predict(input_x)
#
#     out_names = task_pos["exeKG:hasOutput"]
#     for name in out_names:
#         if "Predict" in name:
#             self.extra_data_list[name] = predicted_y
#
#     print("MLP testing finished")


def ml_performance_calculation(
    real_train: np.ndarray = 0,
    real_test: np.ndarray = 0,
    predicted_train: np.ndarray = 0,
    predicted_test: np.ndarray = 0,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    # real_train = 0
    # real_test = 0
    # predict_train = 0
    # predict_test = 0

    # print("inputs = ", inputs)
    # for input in inputs:
    #     if "Train" in input and "Predict" in input:
    #         predict_train = self.extra_data_list[input]
    #     elif "Test" in input and "Predict" in input:
    #         predict_test = self.extra_data_list[input]
    #     elif "Train" in input and "Split" in input:
    #         real_train = self.extra_data_list[input]
    #         real_train = real_train[real_train.columns[-1]]
    #     elif "Test" in input and "Split" in input:
    #         real_test = self.extra_data_list[input]
    #         real_test = real_test[real_test.columns[-1]]

    # print(real_test)
    # print(predict_train)
    train_err = pd.DataFrame(real_train - predicted_train)
    test_err = pd.DataFrame(real_test - predicted_test)

    # print('train_err = ', train_err)
    # print('test_err = ', test_err)

    # plt.plot(train_err.index, train_err, label = 'train')
    # plt.plot(test_err.index, test_err, label = 'test')
    # plt.legend()
    # plt.show()

    # outputs = task_pos["exeKG:hasOutput"]
    # for output in outputs:
    #     if "Test" in output:
    #         self.extra_data_list[output] = test_err
    #     elif "Train" in output:
    #         self.extra_data_list[output] = train_err
    #     else:
    #         pass

    print("ml_performance_calculation finished")

    return train_err, test_err
