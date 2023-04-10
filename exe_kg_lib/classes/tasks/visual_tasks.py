# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from abc import abstractmethod

from ...utils.task_utils.visual_utils import *
from ..entity import Entity
from ..task import Task

"""
❗ Important for contributors: See the package's README.md before extending the code's functionality.
"""


class CanvasTaskCanvasMethod(Task):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)
        self.grid = None
        self.fig = None
        self.has_layout = None
        self.has_canvas_name = None

    def run_method(self, *args):
        self.fig, self.grid = canvas_creation(self.has_layout)

        return None


class PlotTask(Task):
    def __init__(self, iri: str, parent_entity: Entity, canvas_method: CanvasTaskCanvasMethod):
        super().__init__(iri, parent_entity)
        self.fig = canvas_method.fig
        self.grid = canvas_method.grid

        self.has_legend_name = None
        self.has_layout = None
        self.has_y_label = None
        self.has_x_label = None
        self.has_y_lim = None
        self.has_x_lim = None
        self.has_line_style = None
        self.has_line_width = 1

    @abstractmethod
    def run_method(self, *args):
        raise NotImplementedError


class PlotTaskScatterplotMethod(PlotTask):
    def __init__(self, iri: str, parent_entity: Entity, canvas_method: CanvasTaskCanvasMethod):
        super().__init__(iri, parent_entity, canvas_method)
        self.has_scatter_size = None
        self.has_scatter_style = None

    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame):
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        input_data = list(input_dict.values())[0]  # one input expected
        scatter_plot(
            data=input_data,
            fig=self.fig,
            grid=self.grid,
            layout=self.has_layout,
            line_width=self.has_line_width,
            line_style=self.has_line_style,
            legend_name=self.has_legend_name,
            x_lim=self.has_x_lim,
            y_lim=self.has_y_lim,
            x_label=self.has_x_label,
            y_label=self.has_y_label,
        )

        return None


class PlotTaskLineplotMethod(PlotTask):
    def __init__(self, iri: str, parent_entity: Entity, canvas_method: CanvasTaskCanvasMethod):
        super().__init__(iri, parent_entity, canvas_method)

    def run_method(self, other_task_output_dict: dict, input_data: pd.DataFrame):
        input_dict = self.get_inputs(other_task_output_dict, input_data)
        input_data = list(input_dict.values())[0]  # one input expected
        line_plot(
            data=input_data,
            fig=self.fig,
            grid=self.grid,
            layout=self.has_layout,
            line_width=self.has_line_width,
            line_style=self.has_line_style,
            legend_name=self.has_legend_name,
            x_lim=self.has_x_lim,
            y_lim=self.has_y_lim,
            x_label=self.has_x_label,
            y_label=self.has_y_label,
        )

        return None
