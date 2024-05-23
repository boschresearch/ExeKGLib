# ExeKGLib

![PyPI](https://img.shields.io/pypi/v/exe-kg-lib)
![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Poetry](https://img.shields.io/badge/poetry-v1.2.2-blue)
[![Code style: black][black-badge]][black]
[![License](https://img.shields.io/badge/license-AGPL%203.0-blue)](https://www.gnu.org/licenses/agpl-3.0.en.html)

[//]: # (--8<-- [start:overview])
Python library for conveniently constructing and executing Machine Learning (ML) pipelines represented by Knowledge Graphs (KGs). It features a coding interface and a CLI, and allows the user to:

1. **Construct** an ML pipeline that gets a CSV as input and processes the data using any of the [available tasks and methods](https://github.com/boschresearch/ExeKGLib/tree/main/README.md#Ready-to-use-ML-related-tasks-and-methods).
2. **Save** the constructed pipeline as a KG in Turtle format.
3. **Execute** the generated KG.

The coding interface is demonstrated with [three sample Python files](https://github.com/boschresearch/ExeKGLib/tree/main/examples). The pipelines represented by the generated sample KGs are briefly explained below:

1. **ML pipeline**: Loads features and labels from an input CSV dataset, splits the data, trains and tests a k-NN model, and visualizes the prediction errors.
2. **Statistics pipeline**: Loads a feature from an input CSV dataset, normalizes it, and plots its values (before and after normalization) using a scatter plot.
3. **Visualization pipeline**: Loads a feature from an input CSV dataset and plots its values using a line plot.

Under the hood, **ExeKGLib** uses well-known Python libraries for data processing and visualization and performing predictions such as [pandas](https://pandas.pydata.org/), [matplotlib](https://matplotlib.org/), and [scikit-learn](https://scikit-learn.org/).

**ExeKGLib** is described in the following paper published as part of ESWC 2023: <br>[Klironomos A., Zhou B., Tan Z., Zheng Z., Gad-Elrab M., Paulheim H., Kharlamov E. _**ExeKGLib: Knowledge Graphs-Empowered Machine Learning Analytics**_](https://link.springer.com/chapter/10.1007/978-3-031-43458-7_23)

[//]: # (--8<-- [end:overview])

Detailed information (installation, documentation etc.) about **ExeKGLib** can be found in [its website](https://boschresearch.github.io/ExeKGLib/) and basic information is shown below.

## Installation

[//]: # (--8<-- [start:installation])
To install, run `pip install exe-kg-lib`.

[//]: # (--8<-- [end:installation])

For detailed installation instructions, refer to the [installation page](https://boschresearch.github.io/ExeKGLib/installation/) of **ExeKGLib**'s website.

## Ready-to-use ML-related tasks and methods

See [Task hierarchy](task_hierarchy.md).

</details>

## Usage

[//]: # (--8<-- [start:usage])
### Creating an ML pipeline

- **Via code**: See `ml_pipeline_creation.py`,  `stats_pipeline_creation.py`,  `visu_pipeline_creation.py` in the [provided examples](https://github.com/boschresearch/ExeKGLib/tree/main/examples).
- **Using JSON**: See `MLPipeline.json` and `ml_pipeline_creation_from_json.py` in the [provided examples](https://github.com/boschresearch/ExeKGLib/tree/main/examples).
- **Step-by-step via CLI**: Run `typer exe_kg_lib.cli.main run create-pipeline`.

**🗒️ Note**: To fetch the [provided examples](https://github.com/boschresearch/ExeKGLib/tree/main/examples) to your working directory for easy access, run `typer exe_kg_lib.cli.main run get-examples`.

### Executing an ML pipeline
- **Via code**: See [example code](https://github.com/boschresearch/ExeKGLib/blob/21e4df0e7de89c27748c8b61759652b7edf7d9b8/exe_kg_lib/cli/main.py#L28-L29).
- **Via CLI**: Run `typer exe_kg_lib.cli.main run run-pipeline <pipeline_path>`.

[//]: # (--8<-- [end:usage])

## Adding a new ML-related task and method

[//]: # (--8<-- [start:extending])
For detailed guidelines, refer to the [relevant page](https://boschresearch.github.io/ExeKGLib/adding-new-task-and-method/) of **ExeKGLib**'s website.

In summary, these are the steps:

1. Selecting a bottom-level KG schema (Statistics, ML, or Visualization) based on the type of the new task and method.
2. Adding new semantic components (entities, properties, etc.) to the selected KG schema and the corresponding SHACL shapes graph.
3. Modifying the Python code in the corresponding file of `exe_kg_lib.classes.tasks` package.

[//]: # (--8<-- [end:extending])

## Documentation
See the _Code Reference_ and _Development_ sections of the [**ExeKGLib**'s website](https://boschresearch.github.io/ExeKGLib/).

## External resources

[//]: # (--8<-- [start:externalresources])
### KG schemata

- **Top-level**: [Data Science](https://w3id.org/def/exekg-ds)
- **Bottom-level**: [Visualization](https://w3id.org/def/exekg-visu) | [Statistics](https://w3id.org/def/exekg-stats) | [Machine Learning](https://w3id.org/def/exekg-ml)

The above KG schemata are included in the [ExeKGOntology repository](https://github.com/nsai-uio/ExeKGOntology).

### Dataset used in code examples
[The dataset](https://github.com/boschresearch/ExeKGLib/tree/main/examples/data/dummy_data.csv) was generated using the `sklearn.datasets.make_classification()` function of the [scikit-learn Python library](https://scikit-learn.org/).

[//]: # (--8<-- [end:externalresources])

## License

ExeKGLib is open-sourced under the AGPL-3.0 license. See the
[LICENSE](LICENSE.md) file for details.

<!-- URLs -->
[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black]: https://github.com/psf/black
[ci-badge]: https://github.com/boschresearch/ExeKGLib/actions/workflows/ci.yaml/badge.svg
[ci]: https://github.com/boschresearch/ExeKGLib/actions/workflows/ci.yaml
[docs-badge]: https://img.shields.io/badge/docs-gh--pages-inactive
[docs]: https://github.com/boschresearch/ExeKGLib/tree/gh-pages
[license-badge]: https://img.shields.io/badge/License-All%20rights%20reserved-informational
[license-url]: https://pages.github.boschdevcloud.com/bcai-internal//latest/license
[pre-commit-badge]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
[pre-commit]: https://github.com/pre-commit/pre-commit
