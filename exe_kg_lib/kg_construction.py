from classes import ExeKG
from utils.cli_utils import input_pipeline_info

if __name__ == "__main__":
    pipeline_name, input_data_path = input_pipeline_info()
    kg_schema_name = ExeKG.input_kg_schema_name()
    exe_kg = ExeKG(kg_schema_name=kg_schema_name)
    exe_kg.start_pipeline_creation(pipeline_name, input_data_path)
    exe_kg.save_created_kg(f"kg/{pipeline_name}.ttl")
