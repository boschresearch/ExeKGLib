import time
from cgitb import small
from cProfile import label

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.font_manager import FontProperties
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axisartist.parasite_axes import HostAxes, ParasiteAxes
from rdflib import Graph
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from utils import PipelineProcessor, execute_pipeline, parse_entity, parse_namespace, query


class Visualizer(PipelineProcessor):
    """the class for visualization pipeline"""

    def __init__(self, dir_out="./plots"):
        self.fig = None
        self.grid = None

        self.graph = Graph()
        self.raw_data = None
        self.dict_namespace = {}
        self.dir_out = dir_out
        self.program = None

        self.extra_data_list = {}

    def canvas_task(self, canvas_po: dict) -> tuple:
        """the canvas task taking as input the starting task POs and output the fig and grid"""

        font = FontProperties()
        font.set_size(10)
        font.set_name("Verdana")
        self.font = font
        self.figsize_default = (7, 5)
        self.dpi = 150
        try:
            self.figname = canvas_po["exeKG:hasCanvasName"]
        except:
            pass

        try:
            n_rows, n_cols = (int(i) for i in canvas_po["exeKG:hasLayout"][0].split(" "))
        except:
            n_rows, n_cols = (1, 1)
        fig = plt.figure(figsize=self.figsize_default)
        # if n_rows = n_cols = 1, then just single plot
        # otherwise subplot is expected
        grid = None if (n_rows == n_cols and n_rows == 1) else plt.GridSpec(n_rows, n_cols, hspace=0.3, wspace=0.3)
        self.fig = fig
        self.grid = grid
        return (fig, grid)

    def set_plot(self, task):
        """extract parameters for plot if exsiting"""
        style = task.get("exeKG:hasLineStyle", [None])[0]
        width = int(task.get("exeKG:hasLineWidth", [1])[0])
        y_label = task.get("exeKG:hasYaxis", ["Q-Value"])[0]
        x_label = task.get("exeKG:hasXaxis", ["Number of Welding Operations"])[0]
        x_lim = task.get("exeKG:hasXlim", [None])[0]
        y_lim = task.get("exeKG:hasYlim", [None])[0]
        legend_name = task.get("exeKG:hasLegendName", [None])[0]

        return (style, width, y_label, x_label, x_lim, y_lim, legend_name)

    def line_plot(
        self,
        fig: plt.figure = None,
        grid: plt.GridSpec = None,
        input_data: pd.DataFrame = [],
        task: dict = {},
    ):
        """line plot and add descriptions"""
        # extract settings
        style, width, y_label, x_label, x_lim, y_lim, legend_name = self.set_plot(task)
        input_data = input_data.dropna()

        # dynamic layout
        if grid == None:

            plt.plot(
                input_data.index,
                input_data,
                linestyle=style,
                linewidth=width,
                label=legend_name,
            )
            plt.xlim(x_lim)
            plt.ylim(y_lim)
            plt.xlabel(x_label)
            plt.ylabel(y_label)

        else:
            row_start, row_end, col_start, col_end = (int(i) for i in task["exeKG:hasLayout"][0].split())
            ax = fig.add_subplot(grid[row_start:row_end, col_start:col_end])
            # plot
            ax.plot(
                input_data.index,
                input_data,
                linestyle=style,
                linewidth=width,
                label=legend_name,
            )
            ax.set_xlim(x_lim)
            ax.set_ylim(y_lim)
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)

    def scatter_plot(
        self,
        fig: plt.figure = None,
        grid: plt.GridSpec = None,
        input_data: pd.DataFrame = [],
        task: dict = {},
        label: str = None,
    ):
        # plot settings
        style, width, y_label, x_label, x_lim, y_lim, legend_name = self.set_plot(task)
        legend_name = legend_name or label
        # dynamic layout
        # print('input.index = ',input_data.index)
        # print('input = ', input)

        if grid == None:

            plt.scatter(
                input_data.index,
                input_data,
                s=int(width * 10),
                marker=style,
                linewidth=width,
                label=legend_name,
            )
            plt.xlim(x_lim)
            plt.ylim(y_lim)
            plt.xlabel(x_label)
            plt.ylabel(y_label)

        else:
            row_start, row_end, col_start, col_end = (int(i) for i in task["exeKG:hasLayout"][0].split())
            ax = fig.add_subplot(grid[row_start:row_end, col_start:col_end])

            # plot
            ax.scatter(
                input_data.index,
                input_data,
                s=width * 3,
                marker=style,
                label=legend_name,
                color="red",
            )
            ax.set_xlim(x_lim)
            ax.set_ylim(y_lim)
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)

    def plot_multiple(self, plot_tasks: list, fig, grid):
        """multiple subplots in a single figure"""
        input_data = self.raw_data
        plot_data = []

        for i, task in enumerate(plot_tasks):
            # identify input data
            input = task["exeKG:hasInput"][0]
            data = parse_entity(self.graph, input, self.dict_namespace)
            data_source = data["exeKG:hasSource"][0]

            # identify plot type
            # TODO: adjust the parse by the ontology
            # plot_po = []
            # for key in plot_keys:
            #     plot_po = parse_entity(key)
            #     print(plot_po)

            # set other properties
            # if('exeKG:hasYName' in plot_po):
            #     plt.ylabel(plot_po['exeKG:hasYName'][0])
            # if('exeKG:hasXName' in plot_po):
            #     plt.xlabel(plot_po['exeKG:hasXName'][0])

            if data_source not in input_data:
                print(f"desired data: {data_source} not found in the csv file!")
                continue
            if "Line" in task["exeKG:hasMethod"][0]:
                # print("plotting data_source: ", data_source)
                self.line_plot(fig, grid, input_data[data_source], task)
            elif "Scatter" in task["exeKG:hasMethod"][0]:
                # print("plotting data_source: ", data_source)
                self.scatter_plot(fig, grid, input_data[data_source], task)
            # ax = fig.add_subplot(grid[0:1, 1:2])
            # ax.plot([1,2,3],[1,2,3])
        plt.legend()
        plt.show()

    def plot_task(self, plot_task: dict, fig, grid, out_name):
        """multiple lines in a single plot
        Args:
            plot_tasks:
                the list of dict, where each dict represent a plot task with the queried Ps and Os
        """
        input_data = self.raw_data

        # for i, task in enumerate(plot_tasks):
        # identify input data
        task = plot_task
        # print('task = ', task)
        task_input = task["exeKG:hasInput"][0]
        data = parse_entity(self.graph, task_input, self.dict_namespace)
        input_source = data["exeKG:hasSource"][0]

        plot_data = []

        # TODO: used for QValueActual, rewrite afterwards
        # select the program of QVALUE accordingly
        if input_source == "QVALUEActual":
            # if(not self.program):
            #     plot_data = input_data[input_source]/input_data['QVALUESetpoint']
            #     plot_data = plot_data[input_data['WeldingProgramNumber']!=251]
            # else:
            plot_data = self.welding_program_filter(
                input_data[input_source] / input_data["QVALUESetpoint"], self.program
            )
        else:
            plot_data = self.welding_program_filter(input_data[input_source], self.program)

        # skip the not existing input_data
        if input_source not in input_data:
            print(f"desired data: {input_source} not found in the csv file!")
            return

        # only 2 plot types according to method type
        if task["exeKG:hasMethod"][0] == "exeKG:LineplotMethod0":
            # print("plotting input_source: ", input_source)
            self.line_plot(fig, grid, plot_data, task)
        elif task["exeKG:hasMethod"][0] == "exeKG:ScatterplotMethod0":
            # print("plotting input_source: ", input_source)
            self.scatter_plot(fig, grid, plot_data, task)

    # TODO: maybe move the query inside this execution, take only name as input?
    def execute_task(self, task_pos):
        """distinguish between canvas task, line_plot task and scatter plot task

        return: Empty list, which is not needed for now
        """
        # print(task_pos)
        method = task_pos["exeKG:hasMethod"][0]

        if "canvas" in method.lower():
            self.canvas_task(task_pos)
            return

        input = parse_entity(self.graph, task_pos["exeKG:hasInput"][0], self.dict_namespace)
        try:
            data_source = input["exeKG:hasSource"][0]
            input_data = self.raw_data[data_source]
        except:
            input_data = self.extra_data_list[task_pos["exeKG:hasInput"][0]]

        method = task_pos["exeKG:hasMethod"][0]

        if "line" in method.lower():
            self.line_plot(input_data=input_data)
        elif "scatter" in method.lower():
            self.scatter_plot(input_data=input_data)

        # output = []
        # self.plot_task(task_pos, self.fig, self.grid, self.dir_out)

        # if('line' in method.lower()):
        #     output = self.line_plot(self.fig, self.grid, input_data=input_data )
        # elif('scatter' in method.lower()):
        #     output = self.scatter_plot(self.fig, self.grid, input_data=input_data)
        # else:
        #     print('wrong method')

        return


def visu_pipeline(
    raw_data_path=r"data/singlefeatures_wm1.csv",
    ontology_path=r"kg/testVisualKG.ttl",
    debug=True,
    out_name="plot.jpg",
    show=False,
    **kwargs,
):
    """visu task pipeline for debugging"""

    # 1. build current knowledge graph

    visualizer = Visualizer()
    visualizer.load_graph(ontology_path)
    visualizer.load_data(raw_data_path)
    visualizer.program = kwargs.get("program", None)

    if debug:
        print(visualizer.graph)
        print(visualizer.raw_data)

    start_time = time.time()

    # 2. namespace dictionary for mapping namespaces to shortcuts
    visualizer.dict_namespace = parse_namespace(visualizer.graph)
    if debug:
        print(visualizer.dict_namespace)

    # 3. query the visu pipeline
    graph = visualizer.graph
    cquery = "\nSELECT ?s WHERE {?s rdf:type exeKG:Pipeline}"
    visu_pipeline = query(visualizer.graph, cquery, visualizer.dict_namespace)

    if debug:
        print("visu_pipeline:", visu_pipeline)

    # 4. construct the canvas task + plot task
    execute_pipeline(visu_pipeline, True, visualizer=visualizer)

    # for pipeline_name in visu_pipeline:
    #     pipeline_po = parse_entity(visualizer.graph, pipeline_name, visualizer.dict_namespace)
    #     if(debug):
    #         print('pipeline_property_object: ',pipeline_po)

    #     # 4.1 the starting task, normally Canvas Task
    #     start_po = parse_entity(visualizer.graph, pipeline_po['exeKG:hasStartTask'][0], visualizer.dict_namespace)
    #     if(debug):
    #         print('starting_task_property_object: ', start_po)

    #     fig, grid = visualizer.canvas_task(start_po)

    #     # 4.2 for the rest of the following plot tasks
    #     plot_tasks = []
    #     task_po = start_po
    #     while('exeKG:hasNextTask' in task_po):
    #         # append each task with corresponding properties to the plot_tasks
    #         next_task = task_po['exeKG:hasNextTask'][0]
    #         task_po = parse_entity(visualizer.graph, next_task, visualizer.dict_namespace)
    #         if(task_po):
    #             plot_tasks.append(task_po)
    #             visualizer.plot_task(task_po, fig, grid, out_name)
    #     print("plot_tasks: ", plot_tasks)

    # plt.savefig(visualizer.dir_out + r'/'+ out_name)
    end_time = time.time()
    print("total time for visu_pipeline = ", end_time - start_time)

    if show:
        plt.legend()
        plt.show()

    return end_time - start_time


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


def stats_visu_pipeline(
    raw_data_path=r"data/singlefeatures_wm1.csv",
    ontology_path=r"kg/testStatsVisuKG.ttl",
    debug=False,
    out_name="statistics.jpg",
    show=False,
    **kwargs,
):
    """the statistics pipeline for debugging only, currently outlier detection pipeline from the paper"""

    # 1. build current knowledge graph
    program = kwargs.get("program", "")
    program = "" if (program is None) else program
    statistics_analyzer = StatsiticsAnalyzer()
    statistics_analyzer.program = program
    statistics_analyzer.load_graph(ontology_path)
    statistics_analyzer.load_data(raw_data_path)
    data_source = "QVALUEActual"
    selected_rows = statistics_analyzer.select_program(program, "WeldingProgramNumber")
    visu = Visualizer()

    start_time = time.time()

    # 2. namespace dictionary for mapping namespaces to shortcuts
    statistics_analyzer.dict_namespace = parse_namespace(statistics_analyzer.graph)
    # print(statistics_analyzer.dict_namespace)

    # 3. query the stats pipeline
    graph = statistics_analyzer.graph
    # cquery = "\nSELECT ?s WHERE {?s rdf:type exeKG:Pipeline}"
    cquery = "\nSELECT ?s WHERE {?s rdf:type :Pipeline}"
    stats_pipelines = query(graph, cquery, statistics_analyzer.dict_namespace)

    # 4. execute pipeline
    # for i in execute_pipeline(stats_pipelines, statistics_analyzer, True):
    #     print('i = ', i)
    execute_pipeline(stats_pipelines, True, statistics_analyzer=statistics_analyzer)

    # print(statistics_analyzer.extra_data_list)
    # print(statistics_analyzer.raw_data)

    print(statistics_analyzer.extra_data_list)
    for i in statistics_analyzer.extra_data_list:
        visu.scatter_plot(input_data=statistics_analyzer.raw_data[i], label=i)

    end_time = time.time()
    print("stats_visu_pipeline time = ", end_time - start_time)

    plt.xlim([-10, 5000])
    plt.ylim([-50, 150])
    plt.xlabel("Number of Wielding operations")
    plt.ylabel("Q-Value")

    if show:
        plt.legend()
        plt.show()
    return end_time - start_time


class MLAnalyser(PipelineProcessor):
    def __init__(self, dir_out="./plots"):
        self.fig = None
        self.grid = None

        self.graph = Graph()
        self.raw_data = None
        self.dict_namespace = {}
        self.dir_out = dir_out
        self.program = None

        self.model = None
        self.extra_data_list = {}

    def LR_training(self, input_x: list, input_y: list, task_pos):
        reg = LinearRegression()
        reg.fit(input_x, input_y)
        self.model = reg
        predicted_y = reg.predict(input_x)
        # print('input_x = ', input_x)
        # print('predicted_y = ', len(predicted_y))
        # print('input_y = ', len(input_y))
        # plt.plot(predicted_y, label = 'predicted')
        # plt.plot(input_y, label = 'input')

        out_names = task_pos["exeKG:hasOutput"]
        for name in out_names:
            if "Predict" in name:
                self.extra_data_list[name] = predicted_y

        # plt.legend()
        # plt.show()
        print("LR training finished")

    def LR_testing(self, input_x: list, input_y: list, task_pos):
        reg = self.model
        assert not reg is None
        assert isinstance(reg, LinearRegression)
        predict_y = reg.predict(input_x)
        # plt.plot(input_y.index ,predict_y, label = 'predict')
        # plt.plot(input_y.index, input_y, label = 'input_y')

        out_names = task_pos["exeKG:hasOutput"]
        for name in out_names:
            if "Predict" in name:
                self.extra_data_list[name] = predict_y

        # print(self.extra_data_list)

        # plt.legend()
        # plt.show()

    def k_nearest_neighbor_train(self, input_x, input_y, task_pos, n_neighbors=3):
        print("n_neighbors = ", n_neighbors)
        knn = KNeighborsRegressor(n_neighbors=n_neighbors)
        knn.fit(input_x, input_y)

        self.model = knn
        predicted_y = knn.predict(input_x)

        out_names = task_pos["exeKG:hasOutput"]
        for name in out_names:
            if "Predict" in name:
                self.extra_data_list[name] = predicted_y

        print("KNN training finished")

    def k_nearest_neighbor_test(self, input_x, input_y, task_pos):
        knn = self.model
        assert isinstance(knn, KNeighborsRegressor)

        predicted_y = knn.predict(input_x)

        out_names = task_pos["exeKG:hasOutput"]
        for name in out_names:
            if "Predict" in name:
                self.extra_data_list[name] = predicted_y

        print("KNN testing finished")

    def mlp_train(self, input_x, input_y, task_pos, solver="adam"):
        mlp = MLPRegressor(solver=solver)
        mlp.fit(input_x, input_y)

        self.model = mlp
        predicted_y = mlp.predict(input_x)

        out_names = task_pos["exeKG:hasOutput"]
        for name in out_names:
            if "Predict" in name:
                self.extra_data_list[name] = predicted_y

        print("MLP training finished")

    def mlp_test(self, input_x, input_y, task_pos):
        mlp = self.model
        assert isinstance(mlp, MLPRegressor)

        predicted_y = mlp.predict(input_x)

        out_names = task_pos["exeKG:hasOutput"]
        for name in out_names:
            if "Predict" in name:
                self.extra_data_list[name] = predicted_y

        print("MLP testing finished")

    def ml_performance_calculation(self, task_pos):
        model = self.model
        inputs = task_pos["exeKG:hasInput"]

        real_train = 0
        real_test = 0
        predict_train = 0
        predict_test = 0

        print("inputs = ", inputs)
        for input in inputs:
            if "Train" in input and "Predict" in input:
                predict_train = self.extra_data_list[input]
            elif "Test" in input and "Predict" in input:
                predict_test = self.extra_data_list[input]
            elif "Train" in input and "Split" in input:
                real_train = self.extra_data_list[input]
                real_train = real_train[real_train.columns[-1]]
            elif "Test" in input and "Split" in input:
                real_test = self.extra_data_list[input]
                real_test = real_test[real_test.columns[-1]]

        # print(real_test)
        # print(predict_train)
        train_err = pd.DataFrame(real_train - predict_train)
        test_err = pd.DataFrame(real_test - predict_test)

        # print('train_err = ', train_err)
        # print('test_err = ', test_err)

        # plt.plot(train_err.index, train_err, label = 'train')
        # plt.plot(test_err.index, test_err, label = 'test')
        # plt.legend()
        # plt.show()

        outputs = task_pos["exeKG:hasOutput"]
        for output in outputs:
            if "Test" in output:
                self.extra_data_list[output] = test_err
            elif "Train" in output:
                self.extra_data_list[output] = train_err
            else:
                pass

        print("ml_performance_calculation finished")

    def execute_task(self, task_pos):
        """task of ML"""
        method = task_pos["exeKG:hasMethod"][0]

        input = task_pos["exeKG:hasInput"][0]
        temp = parse_entity(self.graph, input, self.dict_namespace)

        print("temp = ", temp)

        # print(self.extra_data_list)
        try:
            input_source = temp["exeKG:hasSource"][0]
            input_data = self.raw_data[input_source]
        except:
            input_data = self.extra_data_list[input]

        if "LRTrain" in method:
            x = input_data[input_data.columns[:-1]]
            y = input_data[input_data.columns[-1]]
            self.LR_training(x, y, task_pos)
        elif "LRTest" in method:
            x = input_data[input_data.columns[:-1]]
            y = input_data[input_data.columns[-1]]
            self.LR_testing(x, y, task_pos)
        elif "KNNTrain" in method:
            x = input_data[input_data.columns[:-1]]
            y = input_data[input_data.columns[-1]]
            self.k_nearest_neighbor_train(x, y, task_pos, num_exps)
        elif "KNNTest" in method:
            x = input_data[input_data.columns[:-1]]
            y = input_data[input_data.columns[-1]]
            self.k_nearest_neighbor_test(x, y, task_pos)
        elif "MLPTrain" in method:
            x = input_data[input_data.columns[:-1]]
            y = input_data[input_data.columns[-1]]
            self.mlp_train(x, y, task_pos, num_exps)
        elif "MLPTest" in method:
            x = input_data[input_data.columns[:-1]]
            y = input_data[input_data.columns[-1]]
            self.mlp_test(x, y, task_pos)
        elif "Performance" in method:
            self.ml_performance_calculation(task_pos)
        else:
            print("execute ML task")


def ML_pipeline(
    raw_data_path=r"data/singlefeatures_wm1.csv",
    ontology_path=r"KG_ML/exeKGExample.ttl",
    debug=True,
    out_name="statistics_extract.jpg",
    show=False,
    exp=3,
):
    """ML_pipeline for debugging only"""
    global num_exps
    num_exps = exp
    # 1. init
    ml_analyser = MLAnalyser()
    ml_analyser.load_data(raw_data_path)
    ml_analyser.load_graph(ontology_path)
    ml_analyser.parse_namespace()

    visualizer = Visualizer()
    visualizer.raw_data = ml_analyser.raw_data
    visualizer.graph = ml_analyser.graph
    visualizer.dict_namespace = ml_analyser.dict_namespace
    visualizer.extra_data_list = ml_analyser.extra_data_list

    statistics_analyzer = StatsiticsAnalyzer()
    statistics_analyzer.raw_data = ml_analyser.raw_data
    statistics_analyzer.graph = ml_analyser.graph
    statistics_analyzer.dict_namespace = ml_analyser.dict_namespace
    statistics_analyzer.extra_data_list = ml_analyser.extra_data_list

    start_time = time.time()
    # 2. query pipeline
    cquery = "\nSELECT ?s WHERE {?s rdf:type :Pipeline}"
    stats_pipelines = query(ml_analyser.graph, cquery, ml_analyser.dict_namespace)
    # print(stats_pipelines)

    # 3. execute pipeline
    execute_pipeline(
        stats_pipelines,
        True,
        visualizer=visualizer,
        statistics_analyzer=statistics_analyzer,
        ML_analyser=ml_analyser,
    )

    # print(ml_analyser.extra_data_list)
    end_time = time.time()

    if show:
        plt.legend()
        plt.show()

    return end_time - start_time


def main_ml_visu():

    # stats_visu_pipeline(program=1)#, show=True)
    # visu_pipeline(debug=False, out_name="Qvalue_line.jpg", program = 2)#, program=2)
    # visu_pipeline(debug=False, out_name="Qvalue_line.jpg", program=1)
    # visu_pipeline(r'data/singlefeatures_wm1.csv', r'KG/testVisualKG_scatter.ttl', True, out_name="Qvalue_scatter.jpg", scatter=True)
    ML_pipeline(ontology_path=r"KG_ML/exeKGExampleKNN.ttl", show=False)

    knn_kg_path = r"KG_ML/exeKGExampleKNN.ttl"
    time1 = []
    for i in range(10):
        time1.append(
            ML_pipeline(
                raw_data_path=r"data/singlefeatures_wm1.csv",
                ontology_path=knn_kg_path,
                show=False,
                exp=i + 3,
            )
        )
        # time.append(stats_visu_pipeline(program=1, debug=False, show=True))
        # time.append(visu_pipeline(debug=False, out_name="Qvalue_line.jpg"))#, show=True))

    print(time1)

    ##### MLP hyperparameters
    mlp_kg_path = r"KG_ML/exeKGExampleMLP.ttl"
    time2 = []
    for i in range(3):
        solver = ["lbfgs", "sgd", "adam"]
        for j in range(4):
            time2.append(
                ML_pipeline(
                    raw_data_path=r"data/singlefeatures_wm1.csv",
                    ontology_path=mlp_kg_path,
                    show=False,
                    exp=solver[i],
                )
            )
        # time.append(stats_visu_pipeline(program=1, debug=False, show=True))
        # time.append(visu_pipeline(debug=False, out_name="Qvalue_line.jpg"))#, show=True))

    print(time2)


def main_visu(input_path=r"kg/testVisualKG.ttl"):
    visu_pipeline(debug=False, out_name="Qvalue_line.jpg", program=1)
    times = []
    visu_ontology = input_path
    for i in range(3):
        times.append(
            visu_pipeline(
                ontology_path=visu_ontology,
                debug=False,
                out_name="Qvalue_line.jpg",
                program=1,
            )
        )
    for i in range(3):
        times.append(
            visu_pipeline(
                ontology_path=visu_ontology,
                debug=False,
                out_name="Qvalue_line.jpg",
                program=2,
            )
        )
    for i in range(4):
        times.append(
            visu_pipeline(
                ontology_path=visu_ontology,
                debug=False,
                out_name="Qvalue_line.jpg",
                program=None,
            )
        )
    print(times)


def main_visu_stats(input_path=r"kg/testStatsVisuKG.ttl"):
    visu_pipeline(debug=False, out_name="Qvalue_line.jpg", program=1)
    times = []
    for i in range(10):
        # time1.append(ML_pipeline(raw_data_path = r'data/singlefeatures_wm1.csv', ontology_path=input_path, show=False, exp = i+3))
        times.append(stats_visu_pipeline(program=1, debug=False, show=False))
        # time.append(visu_pipeline(debug=False, out_name="Qvalue_line.jpg"))#, show=True))

    print(times)


def main_stats(input_path=r"kg/testStatsOnly.ttl"):
    visu_pipeline(debug=False, out_name="Qvalue_line.jpg", program=1)
    times = []
    for i in range(10):
        # time1.append(ML_pipeline(raw_data_path = r'data/singlefeatures_wm1.csv', ontology_path=input_path, show=False, exp = i+3))
        times.append(stats_visu_pipeline(debug=False, show=False))
        # time.append(visu_pipeline(debug=False, out_name="Qvalue_line.jpg"))#, show=True))

    print(times)


def main_stats_ML():
    ML_pipeline(ontology_path=r"KG_ML/exeKGExampleKNN.ttl", show=False)

    # LR
    knn_kg_path = r"KG_ML/exeKGExampleLR_noVisu.ttl"
    time0 = []
    for i in range(10):
        time0.append(
            ML_pipeline(
                raw_data_path=r"data/singlefeatures_wm1.csv",
                ontology_path=knn_kg_path,
                show=False,
                exp=i + 3,
            )
        )

    # knn
    knn_kg_path = r"KG_ML/exeKGExampleKNN_noVisu.ttl"
    time1 = []
    for i in range(10):
        time1.append(
            ML_pipeline(
                raw_data_path=r"data/singlefeatures_wm1.csv",
                ontology_path=knn_kg_path,
                show=False,
                exp=i + 3,
            )
        )

    ##### MLP hyperparameters
    mlp_kg_path = r"KG_ML/exeKGExampleMLP_noVisu.ttl"
    time2 = []
    for i in range(3):
        solver = ["lbfgs", "sgd", "adam"]
        for j in range(4):
            time2.append(
                ML_pipeline(
                    raw_data_path=r"data/singlefeatures_wm1.csv",
                    ontology_path=mlp_kg_path,
                    show=False,
                    exp=solver[i],
                )
            )
        # time.append(stats_visu_pipeline(program=1, debug=False, show=True))
        # time.append(visu_pipeline(debug=False, out_name="Qvalue_line.jpg"))#, show=True))

    print(time0)
    print(time1)
    print(time2)


if __name__ == "__main__":

    # main_stats_ML()
    # main_stats()
    main_visu()
    # main_ml()
    # main_visu_stats()
