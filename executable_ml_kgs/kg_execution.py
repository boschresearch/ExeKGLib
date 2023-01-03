import sys

from classes import ExeKG

if __name__ == "__main__":
    try:
        exe_kg_path = sys.argv[1]
    except IndexError:
        exe_kg_path = "examples/pipelines/MLPipeline.ttl"

    exe_kg = ExeKG(input_exe_kg_path=exe_kg_path)
    exe_kg.execute_pipeline()
