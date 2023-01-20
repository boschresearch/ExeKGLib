# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from typing import Optional, Tuple

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties


def canvas_creation(layout: str) -> Tuple[Figure, Optional[plt.GridSpec]]:
    """the canvas task taking as input the starting task POs and output the fig and grid"""

    font = FontProperties()
    font.set_size(10)
    font.set_name("Verdana")

    try:
        n_rows, n_cols = (int(i) for i in layout[0].split(" "))
    except:
        n_rows, n_cols = (1, 1)

    fig = plt.figure(figsize=(7, 5))

    grid = None if (n_rows == n_cols and n_rows == 1) else plt.GridSpec(n_rows, n_cols, hspace=0.3, wspace=0.3)

    return fig, grid


# def scatter_plot(data: pd.Series, fig: Figure, grid: plt.GridSpec, layout: str, line_width: str, line_style: str,
#                  legend_name: str, x_lim: str, y_lim: str, x_label: str, y_label: str):
def scatter_plot(**kwargs):
    plot_creation("scatter", **kwargs)


def line_plot(**kwargs):
    plot_creation("line", **kwargs)


def plot_creation(
    plot_type: str,
    data: pd.Series,
    fig: Figure,
    grid: plt.GridSpec,
    layout: str,
    line_width: str,
    line_style: str,
    legend_name: str,
    x_lim: str,
    y_lim: str,
    x_label: str,
    y_label: str,
):
    plot = plt
    if grid is not None:
        row_start, row_end, col_start, col_end = (int(i) for i in layout.split())
        plot = fig.add_subplot(grid[row_start:row_end, col_start:col_end])

    if plot_type == "line":
        plot.plot(
            data.index,
            data,
            linestyle=line_style,
            linewidth=int(line_width),
            label=legend_name,
        )
    elif plot_type == "scatter":
        plot.scatter(
            data.index,
            data,
            s=int(int(line_width) * 10),
            marker=line_style,
            linewidth=int(line_width),
            label=legend_name,
        )
    else:
        print("Invalid plot type given")

    if grid is None:
        plot.xlim(x_lim)
        plot.ylim(y_lim)
        plot.xlabel(x_label)
        plot.ylabel(y_label)
    else:
        plot.set_xlim(x_lim)
        plot.set_ylim(y_lim)
        plot.set_xlabel(x_label)
        plot.set_ylabel(y_label)

    plt.legend()
    plt.show()
