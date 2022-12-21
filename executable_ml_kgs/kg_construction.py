from classes.graph import ExeKG

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
    # exe_kg.parse_ontology("https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/ds_exeKGOntology.ttl")
    exe_kg.start_pipeline_creation(pipeline_name)
    exe_kg.save(f"kg/{pipeline_name}.ttl")
