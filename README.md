# ExeKGLib

![PyPI](https://img.shields.io/pypi/v/exe-kg-lib)
![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Poetry](https://img.shields.io/badge/poetry-v1.2.2-blue)
[![Code style: black][black-badge]][black]
[![License](https://img.shields.io/badge/license-AGPL%203.0-blue)](https://www.gnu.org/licenses/agpl-3.0.en.html)

Python library for conveniently constructing and executing Machine Learning (ML) pipelines represented by Knowledge Graphs (KGs).

Detailed information (installation, documentation etc.) about the library can be found in [its website](https://boschresearch.github.io/ExeKGLib/) and basic information is shown below.

## Overview

[//]: # (--8<-- [start:overview])
The functionality of this Python library can be divided in the below two parts:

1. **Executable KG construction**: An executable KG representing an ML pipeline is constructed as per user's input (programmatically or via CLI) based on the KG schemas. The construction is done by sequentially creating pairs of instances of [ds:AtomicTask](https://nsai-uio.github.io/ExeKGOntology/OnToology/ds_exeKGOntology.ttl/documentation/index-en.html#AtomicTask) and [ds:AtomicMethod](https://nsai-uio.github.io/ExeKGOntology/OnToology/ds_exeKGOntology.ttl/documentation/index-en.html#AtomicMethod) sub-classes, and their properties. The definition of these sub-classes can be found in the [bottom-level KG schemas](#bottom-level-kg-schemas). After each KG component is built, it is validated using the KG schemas and added to an RDFLib `Graph` object. The KG is finally saved in Turtle format.
2. **ML pipeline execution**: The executable KG is parsed using RDFLib and queried using SPARQL to retrieve its ML pipeline. The pipeline's ordered tasks are sequentially mapped to Python objects that include an implemented `run_method()` Python method which is then invoked. This is as an abstract method of the _Task_ class that is implemented by its bottom-level children classes.

The different implementations of `run_method()` correspond to the [ds:AtomicMethod](https://nsai-uio.github.io/ExeKGOntology/OnToology/ds_exeKGOntology.ttl/documentation/index-en.html#AtomicMethod) bottom-level sub-classes that are defined in the Visualization, Statistics, and ML KG schemas. The method categories are described below.

1. **Visualization**: This is a set of methods for visualization, including two types: (1) The plot canvas methods that define the plot size and layout. (2) The various kinds of plot methods (line plot, scatter plot, bar plot, etc.). These methods use matplotlib to visualize data.
2. **Statistics and Feature Engineering**: This includes methods for statistical analysis and feature engineering like IQR calculation, mean and std-deviation calculation, etc., which can then form complex methods like outlier detection method and normalization method.
3. **Machine Learning**: This is a group of methods that support ML algorithms like Linear Regression, MLP, and k-NN and helper functions that perform e.g. data splitting and ML model performance calculation.

This library is part of the following paper submitted to ESWC 2023:<br>
_Klironomos A., Zhou B., Tan Z., Zheng Z., Gad-Elrab M., Paulheim H., Kharlamov E.: **ExeKGLib: A Python Library for Machine Learning Analytics based on Knowledge Graphs**_

[//]: # (--8<-- [end:overview])

## Getting started

[//]: # (--8<-- [start:gettingstarted])
The library is available as a [PyPi package](https://pypi.org/project/exe-kg-lib/).

To download, run `pip install exe-kg-lib`.

[//]: # (--8<-- [end:gettingstarted])

## Ready-to-use ML-related tasks and methods

<details>
  <summary>Click to expand</summary>

[//]: # (--8<-- [start:supportedmethods])
| KG schema        | Task                      | Method                       | Properties                                                                                    | Input (data structure)                                                                                                                                           | Output (data structure)                                                                                                                                                                    | Implemented by Python class                          |
| ---------------- | ------------------------- | ---------------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------- |
| Machine Learning | Train                     | KNNTrain                     | \-                                                                                            | DataInTrainX (Matrix or Vector)<br>DataInTrainY (Matrix or Vector)                                                                                               | DataOutPredictedValueTrain (Matrix or Vector)<br>DataOutTrainModel (SingleValue)                                                                                                           | TrainKNNTrain                                        |
| Machine Learning | Train                     | MLPTrain                     | \-                                                                                            | DataInTrainX (Matrix or Vector)<br>DataInTrainY (Matrix or Vector)                                                                                               | DataOutPredictedValueTrain (Matrix or Vector)<br>DataOutTrainModel (SingleValue)                                                                                                           | TrainMLPTrain                                        |
| Machine Learning | Train                     | LRTrain                      | \-                                                                                            | DataInTrainX (Matrix or Vector)<br>DataInTrainY (Matrix or Vector)                                                                                               | DataOutPredictedValueTrain (Matrix or Vector)<br>DataOutTrainModel (SingleValue)                                                                                                           | TrainLRTrain                                         |
| Machine Learning | Test                      | KNNTest                      | \-                                                                                            | DataInTestModel (SingleValue)<br>DataInTestX (Matrix or Vector)                                                                                                  | DataOutPredictedValueTest (Matrix or Vector)                                                                                                                                               | TestKNNTest                                          |
| Machine Learning | Test                      | MLPTest                      | \-                                                                                            | DataInTestModel (SingleValue)<br>DataInTestX (Matrix or Vector)                                                                                                  | DataOutPredictedValueTest (Matrix or Vector)                                                                                                                                               | TestMLPTest                                          |
| Machine Learning | Test                      | LRTest                       | \-                                                                                            | DataInTestModel (SingleValue)<br>DataInTestX (Matrix or Vector)                                                                                                  | DataOutPredictedValueTest (Matrix or Vector)                                                                                                                                               | TestLRTest                                           |
| Machine Learning | PerformanceCalculation    | PerformanceCalculationMethod | \-                                                                                            | DataInTrainRealY (Matrix or Vector)<br>DataInTrainPredictedY (Matrix or Vector)<br>DataInTestPredictedY (Matrix or Vector)<br>DataInTestRealY (Matrix or Vector) | DataOutMLTestErr (Vector)<br>DataOutMLTrainErr (Vector)                                                                                                                                    | PerformanceCalculationPerformanceCalculationMethod   |
| Machine Learning | Concatenation             | ConcatenationMethod          | \-                                                                                            | DataInConcatenation (list of Vector)                                                                                                                             | DataOutConcatenatedData (Matrix)                                                                                                                                                           | ConcatenationConcatenationMethod                     |
| Machine Learning | DataSplitting             | DataSplittingMethod          | \-                                                                                            | DataInDataSplittingX (Matrix or Vector)<br>DataInDataSplittingY (Matrix or Vector)                                                                               | DataOutSplittedTestDataX (Matrix or Vector)<br>DataOutSplittedTrainDataY (Matrix or Vector)<br>DataOutSplittedTrainDataX (Matrix or Vector)<br>DataOutSplittedTestDataY (Matrix or Vector) | DataSplittingDataSplittingMethod                     |
| Visualization    | CanvasTask                | CanvasMethod                 | hasCanvasName (string)<br>hasLayout (string)                                                  | \-                                                                                                                                                               | \-                                                                                                                                                                                         | CanvasTaskCanvasMethod                               |
| Visualization    | PlotTask                  | LineplotMethod               | hasLineStyle (string)<br>hasLineWidth (int)<br>hasLegendName (string)                         | DataInVector (Vector)                                                                                                                                            | \-                                                                                                                                                                                         | PlotTaskLineplotMethod                               |
| Visualization    | PlotTask                  | ScatterplotMethod            | hasLineStyle (string)<br>hasLineWidth (int)<br>hasScatterSize (int)<br>hasLegendName (string) | DataInVector (Vector)                                                                                                                                            | \-                                                                                                                                                                                         | PlotTaskScatterplotMethod                            |
| Statistics       | TrendCalculationTask      | TrendCalculationMethod       | \-                                                                                            | DataInTrendCalculation (Vector)                                                                                                                                  | DataOutTrendCalculation (Vector)                                                                                                                                                           | TrendCalculationTaskTrendCalculationMethod           |
| Statistics       | NormalizationTask         | NormalizationMethod          | \-                                                                                            | DataInNormalization (Vector)                                                                                                                                     | DataOutNormalization (Vector)                                                                                                                                                              | NormalizationTaskNormalizationMethod                 |
| Statistics       | ScatteringCalculationTask | ScatteringCalculationMethod  | \-                                                                                            | DataInScatteringCalculation (Vector)                                                                                                                             | DataOutScatteringCalculation (Vector)                                                                                                                                                      | ScatteringCalculationTaskScatteringCalculationMethod |

[//]: # (--8<-- [end:supportedmethods])

</details>

## Usage

[//]: # (--8<-- [start:usage])
### Fetching examples to working directory
Run `typer exe_kg_lib.cli.main run get-examples`.

### Creating an ML pipeline
#### Via CLI
1. Run `typer exe_kg_lib.cli.main run create-pipeline`.
2. Follow the input prompts.

#### Via code
See the [provided examples](https://github.com/boschresearch/ExeKGLib/tree/main/examples).

### Executing an ML pipeline
Run `typer exe_kg_lib.cli.main run run-pipeline <pipeline_path>`.

[//]: # (--8<-- [end:usage])

## Installation
See the [installation page](https://boschresearch.github.io/ExeKGLib/installation/) of the library's website.

## Adding a new ML-related task and method

[//]: # (--8<-- [start:extending])
To perform this type of library extension, there are 3 required steps:

1. Selection of a relevant bottom-level KG schema (Statistics, ML, or Visualization) according to the type of the new task and method.
2. Addition of new semantic components (entities, properties, etc) to the selected KG schema.
3. Addition of a Python class to the corresponding module of `exe_kg_lib.classes.tasks` package.

For steps 2 and 3, refer to the [relevant page](https://boschresearch.github.io/ExeKGLib/adding-new-task-and-method/) of the library's website.

[//]: # (--8<-- [end:extending])

## Documentation
See the _Code Reference_ and _Development_ sections of the [library's website](https://boschresearch.github.io/ExeKGLib/).

## External resources

[//]: # (--8<-- [start:externalresources])
### Top-level KG schemas
- [Data Science KG schema](https://w3id.org/def/exekg-ds)

### Bottom-level KG schemas
- [Visualization KG schema](https://w3id.org/def/exekg-visu)
- [Statistics KG schema](https://w3id.org/def/exekg-stats)
- [Machine Learning KG schema](https://w3id.org/def/exekg-ml)

The above KG schemas are included in the [ExeKGOntology repository](https://github.com/nsai-uio/ExeKGOntology).

### Dataset used in code examples
This dataset (located in `exe_kg_lib/examples/data/dummy_data.csv`) was generated using the `sklearn.datasets.make_classification()` function of the [scikit-learn Python library](https://scikit-learn.org/).

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
