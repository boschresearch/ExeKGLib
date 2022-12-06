from classes.graph import ExeKG

if __name__ == "__main__":
    pipeline_name = "testPipeline"

    exe_kg = ExeKG()
    exe_kg.parse_ontology("kg/exeKGOntology.ttl")
    exe_kg.start_pipeline_creation(pipeline_name)
    exe_kg.save(f"kg/{pipeline_name}.ttl")
