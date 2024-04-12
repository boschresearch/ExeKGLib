# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from pathlib import Path

from exe_kg_lib import ExeKGConstructor

HERE = Path(__file__).resolve().parent

if __name__ == "__main__":
    exe_kg = ExeKGConstructor()
    feature_1 = exe_kg.create_data_entity(
        name="feature_1",
        source_value="feature_1",
        data_semantics_name="TimeSeries",
        data_structure_name="Vector",
    )

    pipeline_name = "StatsPipeline"
    pipeline = exe_kg.create_pipeline_task(
        pipeline_name,
        input_data_path=HERE / "data" / "dummy_data.csv",
        plots_output_dir=HERE / "plots" / pipeline_name,
    )

    mean_task = exe_kg.add_task(
        kg_schema_short="stats",
        task="CentralTendencyMeasure",
        input_data_entity_dict={"DataInStatisticCalculation": [feature_1]},
        method="Mean",
        method_params_dict={},
    )
    mean = mean_task.output_dict["DataOutStatisticCalculation"]

    std_task = exe_kg.add_task(
        kg_schema_short="stats",
        task="DispersionMeasure",
        input_data_entity_dict={"DataInStatisticCalculation": [feature_1]},
        method="Std",
        method_params_dict={},
    )
    std = std_task.output_dict["DataOutStatisticCalculation"]

    canvas_task = exe_kg.add_task(
        kg_schema_short="visu",
        task="CanvasCreation",
        input_data_entity_dict={},
        method="CanvasMethod",
        method_params_dict={"hasParamLayout": "2 1", "hasParamFigureSize": "10 10"},
    )

    exe_kg.add_task(
        kg_schema_short="visu",
        task="LinePlot",
        input_data_entity_dict={"DataInToPlot": [feature_1]},
        method="Plot",
        method_params_dict={"hasParamTitle": "Feature 1"},
    )

    exe_kg.add_task(
        kg_schema_short="visu",
        task="BarPlot",
        input_data_entity_dict={"DataInToPlot": [mean, std]},
        method="Bar",
        method_params_dict={"hasParamTitle": "Feature 1's Mean and Standard Deviation"},
    )

    exe_kg.save_created_kg(f"./pipelines/{pipeline_name}.ttl")
