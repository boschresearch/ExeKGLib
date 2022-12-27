from classes import ExeKG

if __name__ == "__main__":
    pipeline_name = "testPipeline"
    exe_kg = ExeKG(kg_schema_name="Visual")
    exe_kg.start_pipeline_creation(pipeline_name)
    exe_kg.save(f"kg/{pipeline_name}.ttl")
