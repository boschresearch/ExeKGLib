import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
from rdflib import Graph

from utils import parse_entity
from classes.pipeline_execution.pipeline_processor import PipelineProcessor


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
