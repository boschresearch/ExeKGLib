# ExeKGLib: A Python Library for Knowledge Graphs-Empowered Machine Learning Analytics 🚀

![PyPI](https://img.shields.io/pypi/v/exe-kg-lib)
![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Poetry](https://img.shields.io/badge/poetry-v1.2.2-blue)
[![Code style: black][black-badge]][black]
[![License](https://img.shields.io/badge/license-AGPL%203.0-blue)](https://www.gnu.org/licenses/agpl-3.0.en.html)

[//]: # (--8<-- [start:overview])
ExeKGLib is a Python library that simplifies the construction and execution of Machine Learning (ML) pipelines represented by Executable Knowledge Graphs (ExeKGs). It features a coding interface and a CLI, and allows the user to:

## 🌟 Features

1. **🔨 Construct** data analytics pipelines that take tabular files (e.g. CSV) as input and process the data using a variety of [available tasks and methods](https://boschresearch.github.io/ExeKGLib/supported-tasks-and-methods/).
2. **💾 Save** the constructed pipelines as ExeKGs in RDF Turtle format.
3. **▶️ Execute** the generated ExeKGs.

## 🌟 Key Benefits of ExeKGLib

1. 🚀 **No-code ML Pipeline Creation**: With ExeKGLib, the user can specify the pipeline's structure and the operations to be performed using a simple JSON file (see [Creating an ML pipeline](https://boschresearch.github.io/ExeKGLib/usage/#creating-an-ml-pipeline)), which is then automatically converted to an ExeKG. This ExeKG can be executed to perform the specified operations on the input data (see [Executing an ML pipeline](https://boschresearch.github.io/ExeKGLib/usage/#executing-an-ml-pipeline)).
2. 📦 **Batch Pipeline Creation**: ExeKGLib allows users to create pipelines in a batch fashion through its simple coding interface (see [Creating an ML pipeline](https://boschresearch.github.io/ExeKGLib/usage/#creating-an-ml-pipeline)). This enables automatic creation of multiple pipelines as ExeKGs, which can then be queried and analyzed.
3. 🔗 **Linked Open Data Integration**: ExeKGLib is a tool that leverages linked open data (LOD) in several significant ways:
    - 📚 **Pipeline Creation Guidance**: It helps guide the user through the pipeline creation process. This is achieved by using a predefined hierarchy of tasks, along with their compatible inputs, outputs, methods, and method parameters (see [available tasks and methods](https://boschresearch.github.io/ExeKGLib/supported-tasks-and-methods/)).
    - 🧠 **Enhancing User Understanding**: It enhances the user's understanding of Data Science and the pipeline's functionality. This is achieved by linking the generated pipelines to Knowledge Graph (KG) schemata that encapsulate various Data Science concepts (see [KG schemata](https://boschresearch.github.io/ExeKGLib/external-sources/#kg-schemata)).
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
We provide [example Python and JSON files](https://github.com/boschresearch/ExeKGLib/tree/main/examples) that can be used to create the following pipelines:

1. **🧠 ML pipeline**:
    1. **MLPipelineSimple**: Loads a CSV dataset, concatenates selected features, splits the data into training and testing sets, trains a Support Vector Classifier (SVC) model, tests the model, calculates performance metrics (accuracy, F1 score, precision, and recall), and visualizes the results in bar plots.
    2. **MLPipelineCrossValidation**: An extended version of **MLPipelineSimple** that adds a data splitting step for Stratified K-Fold Cross-Validation. Then, it trains and tests the model using the cross-validation technique and visualizes the validation and test F1 scores in bar plots.
    3. **MLPipelineModelSelection**: A modified version of **MLPipelineSimple** that replaces the training step with a model selection step. Rather than using a fixed model, this pipeline involves training and cross-validating a Support Vector Classifier (SVC) model with various hyperparameters to optimize performance.
2. **📊 Statistics pipeline**:
    - **StatsPipeline**: Loads a specific feature from a CSV dataset, calculates its mean and standard deviation, and visualizes the feature's values using a line plot and the calculated statistics using a bar plot.
3. **📈 Visualization pipeline**:
    - **VisuPipeline**: The pipeline loads two numerical features from a CSV dataset and visualizes each feature's values using separate line plots.

> 💡 **Tip**: To fetch the examples into your working directory for easy access, run `typer exe_kg_lib.cli.main run get-examples`.

> 🗒️ **Note**: The naming convention for output names (used as inputs for subsequent tasks) in `.json` files can be found in `exe_kg_lib/utils/string_utils.py`. Look for `TASK_OUTPUT_NAME_REGEX`.

[//]: # (--8<-- [end:gettingstarted])

## 🧪 Supported ML-related tasks and methods

See [relevant website page](https://boschresearch.github.io/ExeKGLib/supported-tasks-and-methods).

## 🛠️ Usage

[//]: # (--8<-- [start:usage])
### 🚀 Creating an ML pipeline

#### 💻 Via code
See the Python files in the [provided examples](https://github.com/boschresearch/ExeKGLib/tree/main/examples).

#### 📄 Using JSON
Run `typer exe_kg_lib.cli.main run create-pipeline <json_path>` after replacing `<json_path>` to point to a pipeline's JSON file. See the [provided example JSONs](https://github.com/boschresearch/ExeKGLib/tree/main/examples)

> 🗒️ **Note**: Replace `input_data_path` with the path to a dataset and `output_plots_dir` with the directory path where the plots will be saved.

#### 🖥️ Step-by-step via CLI
Run `typer exe_kg_lib.cli.main run create-pipeline`.

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
