import pandas as pd

from classes.graph import ExeKG

exe_kg_namespaces_and_ontologies = {
    "Data Science": (
        "http://www.semanticweb.org/ontologies/ds#",
        "https://raw.githubusercontent.com/baifanzhou/ExeKGOntology/main/ds_exeKGOntology.ttl",
    ),
    "Visual": (
        "http://www.semanticweb.org/ontologies/visu#",
        "https://raw.githubusercontent.com/baifanzhou/ExeKGOntology/main/visu_exeKGOntology.ttl",
    ),
    "Statistics": (
        "http://www.semanticweb.org/ontologies/stats#",
        "https://raw.githubusercontent.com/baifanzhou/ExeKGOntology/main/stats_exeKGOntology.ttl",
    ),
    "Machine Learning": (
        "http://www.semanticweb.org/ontologies/ml#",
        "https://raw.githubusercontent.com/baifanzhou/ExeKGOntology/main/ml_exeKGOntology.ttl",
    ),
    "generic": (
        "http://www.semanticweb.org/zhuoxun/ontologies/exeKG#",
        "./kg/exeKGExampleKNN_noVisu.ttl",
        # "./kg/exeKGExampleKNN_noVisu.ttl",
    ),
}

if __name__ == "__main__":

    chosen_exe_kg_type = "generic"  # TODO: get user input
    namespace_iri, ontology_url = exe_kg_namespaces_and_ontologies[chosen_exe_kg_type]

    input_data = pd.read_csv(
        r"data/singlefeatures_wm1.csv", delimiter=",", encoding="ISO-8859-1"
    )  # TODO: read data dynamically

    exe_kg = ExeKG(namespace_iri, ontology_url)
    # exe_kg.parse_ontology("https://raw.githubusercontent.com/baifanzhou/ExeKGOntology/main/ds_exeKGOntology.ttl")

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
