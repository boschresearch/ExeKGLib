# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor


def concatenation(inputs: List[np.ndarray]) -> pd.DataFrame:
    return pd.concat(inputs, axis=1)


def data_splitting(
    input_x: pd.DataFrame, input_y: np.ndarray, split_ratio: str
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """split data into training and testing set"""

    splitting_point = int(float(split_ratio) * float(input_x.shape[0]))

    train_x = input_x.iloc[:splitting_point]
    test_x = input_x.iloc[splitting_point:]
    train_y = input_y.iloc[:splitting_point]
    test_y = input_y.iloc[splitting_point:]

    return train_x, test_x, train_y, test_y


def k_nn_train(
    input_x: np.ndarray, input_y: np.ndarray, n_neighbors: int = 3
) -> Tuple[KNeighborsRegressor, np.ndarray]:
    print("n_neighbors = ", n_neighbors)
    model = KNeighborsRegressor(n_neighbors=n_neighbors)
    model.fit(input_x, input_y)

    predicted_y = model.predict(input_x)

    print("KNN training finished")

    return model, predicted_y


def k_nn_test(model: KNeighborsRegressor, input_x: np.ndarray) -> np.ndarray:
    predicted_y = model.predict(input_x)

    print("KNN testing finished")

    return predicted_y


def lr_training(input_x: np.ndarray, input_y: np.ndarray) -> Tuple[LinearRegression, np.ndarray]:
    model = LinearRegression()
    model.fit(input_x, input_y)
    predicted_y = model.predict(input_x)

    print("LR training finished")
    return model, predicted_y


def lr_testing(model: LinearRegression, input_x: np.ndarray):
    predict_y = model.predict(input_x)

    return predict_y


def mlp_train(input_x: np.ndarray, input_y: np.ndarray, solver="adam") -> Tuple[MLPRegressor, np.ndarray]:
    model = MLPRegressor(solver=solver)
    model.fit(input_x, input_y)

    predicted_y = model.predict(input_x)

    print("MLP training finished")

    return model, predicted_y


def mlp_test(model: MLPRegressor, input_x: np.ndarray) -> np.ndarray:
    predicted_y = model.predict(input_x)

    print("MLP testing finished")

    return predicted_y


def ml_performance_calculation(
    real_train: np.ndarray = 0,
    real_test: np.ndarray = 0,
    predicted_train: np.ndarray = 0,
    predicted_test: np.ndarray = 0,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    train_err = pd.DataFrame(real_train - predicted_train)
    test_err = pd.DataFrame(real_test - predicted_test)

    return train_err, test_err
