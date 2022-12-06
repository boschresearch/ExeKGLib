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
}

if __name__ == "__main__":
    pipeline_name = "testPipeline"

    chosen_exe_kg_type = "Visual"  # TODO: get user input
    namespace_iri, ontology_url = exe_kg_namespaces_and_ontologies[chosen_exe_kg_type]
    exe_kg = ExeKG(namespace_iri, ontology_url)
    # exe_kg.parse_ontology("https://raw.githubusercontent.com/baifanzhou/ExeKGOntology/main/ds_exeKGOntology.ttl")
    exe_kg.start_pipeline_creation(pipeline_name)
    exe_kg.save(f"kg/{pipeline_name}.ttl")
