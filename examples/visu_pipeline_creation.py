# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from exe_kg_lib import ExeKG

if __name__ == "__main__":
    exe_kg = ExeKG(kg_schema_name="Visualization")
    my_data_entity = exe_kg.create_data_entity(
        name="feature_1",
        source_value="feature_1",
        data_semantics_name="TimeSeries",
        data_structure_name="Vector",
    )
    pipeline_name = "VisuPipeline"
    pipeline = exe_kg.create_pipeline_task(
        pipeline_name,
        input_data_path="./examples/data/dummy_data.csv",
    )

    canvas_task_properties = {"hasCanvasName": "MyCanvas", "hasLayout": "1 2"}
    canvas_task = exe_kg.add_task(
        task_type="CanvasTask",
        input_data_entity_dict={},
        method_type="CanvasMethod",
        data_properties=canvas_task_properties,
    )

    lineplot_task_properties = {
        "hasLegendName": "Feature 1",
        "hasLineStyle": "-",
        "hasLineWidth": 1,
    }
    lineplot_task = exe_kg.add_task(
        task_type="PlotTask",
        input_data_entity_dict={"DataInVector": [my_data_entity]},
        method_type="LineplotMethod",
        data_properties=lineplot_task_properties,
    )

    exe_kg.save_created_kg(f"./pipelines/{pipeline_name}.ttl")
