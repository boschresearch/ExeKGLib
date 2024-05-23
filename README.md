# ExeKGLib: A Python Library for Knowledge Graphs-Empowered Machine Learning Analytics 🚀

![PyPI](https://img.shields.io/pypi/v/exe-kg-lib)
![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Poetry](https://img.shields.io/badge/poetry-v1.2.2-blue)
[![Code style: black][black-badge]][black]
[![License](https://img.shields.io/badge/license-AGPL%203.0-blue)](https://www.gnu.org/licenses/agpl-3.0.en.html)

[//]: # (--8<-- [start:overview])
ExeKGLib is a Python library that simplifies the construction and execution of Machine Learning (ML) pipelines represented by Executable Knowledge Graphs (ExeKGs). It features a coding interface and a CLI, and allows the user to:

## 🌟 Features

1. **🔨 Construct** data analytics pipelines that take tabular files (e.g. CSV) as input and process the data using a variety of [available tasks and methods](https://boschresearch.github.io/ExeKGLib/supported-methods/).
2. **💾 Save** the constructed pipelines as ExeKGs in RDF Turtle format.
3. **▶️ Execute** the generated ExeKGs.

## 🌟 Key Benefits of ExeKGLib

1. 🚀 **No-code ML Pipeline Creation**: With ExeKGLib, the user can specify the pipeline's structure and the operations to be performed using a simple JSON file (see [Creating an ML pipeline](#🚀-creating-an-ml-pipeline)), which is then automatically converted to an ExeKG. This ExeKG can be executed to perform the specified operations on the input data (see [Executing an ML pipeline](#🚀-executing-an-ml-pipeline)).
2. 📦 **Batch Pipeline Creation**: ExeKGLib allows users to create pipelines in a batch fashion through its simple coding interface (see [Creating an ML pipeline](#🚀-creating-an-ml-pipeline)). This enables automatic creation of multiple pipelines as ExeKGs, which can then be queried and analyzed.
3. 🔗 **Linked Open Data Integration**: ExeKGLib is a tool that leverages linked open data (LOD) in several significant ways:
    - 📚 **Pipeline Creation Guidance**: It helps guide the user through the pipeline creation process. This is achieved by using a predefined hierarchy of tasks, along with their compatible inputs, outputs, methods, and method parameters (see [available tasks and methods]([task_hierarchy.md](https://boschresearch.github.io/ExeKGLib/supported-methods/))).
    - 🧠 **Enhancing User Understanding**: It enhances the user's understanding of Data Science and the pipeline's functionality. This is achieved by linking the generated pipelines to Knowledge Graph (KG) schemata that encapsulate various Data Science concepts (see [KG schemata](#📜-kg-schemata)).
    - ✅ **Validation of ExeKGs**: It validates the generated ExeKGs to ensure their executability.
    - 🔄 **Automatic Conversion and Execution**: It automatically converts the ExeKGs to Python code and executes them.

Under the hood, **ExeKGLib** uses well-known Python libraries for data processing and visualization and performing predictions such as [pandas](https://pandas.pydata.org/), [matplotlib](https://matplotlib.org/), and [scikit-learn](https://scikit-learn.org/).

**ExeKGLib** is described in the following paper published as part of ESWC 2023: <br>[Klironomos A., Zhou B., Tan Z., Zheng Z., Gad-Elrab M., Paulheim H., Kharlamov E. _**ExeKGLib: Knowledge Graphs-Empowered Machine Learning Analytics**_](https://link.springer.com/chapter/10.1007/978-3-031-43458-7_23)

[//]: # (--8<-- [end:overview])

Detailed information (installation, documentation etc.) about **ExeKGLib** can be found in [its website](https://boschresearch.github.io/ExeKGLib/) and basic information is shown below.

## 📦 Installation

[//]: # (--8<-- [start:installation])
To install, run `pip install exe-kg-lib`.

[//]: # (--8<-- [end:installation])

For detailed installation instructions, refer to the [installation page](https://boschresearch.github.io/ExeKGLib/installation/) of **ExeKGLib**'s website.

## 🚀 Getting started

[//]: # (--8<-- [start:gettingstarted])
We provide [example Python files and a JSON file](https://github.com/boschresearch/ExeKGLib/tree/main/examples) that can be used to create the following pipelines:

1. **🧠 ML pipeline**: Loads a CSV dataset, concatenates selected features, splits the data into training and testing sets, trains a Support Vector Classifier model, tests the model, calculates performance metrics (accuracy, F1 score, precision, and recall), and visualizes the results in bar plots.
2. **📊 Statistics pipeline**: Loads a specific feature from a CSV dataset, calculates its mean and standard deviation, and visualizes the feature's values using a line plot and the calculated statistics using a bar plot.
3. **📈 Visualization pipeline**: The pipeline loads two numerical features from a CSV dataset and visualizes each feature's values using separate line plots.

[//]: # (--8<-- [end:gettingstarted])

## 🧪 Ready-to-use ML-related tasks and methods

See [Task hierarchy](task_hierarchy.md).

## 🛠️ Usage

[//]: # (--8<-- [start:usage])
### 🚀 Creating an ML pipeline

#### 💻 Via code
See `ml_pipeline_creation.py`,  `stats_pipeline_creation.py`,  `visu_pipeline_creation.py` in the [provided examples](https://github.com/boschresearch/ExeKGLib/tree/main/examples).

#### 📄 Using JSON
See `MLPipeline.json` and `ml_pipeline_creation_from_json.py` in the [provided examples](https://github.com/boschresearch/ExeKGLib/tree/main/examples).

#### 🖥️ Step-by-step via CLI
Run `typer exe_kg_lib.cli.main run create-pipeline`.

> 🗒️ **Note**: To fetch the [provided examples](https://github.com/boschresearch/ExeKGLib/tree/main/examples) to your working directory for easy access, run `typer exe_kg_lib.cli.main run get-examples`.

### 🚀 Executing an ML pipeline

#### 💻 Via code
See [example code](https://github.com/boschresearch/ExeKGLib/blob/21e4df0e7de89c27748c8b61759652b7edf7d9b8/exe_kg_lib/cli/main.py#L28-L29).

#### 🖥️ Via CLI
Run `typer exe_kg_lib.cli.main run run-pipeline <pipeline_path>`. The `pipeline_path` can either be a `.ttl` or `.json` file.

[//]: # (--8<-- [end:usage])

## 📝 Adding a new ML-related task and method

[//]: # (--8<-- [start:extending])
For detailed guidelines, refer to the [relevant page](https://boschresearch.github.io/ExeKGLib/adding-new-task-and-method/) of **ExeKGLib**'s website.

In summary, these are the steps:

1. Selecting a bottom-level KG schema (Statistics, ML, or Visualization) based on the type of the new task and method.
2. Adding new semantic components (entities, properties, etc.) to the selected KG schema and the corresponding SHACL shapes graph.
3. Modifying the Python code in the corresponding file of `exe_kg_lib.classes.tasks` package.

[//]: # (--8<-- [end:extending])

## 📚 Documentation
See the _Code Reference_ and _Development_ sections of the [**ExeKGLib**'s website](https://boschresearch.github.io/ExeKGLib/).

## 🌐 External resources

[//]: # (--8<-- [start:externalresources])
### 📜 KG schemata

- **Top-level**: [Data Science](https://w3id.org/def/exekg-ds)
- **Bottom-level**: [Visualization](https://w3id.org/def/exekg-visu) | [Statistics](https://w3id.org/def/exekg-stats) | [Machine Learning](https://w3id.org/def/exekg-ml)

The above KG schemata are included in the [ExeKGOntology repository](https://github.com/nsai-uio/ExeKGOntology).

### 📊 Dataset used in code examples

[The dataset](https://github.com/boschresearch/ExeKGLib/tree/main/examples/data/dummy_data.csv) was generated using the `sklearn.datasets.make_classification()` function of the [scikit-learn Python library](https://scikit-learn.org/).

[//]: # (--8<-- [end:externalresources])

## 📜 License

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
