# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from exe_kg_lib import ExeKGConstructor

if __name__ == "__main__":
    exe_kg = ExeKGConstructor()
    my_data_entity = exe_kg.create_data_entity(
        name="feature_1",
        source_value="feature_1",
        data_semantics_name="TimeSeries",
        data_structure_name="Vector",
    )

    pipeline_name = "StatsPipeline"
    pipeline = exe_kg.create_pipeline_task(
        pipeline_name,
        input_data_path="./examples/data/dummy_data.csv",
    )

    normalization_task = exe_kg.add_task(
        kg_schema_short="stats",
        task="NormalizationTask",
        input_data_entity_dict={"DataInNormalization": [my_data_entity]},
        method="NormalizationMethod",
        method_params_dict={},
    )
    norm_output = normalization_task.output_dict["DataOutNormalization"]

    canvas_task = exe_kg.add_task(
        kg_schema_short="visu",
        task="CanvasTask",
        input_data_entity_dict={},
        method="CanvasMethod",
        method_params_dict={"hasCanvasName": "MyCanvas", "hasLayout": "1 1"},
    )

    feature_1_scatterplot_task = exe_kg.add_task(
        kg_schema_short="visu",
        task="PlotTask",
        input_data_entity_dict={
            "DataInVector": [my_data_entity],
        },
        method="ScatterplotMethod",
        method_params_dict={
            "hasLegendName": "Feature 1 before normalization",
            "hasLineStyle": "o",
            "hasScatterStyle": "o",
            "hasLineWidth": 1,
            "hasScatterSize": 1,
        },
    )

    norm_output_scatterplot_task = exe_kg.add_task(
        kg_schema_short="visu",
        task="PlotTask",
        input_data_entity_dict={
            "DataInVector": [norm_output],
        },
        method="ScatterplotMethod",
        method_params_dict={
            "hasLegendName": "Normalized feature 1",
            "hasLineStyle": "o",
            "hasScatterStyle": "o",
            "hasLineWidth": 1,
            "hasScatterSize": 1,
        },
    )

    exe_kg.save_created_kg(f"./pipelines/{pipeline_name}.ttl")
