<!-- markdownlint-disable MD046 -->

# Installation

## Step 0: `poetry`

This project is managed by [`poetry`][poetry], a Python packaging and dependency management tool.
This means, however, that `poetry` needs to be installed _before_ you can install this project.
To be honest, the official [`poetry` installation docs][poetry-install] are great and provide different ways to install
`poetry` on different platforms and under different conditions.

However, as some people are lazy, below you can find a few ways to install `poetry`.
As mentioned above:

**If your required / desired way of installation is not listed, go to the official [installation docs][poetry-install]**
before ranting! :pray:

=== "Linux"

    Run

    ```sh
    curl -sSL https://install.python-poetry.org | python3 -
    ```

    and follow the instructions.
    Finally, consider adding `poetry`'s installation path to your environment `PATH` (or similar), e.g. via

    ```sh
    export PATH=$PATH:$HOME/.local/bin
    ```

    for `poetry`'s default installation path.

=== "conda (not recommended)"

    If you really need to go through conda (I know in some cases that's the only option), try this:

    ```sh
    conda activate some-environment
    conda install pip
    pip install pipx
    pipx install poetry
    conda deactivate
    ```

## Step 1: Dependency Installation

The installation of the project's dependencies should be piece of :cake: in most cases by running

```sh
poetry install
```

from within the project directory.

!!! tip "No project development intended?"

    If you don't need any development setup, you can pass the `--no-dev` flag to skip the development dependencies.

??? fail "Computer says no…"

    In some cases, this does not work right away.
    Please find a collection of failure cases below (thanks for the feedback! :heart:)

    | What?                                 | Hint                                            |
    | :------------------------------------ | :---------------------------------------------- |
    | _"I get a `ConnectionError`"_         | Maybe you have proxy issues.                    |
    | _"I destroyed my poetry environment"_ | Delete the `.venv` folder and create a new env. |

## Step 2: Pre-commit Git Hooks Installation

To ensure compatibility of each future commit with the project's conventions (e.g. code format), some predefined git hooks should be installed by running the following commands.

```sh
poetry shell  # use the created poetry environment
pre-commit install
```

<!-- URLs -->
[poetry]: https://python-poetry.org/
[poetry-install]: https://python-poetry.org/docs/#installation
