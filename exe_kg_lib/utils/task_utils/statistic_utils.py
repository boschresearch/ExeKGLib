# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

import numpy as np
import pandas as pd


def trend_calculation(
    input_data: np.ndarray,
    half_window_size: int = 2,
    padding: str = "same",
) -> np.ndarray:
    """calculate the trend of the data, which is the sliding-window average"""

    def padding_input(input: np.ndarray, half_window_size: int, padding: str = "same") -> np.ndarray:
        """padding the beginning and end of the input data by the beginning or end value"""
        if padding == "same":
            begin_padding = pd.Series([input.iloc[0]] * half_window_size)
            end_padding = pd.Series([input.iloc[len(input) - 1]] * half_window_size)
            output = pd.concat([begin_padding, input, end_padding]).reset_index().drop("index", axis=1)
            return output

        else:
            return 0

    input = padding_input(input_data, half_window_size)

    output = 0
    input_len = len(input) - 2 * half_window_size
    for i in range(2 * half_window_size + 1):
        output += np.array(input.iloc[i : i + input_len])

    output = output / (2 * half_window_size + 1)

    return output


def mean_calculation(input_data: np.ndarray) -> np.ndarray:
    return np.mean(input_data)


def std_deviation(input_data: np.ndarray) -> np.ndarray:
    return np.std(input_data)


def minimum_calculation(input_data: np.ndarray) -> np.ndarray:
    return np.min(input_data)


def maximum_calculation(input_data: np.ndarray) -> np.ndarray:
    return np.max(input_data)


def iqr_calculation(input_data: np.ndarray, percent: int = 50) -> np.ndarray:
    """return quarter of the input_data"""
    return np.percentile(input_data, percent)


def outlier_calculation(input: np.ndarray, iq1: float = None, iq3: float = None) -> np.ndarray:
    """return the outliers in the data"""
    iq1 = iqr_calculation(input, 25) if (not iq1) else iq1
    iq3 = iqr_calculation(input, 75) if (not iq3) else iq3
    median = np.median(input)
    iqr = iq3 - iq1
    high_outliers = input < median - 1.5 * iqr
    low_outliers = input > median + 1.5 * iqr
    outlier_rows = [low_outliers.iloc[i] or high_outliers.iloc[i] for i in range(len(input))]
    return outlier_rows


def scattering_calculation(input_data: np.ndarray) -> np.ndarray:
    trend_calc_output = trend_calculation(input_data)
    output = input_data - trend_calc_output

    return output


def normalization(input_data: np.ndarray) -> np.ndarray:
    mean = mean_calculation(input_data)
    std = std_deviation(input_data)
    output = (input_data - mean) / std

    return output
