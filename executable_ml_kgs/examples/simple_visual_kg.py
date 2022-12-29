from classes import ExeKG

if __name__ == "__main__":
    exe_kg = ExeKG(kg_schema_name="Visualization")
    my_data_entity = exe_kg.create_data_entity(
        "CurrentActual", "CurrentActual", "TimeSeries", "Vector"
    )

    pipeline_name = "testPipeline"
    pipeline = exe_kg.create_pipeline_task(pipeline_name)

    canvas_task_properties = {"hasCanvasName": "mycanvas", "hasLayout": "1 2"}
    canvas_task = exe_kg.add_task(
        prev_task=pipeline,
        task_type="CanvasTask",
        input_data_entity_dict={},
        method_type="CanvasMethod",
        data_properties=canvas_task_properties,
        existing_data_entity_list=[],
    )

    lineplot_task_properties = {
        "hasLegendName": "mylegend",
        "hasLineStyle": "-",
        "hasLineWidth": 1,
    }
    lineplot_task = exe_kg.add_task(
        prev_task=canvas_task,
        task_type="PlotTask",
        input_data_entity_dict={"DataInVector": my_data_entity},
        method_type="LineplotMethod",
        data_properties=lineplot_task_properties,
        existing_data_entity_list=[],
    )

    exe_kg.save(f"../kg/{pipeline_name}.ttl")
