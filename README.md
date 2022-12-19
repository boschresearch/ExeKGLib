# ExeKGLib

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Poetry](https://img.shields.io/badge/poetry-v1.2.2-blue)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)
[![License](https://img.shields.io/badge/license-AGPL%203.0-blue)](https://www.gnu.org/licenses/agpl-3.0.en.html)

Library for conveniently constructing and executing Machine Learning (ML) pipelines represented by Knowledge Graphs (KGs).

## External resources
### Top-level KG schemas
- Data Science KG schema: https://w3id.org/def/exekg-ds

### Bottom-level KG schemas
- Visualization KG schema: https://w3id.org/def/exekg-visu
- Statistics KG schema: https://w3id.org/def/exekg-stats
- Machine Learning KG schema: https://w3id.org/def/exekg-ml

Repo for the above KG schemas: https://github.com/nsai-uio/ExeKGOntology

## Overview
The functionality of this Python library can be divided in the below two parts:
1. **Executable KG construction**: An executable KG representing an ML pipeline is constructed as per user's input (programmatically or via CLI) based on the KG schemas. The construction consists of sequential creations of task-method pairs and their properties. After each KG component is built, it is validated using the KG schemas and added to an RDFLib `Graph` object. The KG is finally saved in Turtle format.
2. **ML pipeline execution**: The executable KG is parsed using RDFLib and queried using SPARQL to retrieve its ML pipeline. The pipeline's ordered tasks are sequentially mapped to Python objects that include an implemented `run_method()` Python method which is then invoked. This is as an abstract method of the _Task_ class that is implemented by its bottom-level children classes.

The different implementations of `run_method()` correspond to each of the _Method_'s bottom level sub-classes that are defined in the Visualization, Statistics, and ML KG schemas. The method categories are described below.
1. **Visualization**: This is a set of methods for visualization, including two types: (1) The plot canvas methods that define the plot size and layout. (2) The various kinds of plot methods (line plot, scatter plot, bar plot, etc.). These methods use matplotlib to visualize data.
2. **Statistics and Feature Engineering**: This includes methods for statistical analysis and feature engineering like IQR calculation, mean and std-deviation calculation, etc., which can then form complex methods like outlier detection method and normalization method.
3. **Machine Learning**: This is a group of methods that support ML algorithms like Linear Regression, MLP, and k-NN and helper functions that perform e.g. data splitting and ML model performance calculation.
