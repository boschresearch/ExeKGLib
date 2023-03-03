# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from exe_kg_lib import ExeKG

if __name__ == "__main__":
    exe_kg = ExeKG(kg_schema_name="Machine Learning")
    feature_columns = ["feature_1", "feature_2", "feature_3", "feature_4", "feature_5"]
    label_column = "label"

    feature_data_entities = []
    for feature_column in feature_columns:
        feature_data_entities.append(
            exe_kg.create_data_entity(
                name=feature_column,
                source_value=feature_column,
                data_semantics_name="TimeSeries",
                data_structure_name="Vector",
            )
        )

    label_data_entity = exe_kg.create_data_entity(
        name=label_column,
        source_value=label_column,
        data_semantics_name="TimeSeries",
        data_structure_name="Vector",
    )

    pipeline_name = "MLPipeline"
    pipeline = exe_kg.create_pipeline_task(
        pipeline_name,
        input_data_path="./examples/data/dummy_data.csv",
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
            "DataInDataSplittingX": [concatenate_task.output_dict["DataOutConcatenatedData"]],
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

    exe_kg.save_created_kg(f"./pipelines/{pipeline_name}.ttl")
