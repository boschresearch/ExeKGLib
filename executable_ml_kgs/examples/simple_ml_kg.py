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
    pipeline = exe_kg.create_pipeline_task(
        pipeline_name, input_data_path="data/singlefeatures_wm1.csv"
    )

    concatenate_task = exe_kg.add_task(
        task_type="Concatenation",
        input_data_entity_dict={
            "DataInConcatenation": [current_actual, cap_wear_count]
        },
        method_type="ConcatenationMethod",
        data_properties={},
    )

    data_splitting_task = exe_kg.add_task(
        task_type="DataSplitting",
        input_data_entity_dict={
            "DataInDataSplittingX": [
                concatenate_task.output_dict["DataOutConcatenatedData"]
            ],
            "DataInDataSplittingY": [qvalue_actual],
        },
        method_type="DataSplittingMethod",
        data_properties={"hasSplitRatio": 0.8},
    )

    train_x = data_splitting_task.output_dict["DataOutSplittedTrainDataX"]
    train_real_y = data_splitting_task.output_dict["DataOutSplittedTrainDataY"]
    test_x = data_splitting_task.output_dict["DataOutSplittedTestDataX"]
    test_real_y = data_splitting_task.output_dict["DataOutSplittedTestDataY"]

    knn_train_task = exe_kg.add_task(
        task_type="Train",
        input_data_entity_dict={
            "DataInTrainX": [train_x],
            "DataInTrainY": [train_real_y],
        },
        method_type="KNNTrain",
        data_properties={},
    )
    model = knn_train_task.output_dict["DataOutTrainModel"]
    train_predicted_y = knn_train_task.output_dict["DataOutPredictedValueTrain"]

    knn_test_task = exe_kg.add_task(
        task_type="Test",
        input_data_entity_dict={
            "DataInTestModel": [model],
            "DataInTestX": [test_x],
        },
        method_type="KNNTest",
        data_properties={},
    )
    test_predicted_y = knn_test_task.output_dict["DataOutPredictedValueTest"]

    performance_calc_task = exe_kg.add_task(
        task_type="PerformanceCalculation",
        input_data_entity_dict={
            "DataInTrainRealY": [train_real_y],
            "DataInTrainPredictedY": [train_predicted_y],
            "DataInTestRealY": [test_real_y],
            "DataInTestPredictedY": [test_predicted_y],
        },
        method_type="PerformanceCalculationMethod",
        data_properties={},
    )
    train_error = performance_calc_task.output_dict["DataOutMLTrainErr"]
    test_error = performance_calc_task.output_dict["DataOutMLTestErr"]

    canvas_task = exe_kg.add_task(
        task_type="CanvasTask",
        input_data_entity_dict={},
        method_type="CanvasMethod",
        data_properties={"hasCanvasName": "MyCanvas", "hasLayout": "1 1"},
        visualization=True,
    )

    train_error_lineplot_task = exe_kg.add_task(
        task_type="PlotTask",
        input_data_entity_dict={
            "DataInVector": [train_error],
        },
        method_type="LineplotMethod",
        data_properties={
            "hasLegendName": "MyLegend",
            "hasLineStyle": "-",
            "hasLineWidth": 1,
        },
        visualization=True,
    )

    test_error_lineplot_task = exe_kg.add_task(
        task_type="PlotTask",
        input_data_entity_dict={
            "DataInVector": [test_error],
        },
        method_type="LineplotMethod",
        data_properties={
            "hasLegendName": "MyLegend",
            "hasLineStyle": "-",
            "hasLineWidth": 1,
        },
        visualization=True,
    )

    exe_kg.save(f"../kg/{pipeline_name}.ttl")
