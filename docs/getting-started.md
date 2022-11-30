<!-- markdownlint-disable MD046 -->
<!-- markdownlint-disable-next-line MD041 -->
## Overview

This project contains Python modules (project directory) and corresponding tests of these modules in the `tests` directory.
The `pyproject.toml` file contains all relevant project configuration. Please see [the `poetry` docs][poetry-pyproject] for
an overview of the `pyproject.toml` sections & fields. The `docs` directory and `mkdocs.yaml` file contain all
information to build the project documentation. The `poetry.toml` and `poetry.lock` files contain
[`poetry`][poetry]-specific information. It's important to know that `poetry.lock` _exactly defines_ the dependency
versions and thus enables deterministic builds.

??? info "Project File / Directory Structure"

    | File / Directory            | Purpose                                                                  |
    | --------------------------- | ------------------------------------------------------------------------ |
    | `.github`                   | CI/CD/release workflow definitions and a PR template                     |
    | `executable_ml_kgs` | Project import modules                                                   |
    | `docs`                      | Documentation directory (better write docs there instead of `README.md`) |
    | `tests`                     | Python module unit- & integration tests                                  |
    | `.pre-commit-config.yaml`   | `git` hook definitions comsumed by `pre-commit`                          |
    | `LICENSE`                   | The license in its long form                                             |
    | `mkdocs.yml`                | Documentation config consumed by `mkdocs`                                |
    | `pyproject.toml`            | Project information, (dev-) dependencies and task runner configuration   |
    | `README.md`                 | General project overview, displayed when visiting GitHub repository      |

## Dependency Management & Packaging

To keep the dependencies of different projects from interfering with each other, it is highly recommended to create an
own python environment for every project. We use [`poetry`][poetry] to address this issue. By running `poetry install`,
a separate virtual environment is created automatically into which all your dependencies are installed. This is similar
to running `pip install -r requirements.txt` in an isolated virtual environment. Afterwards you can run any command
within the virtual environment by simply calling

```sh
poetry run <command>
```

such as `poetry run pylint`.

### Deploying Packages to Artifactory

If you want to release your software to make it available to others, you need to create a new git tag using [semantic versioning].
If you push this tag to the GitHub remote, it will trigger a [GitHub workflow] to build the Python package and upload it
to the Artifactory repository.

!!! attention "Artifactory access"

    In order to be able to push to an Artifactory, you need access to it. Check [this guide][artifactory-access] on how
    to manage access.

To enable automatic package deployment to Artifactory, different Artifactory credentials need to be available depending
on the organization your project was created in: E.g. for `bios-bcai` the secrets `ARTIFACTORY_RESOURCE_USER` and
`ARTIFACTORY_RESOURCE_TOKEN` must be provided to GitHub Action workflows, while for `bcai-internal` the secrets
`BDC_ARTIFACTORY_USER` and `BDC_ARTIFACTORY_TOKEN` are used. You can
[check in the repository settings tab][settings-secrets] if the secrets are available or add them otherwise.

Finally, enable the deployment step in your CD GitHub Actions workflow located at `.github/workflows/cd.yaml`.

## Task Runner

We define common tasks (e.g. executed in commit hooks and CI) with [`poe`][poe], a task runner that allows defining
tasks in the `pyproject.toml` file.

??? info "Available tasks"

    You can get a list of available tasks by running `poetry run poe --help`:

    ```sh
    --8<-- "docs/exported/poe-options.txt"
    ```

In the following, we explain the most frequently used tasks in more detail.

### Formatting

Calling

```sh
poetry run poe format
```

formats Python code in-place using [`black`][black] and [`isort`][isort].

### Linting

Running

```sh
poetry run poe lint
```

checks the Python code base using [`pylint`][pylint] & `mypy`[mypy]. This task will fail if there are errors or if the
code quality score is below the `tool.pylint.master.fail-under` threshold defined in the `pyproject.toml` file.

### Testing

Running

```sh
poetry run poe test
```

will run [pytest][pytest], compute the test [coverage][coverage] and fail if below the minimum coverage defined by the
`tool.coverage.report.fail_under` threshold in the `pyproject.toml` file.

### Documentation

The code documentation is based on [`mkdocs`][mkdocs] which converts markdown files into a nicely-rendered web-page. In
particular, we use the awesome [`mkdocs-material`][mkdocs-material] package which offers more than just theming.
To generate documentation for different versions, [`mike`][mike] is used as a plugin within [`mkdocs`][mkdocs].

To generate the docs, run

```sh
poetry run poe docs
```

The documentation features:

- _Getting Started_ page set as home page
- Changelog
- API reference
- Contributing guideline
- Test summary & coverage report
- Project license & list of third-party dependencies with their licenses

To deploy the docs to the `gh-pages` remote branch run

```sh
poetry run poe deploy-docs --push --alias <alias>
```

where `<alias>` may be e.g. `latest`, `stable` or `my-awesome-temporary-branch`.

## Git Hooks

We use [`pre-commit`][pre-commit] to run git hooks helping you to develop high-quality code.
The hooks are configured in the `.pre-commit-config.yaml` file and executed before commit.

!!! info "Installation"

    After you cloned this project and plan to develop in it, don't forget to install these hooks via

    ```sh
    poetry run pre-commit install
    ```

??? example "Available pre-commit hooks"

    As you can see below, `poe` tasks are mostly reused to get consistent results across manual execution, git hooks & [CI](#github-workflows).

    ```yaml
    --8<-- ".pre-commit-config.yaml"
    ```

## GitHub Actions

There are basic CI, CD and Release pipelines, executed as [GitHub Actions workflow] when pushing changes or opening PR's.

??? example "Available workflows"

    === ".github/workflows/ci.yaml"

        ```yaml
        --8<-- ".github/workflows/ci.yaml"
        ```

    === ".github/workflows/cd.yaml"

        ```yaml
        --8<-- ".github/workflows/cd.yaml"
        ```

    === ".github/workflows/release.yaml"

        ```yaml
        --8<-- ".github/workflows/release.yaml"
        ```

??? info "Custom GitHub Actions Runners"

    Depending on the namespace the project lives in, you may not be able to use any public GitHub Actions runners.
    However, additional GitHub Action runners for your project can be added following the steps outlined in

    ```url
    https://github.boschdevcloud.com/bcai-internal/executable-ml-kgs/settings/actions/runners/new
    ```

    To deal with the Bosch proxy settings add a `.env` file into the runner directory:

    ```text title=".env"
    LANG=en_us.UTF-8
    http_proxy=http://rb-proxy-de.bosch.com:8080
    https_proxy=http://rb-proxy-de.bosch.com:8080
    ```

<!-- Glossary -->
*[CD]: Continuous Deployment / Delivery
*[CI]: Continuous Integration
*[PR]: Pull Request

<!-- URLs -->
[artifactory-access]: https://inside-docupedia.bosch.com/confluence/x/pTREXw#GitHubEnterprise-AccesstoArtifactoryRepositories
[black]: https://black.readthedocs.io/en/stable/
[coverage]: https://coverage.readthedocs.io/
[GitHub Actions workflow]: https://docs.github.com/en/actions/using-workflows
[isort]: https://pycqa.github.io/isort/
[mike]: https://github.com/jimporter/mike
[mkdocs-material]: https://squidfunk.github.io/mkdocs-material/
[mkdocs]: https://www.mkdocs.org/
[mypy]: http://mypy-lang.org/
[poe]: https://github.com/nat-n/poethepoet/
[poetry-pyproject]: https://python-poetry.org/docs/pyproject/
[poetry]: https://python-poetry.org/
[pre-commit]: https://pre-commit.com/
[pylint]: https://www.pylint.org/
[pytest]: https://docs.pytest.org/en/6.2.x/
[semantic versioning]: https://semver.org/
[settings-secrets]: https://github.boschdevcloud.com/bcai-internal/executable-ml-kgs/settings/secrets/actions
