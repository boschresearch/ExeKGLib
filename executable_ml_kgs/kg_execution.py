from classes import ExeKG

if __name__ == "__main__":
    exe_kg = ExeKG(input_exe_kg_path="./kg/testPipeline_ml.ttl")
    # exe_kg = ExeKG(input_exe_kg_path="./kg/testPipeline_visu.ttl")
    exe_kg.execute_pipeline()
