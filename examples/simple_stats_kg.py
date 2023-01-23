# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from classes import ExeKG

if __name__ == "__main__":
    exe_kg = ExeKG(kg_schema_name="Statistics")
    my_data_entity = exe_kg.create_data_entity(
        name="feature_1",
        source_value="feature_1",
        data_semantics_name="TimeSeries",
        data_structure_name="Vector",
    )

    pipeline_name = "StatsPipeline"
    pipeline = exe_kg.create_pipeline_task(
        pipeline_name,
        input_data_path="../examples/data/dummy_data.csv",  # relative to kg_execution.py
    )

    normalization_task = exe_kg.add_task(
        task_type="NormalizationTask",
        input_data_entity_dict={"DataInNormalization": [my_data_entity]},
        method_type="NormalizationMethod",
        data_properties={},
    )
    norm_output = normalization_task.output_dict["DataOutNormalization"]

    canvas_task = exe_kg.add_task(
        task_type="CanvasTask",
        input_data_entity_dict={},
        method_type="CanvasMethod",
        data_properties={"hasCanvasName": "MyCanvas", "hasLayout": "1 1"},
        visualization=True,
    )

    feature_1_scatterplot_task = exe_kg.add_task(
        task_type="PlotTask",
        input_data_entity_dict={
            "DataInVector": [my_data_entity],
        },
        method_type="ScatterplotMethod",
        data_properties={
            "hasLegendName": "Feature 1 before normalization",
            "hasLineStyle": "o",
            "hasScatterStyle": "o",
            "hasLineWidth": 1,
            "hasScatterSize": 1,
        },
        visualization=True,
    )

    norm_output_scatterplot_task = exe_kg.add_task(
        task_type="PlotTask",
        input_data_entity_dict={
            "DataInVector": [norm_output],
        },
        method_type="ScatterplotMethod",
        data_properties={
            "hasLegendName": "Normalized feature 1",
            "hasLineStyle": "o",
            "hasScatterStyle": "o",
            "hasLineWidth": 1,
            "hasScatterSize": 1,
        },
        visualization=True,
    )

    exe_kg.save_created_kg(f"./pipelines/{pipeline_name}.ttl")
