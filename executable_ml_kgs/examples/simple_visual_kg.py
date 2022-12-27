from classes import ExeKG

kg_paths_and_prefixes = {
    "Data Science": (
        "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/ds_exeKGOntology.ttl",
        "ds",
    ),
    "Visual": (
        "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/visu_exeKGOntology.ttl",
        "visu",
    ),
    "Statistics": (
        "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/stats_exeKGOntology.ttl",
        "stats",
    ),
    "Machine Learning": (
        "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/ml_exeKGOntology.ttl",
        "ml",
    ),
}

if __name__ == "__main__":
    pipeline_name = "testPipeline"

    top_level_kg_schema_path, top_level_kg_schema_prefix = kg_paths_and_prefixes[
        "Data Science"
    ]

    chosen_exe_kg_type = "Visual"  # TODO: get user input
    chosen_kg_schema_path, chosen_kg_schema_prefix = kg_paths_and_prefixes[
        chosen_exe_kg_type
    ]
    exe_kg = ExeKG(
        chosen_kg_schema_path + "#",
        "../../ExeKGOntology/visu_exeKGOntology.ttl",
        chosen_kg_schema_prefix,
        top_level_kg_schema_path + "#",
        top_level_kg_schema_path,
        top_level_kg_schema_prefix,
    )
    my_data_entity = exe_kg.create_data_entity(
        "CurrentActual", "CurrentActual", "TimeSeries", "Vector"
    )

    pipeline = exe_kg.create_pipeline_task(pipeline_name)

    canvas_task_properties = {"hasCanvasName": "mycanvas", "hasLayout": "1 2"}
    canvas_task = exe_kg.add_task(
        prev_task=pipeline,
        task_type="CanvasTask",
        input_data_entities=[],
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
        input_data_entities=[my_data_entity],
        method_type="LineplotMethod",
        data_properties=lineplot_task_properties,
        existing_data_entity_list=[],
    )

    exe_kg.save(f"../kg/{pipeline_name}.ttl")
