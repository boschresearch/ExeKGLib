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
        data_semantics_name="Numerical",
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
        task_type="CentralTendencyMeasure",
        input_entity_dict={"DataInStatisticCalculation": [feature_1]},
        method_type="MeanMethod",
        method_params_dict={},
    )
    mean = mean_task.output_dict["DataOutStatisticCalculation"]

    std_task = exe_kg.add_task(
        kg_schema_short="stats",
        task_type="DispersionMeasure",
        input_entity_dict={"DataInStatisticCalculation": [feature_1]},
        method_type="StdMethod",
        method_params_dict={},
    )
    std = std_task.output_dict["DataOutStatisticCalculation"]

    canvas_task = exe_kg.add_task(
        kg_schema_short="visu",
        task_type="CanvasCreation",
        input_entity_dict={},
        method_type="CanvasMethod",
        method_params_dict={"hasParamLayout": "2 1", "hasParamFigureSize": "10 10"},
    )

    exe_kg.add_task(
        kg_schema_short="visu",
        task_type="LinePlotting",
        input_entity_dict={"DataInToPlot": [feature_1]},
        method_type="PlotMethod",
        method_params_dict={
            "hasParamTitle": "Feature 1",
            "hasParamAnnotate": False,
        },
    )

    exe_kg.add_task(
        kg_schema_short="visu",
        task_type="BarPlotting",
        input_entity_dict={"DataInToPlot": [mean, std]},
        method_type="BarMethod",
        method_params_dict={
            "hasParamTitle": "Feature 1's Mean and Standard Deviation",
            "hasParamAnnotate": True,
        },
    )

    exe_kg.save_created_kg(HERE / "pipelines")
