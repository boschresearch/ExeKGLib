import pandas as pd

from classes import ExeKG

if __name__ == "__main__":
    input_data = pd.read_csv(
        r"data/singlefeatures_wm1.csv", delimiter=",", encoding="ISO-8859-1"
    )  # TODO: read data dynamically

    exe_kg = ExeKG(input_exe_kg_path="./kg/testPipeline_ml.ttl")

    pipeline_iri, next_task_iri = exe_kg.get_pipeline_and_first_task_iri()
    canvas_method = None
    task_output_dict = {}
    while next_task_iri is not None:
        next_task = exe_kg.parse_task_by_iri(next_task_iri, canvas_method)
        output = next_task.run_method(task_output_dict, input_data)
        if output:
            task_output_dict.update(output)
        # TODO: plot results of tasks for stats pipeline

        if next_task.type == "CanvasTask":
            canvas_method = next_task

        next_task_iri = next_task.has_next_task
