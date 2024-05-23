# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from pathlib import Path

from exe_kg_lib import ExeKGConstructor

HERE = Path(__file__).resolve().parent

if __name__ == "__main__":
    exe_kg = ExeKGConstructor()
    exe_kg.create_exe_kg_from_json(HERE / "MLPipeline.json")
    exe_kg.save_created_kg(HERE / "pipelines")
