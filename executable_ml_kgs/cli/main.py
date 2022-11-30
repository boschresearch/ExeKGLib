# Copyright (c) 2022 Robert Bosch GmbH and its subsidiaries. All rights reserved.

"""CLI entry point."""

import typer

from executable_ml_kgs.cli import say

app = typer.Typer(name="cli", help="CLI entry point.", no_args_is_help=True, add_completion=False)
app.add_typer(typer_instance=say.app)


if __name__ == "__main__":
    app()
