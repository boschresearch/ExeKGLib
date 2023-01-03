"""CLI entry point."""

import typer

app = typer.Typer(name="cli", help="CLI entry point.", no_args_is_help=True, add_completion=False)


if __name__ == "__main__":
    app()
