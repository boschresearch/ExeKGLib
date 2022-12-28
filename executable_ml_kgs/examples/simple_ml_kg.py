from classes import ExeKG

if __name__ == "__main__":
    exe_kg = ExeKG(kg_schema_name="Machine Learning")
    current_actual = exe_kg.create_data_entity(
        "CurrentActual", "CurrentActual", "TimeSeries", "Vector"
    )
    cap_wear_count = exe_kg.create_data_entity(
        "CapWearCount", "CapWearCount", "TimeSeries", "Vector"
    )
    qvalue_actual = exe_kg.create_data_entity(
        "QValueActual", "QVALUEActual", "TimeSeries", "Vector"
    )

    pipeline_name = "testPipeline_ml"
    pipeline = exe_kg.create_pipeline_task(pipeline_name)

    concatenate_task = exe_kg.add_task(
        prev_task=pipeline,
        task_type="Concatenation",
        input_data_entity_dict={"DataInConcatenation": [current_actual, cap_wear_count]},
        method_type="ConcatenationMethod",
        data_properties={},
        existing_data_entity_list=[],
    )

    knn_train_task = exe_kg.add_task(
        prev_task=concatenate_task,
        task_type="Train",
        input_data_entity_dict={"DataInX": [concatenate_task.has_output[0]], "DataInY": [qvalue_actual]},
        method_type="KNNTrain",
        data_properties={},
        existing_data_entity_list=[],
    )

    exe_kg.save(f"../kg/{pipeline_name}.ttl")
