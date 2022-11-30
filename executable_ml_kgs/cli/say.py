# Copyright (c) 2022 Robert Bosch GmbH and its subsidiaries. All rights reserved.

"""'say' commands."""

import typer

app = typer.Typer(name="say", help="Say something.", no_args_is_help=True)

DEFAULT_NAME = typer.Argument(default="stranger", help="The person to say 'Hello' to.")


@app.command()
def hello(name: str = DEFAULT_NAME) -> None:
    """Says 'Hello' to someone."""

    typer.secho(f"Hello, {name}!", fg="green")


@app.command()
def goodbye(name: str = DEFAULT_NAME) -> None:
    """Says 'Goodbye' to someone."""

    typer.secho(f"Goodbye, {name}!", fg="blue")
