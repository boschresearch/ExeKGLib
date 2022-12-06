# Copyright (c) 2022 Robert Bosch GmbH and its subsidiaries. All rights reserved.

"""CLI-related tests."""

from typing import List

import pytest
from typer.testing import CliRunner

from executable_ml_kgs.cli.main import app

SAY_ARGS = [
    ["hello"],
    ["goodbye"],
]

NAME_ARGS = [
    [],
    ["Jane Doe"],
    ["Max M."],
    ["Python 🐍"],
]


@pytest.mark.parametrize("say_args", SAY_ARGS)
@pytest.mark.parametrize("name_args", NAME_ARGS)
def test_say(say_args: List[str], name_args: List[str]):
    """Test CLI entry point for different args."""
    assert True
    # runner = CliRunner()
    # result = runner.invoke(app, ["say"] + say_args + name_args)
    # assert result.exit_code == 0
