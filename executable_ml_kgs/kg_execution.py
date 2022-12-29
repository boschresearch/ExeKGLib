import pandas as pd

from classes import ExeKG

if __name__ == "__main__":
    input_data = pd.read_csv(
        r"data/singlefeatures_wm1.csv", delimiter=",", encoding="ISO-8859-1"
    )  # TODO: read data dynamically

    exe_kg = ExeKG(input_exe_kg_path="./kg/testPipeline_ml.ttl")
    exe_kg.execute_pipeline(input_data)
