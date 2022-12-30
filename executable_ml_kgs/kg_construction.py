from classes import ExeKG
from utils.cli_utils import input_pipeline_info

if __name__ == "__main__":
    pipeline_name, input_data_path = input_pipeline_info()
    exe_kg = ExeKG(kg_schema_name="Machine Learning")
    exe_kg.start_pipeline_creation(pipeline_name, input_data_path)
    exe_kg.save(f"kg/{pipeline_name}.ttl")
