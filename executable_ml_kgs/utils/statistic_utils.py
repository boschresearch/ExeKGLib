import numpy as np
import pandas as pd


# TODO: remove because it's welding-specific
def select_program(input_data, program, name: str = "WeldingProgramNumber"):
    # program must be int to be compared with excel data
    return (
        input_data[name] == int(program)
        if (program and name)
        else [True] * len(input_data)
    )


# TODO: remove because it's welding-specific
def welding_program_filter(
        input_data: pd.DataFrame,
        data_to_filter: pd.Series,
        filter_value: int = 1,
        filter_name: str = "WeldingProgramNumber",
):
    """currently only used for distinguishing filtering different program numbers"""
    return data_to_filter[select_program(input_data, filter_value, filter_name)]


def add_new_data(
        data_to_add: pd.DataFrame,
        input_data: pd.DataFrame,
        data_source: str,
        column_name: str = None,
        program: int = None,
        filter_name: str = "WeldingProgramNumber",
):
    """add new column to the raw_data while keeping the index consistent,
    assuming the input_data does not have NaN"""
    selected_rows = select_program(input_data, program=program, name=filter_name)
    # trying to make new column the same length as old column, maybe not needed
    input_data[data_source + column_name + str(program)] = np.NaN
    # print(selected_rows)
    # print(input_data)
    input_data.loc[selected_rows, data_source + column_name + str(program)] = np.array(
        data_to_add
    )
    # self.extra_data_list[data_source + column_name + str(program)] = data_to_add


def trend_calculation(
        input_data: pd.DataFrame,
        data_source: str,
        half_window_size: int = 2,
        padding="same",
):
    """calculate the trend of the data, which is the sliding-window average"""

    filtered_input_data = input_data[data_source]

    def padding_input(input, half_window_size, padding="same"):
        """padding the beginning and end of the input data by the beginning or end value"""
        if padding == "same":
            # print(input)
            begin_padding = pd.DataFrame([input.iloc[0]] * half_window_size)
            end_padding = pd.DataFrame([input.iloc[len(input) - 1]] * half_window_size)
            input = (
                pd.concat([begin_padding, input, end_padding])
                .reset_index()
                .drop("index", axis=1)
            )
            return input

        else:
            return 0

    # choose the input
    # program = kwargs.get("program", "")
    program = 1  # TODO: remove because it's welding-specific

    input = welding_program_filter(input_data, filtered_input_data, program)

    input = padding_input(input, half_window_size)

    output = 0
    input_len = len(input) - 2 * half_window_size
    for i in range(2 * half_window_size + 1):
        output += np.array(input.iloc[i: i + input_len])

    output = output / (2 * half_window_size + 1)
    output = pd.DataFrame(output)

    add_new_data(
        output,
        input_data,
        data_source,
        "_trend",
        program,
        "WeldingProgramNumber",
    )

    return input_data[data_source + "_trend" + str(program)]


def mean_calculation(input_data: pd.DataFrame):
    return np.mean(input_data)


def std_deviation(input_data: pd.DataFrame):
    return np.std(input_data)


# def concatenation_method(input_data, out_name):
#     """concatenate the data specified from extra dictionary,
#     maybe need to specify input?
#     """
#     output = []
#     # for i in self.extra_data_list:
#     # output.append(self.raw_data[i])
#     # print(output)
#     output = input_data
#     # self.extra_data_list['ConcatenatedData'] = input_data
#     self.extra_data_list[out_name] = input_data
#     # print('out_name = ', out_name)
#     # print(self.extra_data_list)
#     return output


def minimum_calculation(input_data: pd.DataFrame = []):
    return np.min(input_data)


def maximum_calculation(input_data: pd.DataFrame = []):
    return np.max(input_data)


def iqr_calculation(input_data: list = [], percent: int = 50):
    """return quarter of the input_data"""
    return np.percentile(input_data, percent)


def outlier_calculation(input: list = [], iq1: float = None, iq3: float = None):
    """return the outliers in the data"""
    iq1 = iqr_calculation(input, 25) if (not iq1) else iq1
    iq3 = iqr_calculation(input, 75) if (not iq3) else iq3
    median = np.median(input)
    iqr = iq3 - iq1
    high_outliers = input < median - 1.5 * iqr
    low_outliers = input > median + 1.5 * iqr
    outlier_rows = [
        low_outliers.iloc[i] or high_outliers.iloc[i] for i in range(len(input))
    ]
    return input[outlier_rows], outlier_rows


def scattering_calculation(input_data: pd.DataFrame, data_source):
    # program = kwargs.get("program", "")
    program = 1  # TODO: remove because it's welding-specific

    try:
        input = input_data[data_source + "_trend" + str(program)]
    except:
        print("Warning: must perform trend before scatter!")
        trend_calculation(input_data, data_source)
        input = input_data[data_source + "_trend" + str(program)]

    output = input_data[data_source] - input
    selected_output = welding_program_filter(input_data, output, program)
    add_new_data(
        selected_output,
        input_data,
        data_source,
        "_scatter",
        program,
        "WeldingProgramNumber",
    )


def normalization(input_data: pd.DataFrame, data_source):
    program = 1  # TODO: remove because it's welding-specific

    filtered_data = welding_program_filter(input_data, input_data[data_source], program)
    # if not mean:
    mean = mean_calculation(filtered_data)
    # if not std:
    std = std_deviation(filtered_data)
    output = (filtered_data - mean) / std

    add_new_data(
        output, input_data, data_source, "_normalized", program
    )

    return output
