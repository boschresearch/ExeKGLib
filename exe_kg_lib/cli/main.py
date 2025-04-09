# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

"""CLI entry point."""

import os
from distutils.dir_util import copy_tree
from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

from exe_kg_lib.classes.exe_kg_actors import (ExeKGConExe, ExeKGConstructor,
                                              ExeKGConstructorCLI,
                                              ExeKGExecutor)
from exe_kg_lib.utils.cli_utils import input_pipeline_info

app = typer.Typer(name="ML pipeline creation and execution", no_args_is_help=True)

HERE = Path(__file__).resolve().parent


@app.command()
def create_pipeline(json_path: Annotated[Optional[str], typer.Argument()] = None):
    if json_path:
        exe_kg = ExeKGConstructor()
        exe_kg.create_exe_kg_from_json(json_path)
        exe_kg.save_created_kg(HERE / ".." / ".." / "pipelines")

        return

    pipeline_name, input_data_path, input_plots_output_dir = input_pipeline_info()

    exe_kg = ExeKGConstructorCLI()
    exe_kg.start_pipeline_creation_cli(pipeline_name, input_data_path, input_plots_output_dir)
    exe_kg.save_created_kg(HERE / ".." / ".." / "pipelines")


@app.command()
def run_pipeline(path: str):
    if path.endswith(".ttl"):
        exe_kg = ExeKGExecutor()
    else:
        # file needs to be converted to ExeKG first
        exe_kg = ExeKGConExe()

    exe_kg.execute_pipeline(path)


@app.command()
def get_examples():
    examples_dir = HERE / ".." / ".." / "examples"

    copy_tree(str(examples_dir), "./examples")


if __name__ == "__main__":
    app()
