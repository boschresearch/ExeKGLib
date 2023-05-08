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

**ExeKGLib** is part of the following paper submitted to ESWC 2023:<br>
_Klironomos A., Zhou B., Tan Z., Zheng Z., Gad-Elrab M., Paulheim H., Kharlamov E.: **ExeKGLib: A Python Library for Machine Learning Analytics based on Knowledge Graphs**_

[//]: # (--8<-- [end:overview])

Detailed information (installation, documentation etc.) about **ExeKGLib** can be found in [its website](https://boschresearch.github.io/ExeKGLib/) and basic information is shown below.

## Installation

[//]: # (--8<-- [start:installation])
To install, run `pip install exe-kg-lib`.

[//]: # (--8<-- [end:installation])

For detailed installation instructions, refer to the [installation page](https://boschresearch.github.io/ExeKGLib/installation/) of **ExeKGLib**'s website.

## Ready-to-use ML-related tasks and methods

<details>
  <summary>Click to expand</summary>

<!-- --8<-- [start:supportedmethods] -->
| KG schema (abbreviation) | Task                      | Method                       | Properties                                                                                    | Input (data structure)                                                                                                                                           | Output (data structure)                                                                                                                                                                    | Implemented by Python class                          |
| ------------------------ | ------------------------- | ---------------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------- |
| Machine Learning (ml)    | Train                     | KNNTrain                     | \-                                                                                            | DataInTrainX (Matrix or Vector)<br>DataInTrainY (Matrix or Vector)                                                                                               | DataOutPredictedValueTrain (Matrix or Vector)<br>DataOutTrainModel (SingleValue)                                                                                                           | TrainKNNTrain                                        |
| Machine Learning (ml)    | Train                     | MLPTrain                     | \-                                                                                            | DataInTrainX (Matrix or Vector)<br>DataInTrainY (Matrix or Vector)                                                                                               | DataOutPredictedValueTrain (Matrix or Vector)<br>DataOutTrainModel (SingleValue)                                                                                                           | TrainMLPTrain                                        |
| Machine Learning (ml)    | Train                     | LRTrain                      | \-                                                                                            | DataInTrainX (Matrix or Vector)<br>DataInTrainY (Matrix or Vector)                                                                                               | DataOutPredictedValueTrain (Matrix or Vector)<br>DataOutTrainModel (SingleValue)                                                                                                           | TrainLRTrain                                         |
| Machine Learning (ml)    | Test                      | KNNTest                      | \-                                                                                            | DataInTestModel (SingleValue)<br>DataInTestX (Matrix or Vector)                                                                                                  | DataOutPredictedValueTest (Matrix or Vector)                                                                                                                                               | TestKNNTest                                          |
| Machine Learning (ml)    | Test                      | MLPTest                      | \-                                                                                            | DataInTestModel (SingleValue)<br>DataInTestX (Matrix or Vector)                                                                                                  | DataOutPredictedValueTest (Matrix or Vector)                                                                                                                                               | TestMLPTest                                          |
| Machine Learning (ml)    | Test                      | LRTest                       | \-                                                                                            | DataInTestModel (SingleValue)<br>DataInTestX (Matrix or Vector)                                                                                                  | DataOutPredictedValueTest (Matrix or Vector)                                                                                                                                               | TestLRTest                                           |
| Machine Learning (ml)    | PerformanceCalculation    | PerformanceCalculationMethod | \-                                                                                            | DataInTrainRealY (Matrix or Vector)<br>DataInTrainPredictedY (Matrix or Vector)<br>DataInTestPredictedY (Matrix or Vector)<br>DataInTestRealY (Matrix or Vector) | DataOutMLTestErr (Vector)<br>DataOutMLTrainErr (Vector)                                                                                                                                    | PerformanceCalculationPerformanceCalculationMethod   |
| Machine Learning (ml)    | Concatenation             | ConcatenationMethod          | \-                                                                                            | DataInConcatenation (list of Vector)                                                                                                                             | DataOutConcatenatedData (Matrix)                                                                                                                                                           | ConcatenationConcatenationMethod                     |
| Machine Learning (ml)    | DataSplitting             | DataSplittingMethod          | \-                                                                                            | DataInDataSplittingX (Matrix or Vector)<br>DataInDataSplittingY (Matrix or Vector)                                                                               | DataOutSplittedTestDataX (Matrix or Vector)<br>DataOutSplittedTrainDataY (Matrix or Vector)<br>DataOutSplittedTrainDataX (Matrix or Vector)<br>DataOutSplittedTestDataY (Matrix or Vector) | DataSplittingDataSplittingMethod                     |
| Visualization (visu)     | CanvasTask                | CanvasMethod                 | hasCanvasName (string)<br>hasLayout (string)                                                  | \-                                                                                                                                                               | \-                                                                                                                                                                                         | CanvasTaskCanvasMethod                               |
| Visualization (visu)     | PlotTask                  | LineplotMethod               | hasLineStyle (string)<br>hasLineWidth (int)<br>hasLegendName (string)                         | DataInVector (Vector)                                                                                                                                            | \-                                                                                                                                                                                         | PlotTaskLineplotMethod                               |
| Visualization (visu)     | PlotTask                  | ScatterplotMethod            | hasLineStyle (string)<br>hasLineWidth (int)<br>hasScatterSize (int)<br>hasLegendName (string) | DataInVector (Vector)                                                                                                                                            | \-                                                                                                                                                                                         | PlotTaskScatterplotMethod                            |
| Statistics (stats)       | TrendCalculationTask      | TrendCalculationMethod       | \-                                                                                            | DataInTrendCalculation (Vector)                                                                                                                                  | DataOutTrendCalculation (Vector)                                                                                                                                                           | TrendCalculationTaskTrendCalculationMethod           |
| Statistics (stats)       | NormalizationTask         | NormalizationMethod          | \-                                                                                            | DataInNormalization (Vector)                                                                                                                                     | DataOutNormalization (Vector)                                                                                                                                                              | NormalizationTaskNormalizationMethod                 |
| Statistics (stats)       | ScatteringCalculationTask | ScatteringCalculationMethod  | \-                                                                                            | DataInScatteringCalculation (Vector)                                                                                                                             | DataOutScatteringCalculation (Vector)                                                                                                                                                      | ScatteringCalculationTaskScatteringCalculationMethod |

[//]: # (--8<-- [end:supportedmethods])

</details>

## Usage

[//]: # (--8<-- [start:usage])
### Creating an ML pipeline

- **Via code**: See the [provided examples](https://github.com/boschresearch/ExeKGLib/tree/main/examples). To fetch them to your working directory for easy access, run `typer exe_kg_lib.cli.main run get-examples`.
- **Step-by-step via CLI**: Run `typer exe_kg_lib.cli.main run create-pipeline`.

### Executing an ML pipeline
- **Via code**: See [example code](https://github.com/boschresearch/ExeKGLib/blob/21e4df0e7de89c27748c8b61759652b7edf7d9b8/exe_kg_lib/cli/main.py#L28-L29).
- **Via CLI**: Run `typer exe_kg_lib.cli.main run run-pipeline <pipeline_path>`.

[//]: # (--8<-- [end:usage])

## Adding a new ML-related task and method

[//]: # (--8<-- [start:extending])
To perform this type of **ExeKGLib** extension, there are 3 required steps:

1. Selection of a relevant bottom-level KG schema (Statistics, ML, or Visualization) according to the type of the new task and method.
2. Addition of new semantic components (entities, properties, etc) to the selected KG schema.
3. Addition of a Python class to the corresponding module of `exe_kg_lib.classes.tasks` package.

For steps 2 and 3, refer to the [relevant page](https://boschresearch.github.io/ExeKGLib/adding-new-task-and-method/) of **ExeKGLib**'s website.

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
