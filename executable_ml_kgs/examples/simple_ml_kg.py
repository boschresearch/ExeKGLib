from classes import ExeKG

if __name__ == "__main__":
    exe_kg = ExeKG(kg_schema_name="Machine Learning")
    feature_columns = [
        "diagnosis",
        "radius_mean",
        "texture_mean",
        "perimeter_mean",
        "area_mean",
        "smoothness_mean",
        "compactness_mean",
        "concavity_mean",
        "concave_points_mean",
        "symmetry_mean",
        "fractal_dimension_mean",
        "radius_se",
        "texture_se",
        "perimeter_se",
        "area_se",
        "smoothness_se",
        "compactness_se",
        "concavity_se",
        "concave_points_se",
        "symmetry_se",
        "fractal_dimension_se",
        "radius_worst",
        "texture_worst",
        "perimeter_worst",
        "area_worst",
        "smoothness_worst",
        "compactness_worst",
        "concavity_worst",
        "concave_points_worst",
        "symmetry_worst",
        "fractal_dimension_worst",
        "diagnosis_binary",
    ]

    label_column = "diagnosis_binary"

    feature_data_entities = []
    for feature_column in feature_columns:
        feature_data_entities.append(
            exe_kg.create_data_entity(
                "feature_" + feature_column, feature_column, "TimeSeries", "Vector"
            )
        )

    label_data_entity = exe_kg.create_data_entity(
        "label_" + label_column, label_column, "TimeSeries", "Vector"
    )

    pipeline_name = "MLPipeline"
    pipeline = exe_kg.create_pipeline_task(
        pipeline_name, input_data_path="examples/data/breast_cancer_data.csv"
    )

    concatenate_task = exe_kg.add_task(
        task_type="Concatenation",
        input_data_entity_dict={"DataInConcatenation": feature_data_entities},
        method_type="ConcatenationMethod",
        data_properties={},
    )

    data_splitting_task = exe_kg.add_task(
        task_type="DataSplitting",
        input_data_entity_dict={
            "DataInDataSplittingX": [
                concatenate_task.output_dict["DataOutConcatenatedData"]
            ],
            "DataInDataSplittingY": [label_data_entity],
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
        method_type="ScatterplotMethod",
        data_properties={
            "hasLegendName": "Train error",
            "hasLineStyle": "o",
            "hasScatterStyle": "o",
            "hasLineWidth": 1,
            "hasScatterSize": 1,
        },
        visualization=True,
    )

    test_error_lineplot_task = exe_kg.add_task(
        task_type="PlotTask",
        input_data_entity_dict={
            "DataInVector": [test_error],
        },
        method_type="ScatterplotMethod",
        data_properties={
            "hasLegendName": "Test error",
            "hasLineStyle": "o",
            "hasScatterStyle": "o",
            "hasLineWidth": 1,
            "hasScatterSize": 1,
        },
        visualization=True,
    )

    exe_kg.save(f"./pipelines/{pipeline_name}.ttl")
