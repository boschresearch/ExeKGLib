<!---
  Copyright (c) 2022 Robert Bosch GmbH and its subsidiaries. All rights reserved.
-->

# Executable Machine Learning Knowledge Graphs

[![License: All rights reserved][license-badge]][license-url]
[![CI][ci-badge]][ci]
[![Docs][docs-badge]][docs]
[![pre-commit][pre-commit-badge]][pre-commit]
[![Code style: black][black-badge]][black]

Library for executable ML pipelines KGs.

## Overview
This library consists of the below 2 parts:
1. **KG construction**: A KG is created as per user's input (via CLI) based on the ontologies published on this repo: https://github.com/baifanzhou/ExeKGOntology.
   <br>The KG can have one of the following functionalities:
   1. Visual: Plotting values of the input data.
   3. Statistics: Performing an operation on the input data and outputting the result.
   4. Machine Learning (ML): Applying an ML algorithm to the input data and outputting predictions.
3. **KG execution**: The constructed KG is translated to Python code and executed to produce results depending on the KG's functionality.

## Installation

Use `poetry install` to install the project's dependencies.

## Usage

1. Run `python kg_construction.py` and follow the CLI's instructions to create the KG.
2. Run `python kg_execution.py` to execute the created KG.

<!-- URLs -->
[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black]: https://github.com/psf/black
[ci-badge]: https://github.boschdevcloud.com/bcai-internal/executable-ml-kgs/actions/workflows/ci.yaml/badge.svg
[ci]: https://github.boschdevcloud.com/bcai-internal/executable-ml-kgs/actions/workflows/ci.yaml
[docs-badge]: https://img.shields.io/badge/docs-gh--pages-inactive
[docs]: https://github.boschdevcloud.com/bcai-internal/executable-ml-kgs/tree/gh-pages
[license-badge]: https://img.shields.io/badge/License-All%20rights%20reserved-informational
[license-url]: https://pages.github.boschdevcloud.com/bcai-internal/executable-ml-kgs/latest/license
[pre-commit-badge]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
[pre-commit]: https://github.com/pre-commit/pre-commit
