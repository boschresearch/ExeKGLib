import time

import numpy as np
import pandas as pd
from rdflib import Graph

from utils import parse_entity
from classes.pipeline_execution.pipeline_processor import PipelineProcessor


class StatsiticsAnalyzer(PipelineProcessor):
    """class for statistical analysis"""

    def __init__(self, dir_out="."):
        self.raw_data = None
        self.graph = Graph()
        self.dict_namespace = {}
        self.program = None
        self.extra_data_list = {}

    # def load_graph(self, kg_path = r"KG/exeKGOntology.ttl"):
    #     '''load the KG from .ttl file into the object'''
    #     self.graph.parse(kg_path)

    # def load_data(self, raw_path = r'data/a.csv'):
    #     '''load the raw csv data
    #     Args:
    #         raw_path: csv file path
    #     '''
    #     self.raw_data = pd.read_csv(raw_path, delimiter=',',encoding="ISO-8859-1")

    def add_new_data(
        self,
        input_data,
        data_source: str,
        column_name: str = None,
        program: int = None,
        filter_name: str = "WeldingProgramNumber",
    ):
        """add new column to the raw_data while keeping the index consistent,
        assuming the input_data does not have NaN"""
        selected_rows = self.select_program(program=program, name=filter_name)
        # trying to make new column the same length as old column, maybe not needed
        self.raw_data[data_source + column_name + str(program)] = np.NaN
        # print(selected_rows)
        # print(input_data)
        self.raw_data.loc[selected_rows, data_source + column_name + str(program)] = np.array(input_data)
        self.extra_data_list[data_source + column_name + str(program)] = input_data

    def trend_calculation_method(self, data_source: str, half_window_size: int = 2, padding="same", **kwargs):
        """calculate the trend of the data, which is the sliding-window average"""
        # print('Calculating trend now ...')
        start_time = time.time()

        def padding_input(input, half_window_size, padding="same"):
            """padding the beginning and end of the input data by the beginning or end value"""
            if padding == "same":
                # print(input)
                begin_padding = pd.DataFrame([input.iloc[0]] * half_window_size)
                end_padding = pd.DataFrame([input.iloc[len(input) - 1]] * half_window_size)
                input = pd.concat([begin_padding, input, end_padding]).reset_index().drop("index", axis=1)
                return input

            else:
                return 0

        # choose the input
        program = kwargs.get("program", "")
        # selected_rows = self.raw_data['WeldingProgramNumber'] == program if(program) else [True] * len(self.raw_data[data_source])
        # print(selected_rows)
        # the padding
        # input = padding_input(self.raw_data[data_source][selected_rows], half_window_size)
        input = self.welding_program_filter(self.raw_data[data_source], program)
        # print('input = ',input)
        input = padding_input(input, half_window_size)

        # print("input = ", input)
        # plt.plot(input)
        # the sliding window calculation

        ### version 1 of trend calculation
        # output = []
        # for i in range(len(input)-2*half_window_size):
        #     output.append(np.mean(input[i:i+2*half_window_size+1]))

        # output = pd.DataFrame(output)

        ### version 2 of trend calculation
        output = 0
        input_len = len(input) - 2 * half_window_size
        for i in range(2 * half_window_size + 1):
            output += np.array(input.iloc[i : i + input_len])

        output = output / (2 * half_window_size + 1)
        output = pd.DataFrame(output)

        # print(output)
        # print(output2)

        # print('output - output2 = ', output - output2)

        # print('output = ', output)
        self.add_new_data(output, data_source, "_trend", program, "WeldingProgramNumber")
        # print(self.raw_data['QVALUEActual_WeldingProgramNumber_2'][:20])
        # print(self.raw_data)
        # plt.plot(output, label='trend'+str(program))
        # print('trend calculation finished ...')
        end_time = time.time()
        print("trend_time = ", end_time - start_time)
        return self.raw_data[data_source + "_trend" + str(program)]

    # def select_program(self, program, name:str = 'WeldingProgramNumber'):
    #     # program must be int to be compared with excel data
    #     return self.raw_data[name] == int(program) if(program and name) else [True] * len(self.raw_data)

    def scattering_calculation(self, data_source: str, **kwargs):
        # print('Calculating scattering now ...')
        program = kwargs.get("program", "")
        # selected_rows = self.select_program(program)
        try:
            input = self.raw_data[data_source + "_trend" + str(program)]
        except:
            print("Warning: must perform trend before scatter!")
            self.trend_calculation_method(data_source, 2, "same", program=program)
            input = self.raw_data[data_source + "_trend" + str(program)]

        output = self.raw_data[data_source] - input
        # selected_rows = self.select_program(data_source, program, 'WeldingProgramNumber')
        selected_output = self.welding_program_filter(output, program)
        # self.add_new_data(output[selected_rows], data_source, '_scatter', program, 'WeldingProgramNumber')
        self.add_new_data(selected_output, data_source, "_scatter", program, "WeldingProgramNumber")
        # print(output)
        # plt.scatter(range(len(real_value)), real_value, label = 'Q-Value'+str(program))
        # plt.scatter(range(len(output)), output, label = 'scatter'+str(program))
        # plt.show()
        # print('scattering calculation finished!')
        return selected_output

    def iqr_calculation_method(self, input_data: list = [], percent: int = 50):
        """return quarter of the input_data"""
        return np.percentile(input_data, percent)

    def outlier_calculation(self, input: list = [], iq1: float = None, iq3: float = None):
        """return the outliers in the data"""
        iq1 = self.iqr_calculation_method(input, 25) if (not iq1) else iq1
        iq3 = self.iqr_calculation_method(input, 75) if (not iq3) else iq3
        median = np.median(input)
        iqr = iq3 - iq1
        high_outliers = input < median - 1.5 * iqr
        low_outliers = input > median + 1.5 * iqr
        outlier_rows = [low_outliers.iloc[i] or high_outliers.iloc[i] for i in range(len(input))]
        return input[outlier_rows], outlier_rows

    # def dictionary_construction_method(self, input_data, data_source:str, column_name:str = None, filter_value:int = None, filter_name:str = None):
    #     self.add_new_data(input_data, data_source, column_name, filter_value, filter_name)
    #     self.extra_data_list.append(data_source+column_name+str(filter_value))

    def mean_calculation_method(self, input_data: pd.DataFrame = []):
        return np.mean(input_data)

    def std_deviation_method(self, input_data: pd.DataFrame = []):
        return np.std(input_data)

    def concatenation_method(self, input_data, out_name):
        """concatenate the data specified from extra dictionary,
        maybe need to specify input?
        """
        output = []
        # for i in self.extra_data_list:
        # output.append(self.raw_data[i])
        # print(output)
        output = input_data
        # self.extra_data_list['ConcatenatedData'] = input_data
        self.extra_data_list[out_name] = input_data
        # print('out_name = ', out_name)
        # print(self.extra_data_list)
        return output

    def minimum_calculation_method(self, input_data: pd.DataFrame = []):
        return np.min(input_data)

    def maximum_calculation_method(self, input_data: pd.DataFrame = []):
        return np.max(input_data)

    def normalization_method(
        self,
        input_data: pd.DataFrame = [],
        data_source: str = None,
        mean: float = None,
        std: float = None,
    ):
        input_data = self.welding_program_filter(input_data, self.program)
        if not mean:
            mean = self.mean_calculation_method(input_data)
        if not std:
            std = self.std_deviation_method(input_data)
        output = (input_data - mean) / std

        self.add_new_data(output, data_source, "_normalized", self.program)
        return output

    def data_splitting(self, input_data, task_pos):
        """split data into training and testing set"""
        # print('inside data splitting function #')
        # print('input_data = ', input_data)
        output_names = task_pos["exeKG:hasOutput"]
        training_data_name = None
        test_data_name = None

        for i in output_names:
            if "Train" in i:
                result = parse_entity(self.graph, i, self.dict_namespace)
                print(result)
                training_data_name = i  # result['exeKG:hasSource'][0]
            elif "Test" in i:
                result = parse_entity(self.graph, i, self.dict_namespace)
                print(result)
                test_data_name = i  # result['exeKG:hasSource'][0]
            else:
                pass

        split_ration = task_pos["exeKG:SplitRatio"][0]

        splitting_point = int(float(split_ration) * float(input_data.shape[0]))
        out_training = input_data.iloc[:splitting_point]
        out_test = input_data.iloc[splitting_point:]

        self.extra_data_list[training_data_name] = out_training
        self.extra_data_list[test_data_name] = out_test

        # print(self.extra_data_list)

    def execute_task(self, task_pos):
        """distinguish between different statistics tasks, and apply different methods"""
        data_source = []
        try:
            if len(task_pos["exeKG:hasInput"]) == 1:
                input = parse_entity(self.graph, task_pos["exeKG:hasInput"][0], self.dict_namespace)
                data_source = input["exeKG:hasSource"][0]
            elif len(task_pos["exeKG:hasInput"]) > 1:
                for i in task_pos["exeKG:hasInput"]:
                    input = parse_entity(self.graph, i, self.dict_namespace)
                    data_source.append(input["exeKG:hasSource"][0])
        except:
            data_source = task_pos["exeKG:hasInput"][0]

        # print('data_source = ', data_source)

        program = self.program

        # input data for current task
        try:
            input_data = self.raw_data[data_source]
        except:
            input_data = self.extra_data_list[task_pos["exeKG:hasInput"][0]]
        # print('input = ', input_data)

        method = task_pos["exeKG:hasMethod"][0]
        output = []
        if "trend" in method.lower():
            output = self.trend_calculation_method(data_source, 2, "same", program=program)
        elif "scatter" in method.lower():
            output = self.scattering_calculation(data_source, program=program)
        elif "iqr" in method.lower():
            output.append(self.iqr_calculation_method(self.raw_data[data_source], 25))
            output.append(self.iqr_calculation_method(self.raw_data[data_source], 75))
        elif "outlier" in method.lower():
            output = self.outlier_calculation(self.raw_data[data_source])
        elif "normalization" in method.lower():
            output = self.normalization_method(self.raw_data[data_source], data_source)
        elif "concatenation" in method.lower():
            output = self.concatenation_method(input_data, task_pos["exeKG:hasOutput"][0])
        elif "splitting" in method.lower():
            output = self.data_splitting(input_data, task_pos)
        else:
            print("ERROR: method not found!")

        return output
