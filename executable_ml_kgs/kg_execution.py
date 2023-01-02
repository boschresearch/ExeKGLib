from classes import ExeKG

if __name__ == "__main__":
    exe_kg = ExeKG(input_exe_kg_path="./examples/pipelines/MLPipeline.ttl")
    # exe_kg = ExeKG(input_exe_kg_path="./examples/pipelines/VisuPipeline.ttl")
    exe_kg.execute_pipeline()
