# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

"""CLI entry point."""

import os
from distutils.dir_util import copy_tree

import typer

from exe_kg_lib import ExeKG
from exe_kg_lib.utils.cli_utils import input_pipeline_info

app = typer.Typer(name="ML pipeline creation and execution", no_args_is_help=True)


@app.command()
def create_pipeline():
    pipeline_name, input_data_path = input_pipeline_info()

    exe_kg = ExeKG()
    exe_kg.start_pipeline_creation(pipeline_name, input_data_path)
    exe_kg.save_created_kg(f"pipelines/{pipeline_name}.ttl")


@app.command()
def run_pipeline(path: str):
    exe_kg = ExeKG(input_exe_kg_path=path)
    exe_kg.execute_pipeline()


@app.command()
def get_examples():
    current_dir = os.path.dirname(__file__)
    examples_dir = os.path.join(current_dir, "..", "..", "examples")

    copy_tree(examples_dir, "./examples")


if __name__ == "__main__":
    app()
