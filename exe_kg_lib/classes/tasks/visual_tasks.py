# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from abc import abstractmethod
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt

from ...utils.task_utils.visual_utils import *
from ..entity import Entity
from ..task import Task

"""
❗ Important for contributors: See the package's README.md before extending the code's functionality.
"""


class CanvasCreation(Task):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)
        self.fig = None
        self.grid = None
        self.current_plot_pos = 0
        # self.layout = None
        # self.canvas_name = None

    def run_method(self, *args):
        n_rows, n_cols = (
            [int(i) for i in self.method_params_dict["layout"].split(" ")]
            if "layout" in self.method_params_dict
            else (1, 1)
        )

        figsize = (
            [int(i) for i in self.method_params_dict["figure_size"].split(" ")]
            if "figure_size" in self.method_params_dict
            else (7, 5)
        )

        self.fig = plt.figure(figsize=(figsize))
        self.grid = None if (n_rows == n_cols and n_rows == 1) else plt.GridSpec(n_rows, n_cols, hspace=0.3, wspace=0.3)


class Plotting(Task):
    def __init__(self, iri: str, parent_entity: Entity, plots_output_dir: str, canvas_task: CanvasCreation):
        super().__init__(iri, parent_entity)
        self.fig = canvas_task.fig
        self.grid = canvas_task.grid
        self.current_plot_pos = canvas_task.current_plot_pos
        self.layout = canvas_task.method_params_dict["layout"]
        self.plots_output_dir = plots_output_dir

        canvas_task.current_plot_pos += 1

    @abstractmethod
    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame):
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        input_data = input_dict["DataInToPlot"]
        # input_labels = input_dict["DataInPlotLabels"]

        method_module = self.resolve_module(module_name_to_snakecase=True)
        if "matplotlib" in method_module.__module__:
            plot = None
            if self.grid is not None:
                plot = self.fig.add_subplot(self.grid[self.current_plot_pos])

            for input in input_data:
                input_name = input["name"]
                input_value = input["value"]

                x = input_value.index if isinstance(input_value, pd.DataFrame) else input_name
                y = input_value

                method_to_call = method_module if plot is None else getattr(plot, method_module.__name__)
                method_to_call(x, y, **self.method_params_dict)
                if plot is not None:
                    if "title" in self.method_inherited_params_dict:
                        plot.set_title(self.method_inherited_params_dict["title"])
                    if "x_label" in self.method_inherited_params_dict:
                        plot.set_xlabel(self.method_inherited_params_dict["x_label"])
                    if "y_label" in self.method_inherited_params_dict:
                        plot.set_ylabel(self.method_inherited_params_dict["y_label"])
                    if "hasParamLegendName" in self.method_inherited_params_dict:
                        plot.legend(title=self.method_inherited_params_dict["hasParamLegendName"])
                else:
                    if "title" in self.method_inherited_params_dict:
                        plt.title(self.method_inherited_params_dict["title"])
                    if "x_label" in self.method_inherited_params_dict:
                        plt.xlabel(self.method_inherited_params_dict["hasParamXLabel"])
                    if "y_label" in self.method_inherited_params_dict:
                        plt.ylabel(self.method_inherited_params_dict["hasParamYLabel"])
                    if "hasParamLegendName" in self.method_inherited_params_dict:
                        plt.legend(title=self.method_inherited_params_dict["hasParamLegendName"])

            output_dir = Path(self.plots_output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_dir / f"{self.name}_plot.png")
            print(f"Plot saved in {output_dir / f'{self.name}_plot.png'}")
        else:
            raise NotImplementedError("Only matplotlib library is supported for now")
