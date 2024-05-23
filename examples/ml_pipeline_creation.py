# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from pathlib import Path

from exe_kg_lib import ExeKGConstructor

HERE = Path(__file__).resolve().parent

if __name__ == "__main__":
    exe_kg = ExeKGConstructor()
    feature_columns = ["feature_1", "feature_2", "feature_3", "feature_4", "feature_5"]
    label_column = "label"

    feature_data_entities = []
    for feature_column in feature_columns:
        feature_data_entities.append(
            exe_kg.create_data_entity(
                name=feature_column,
                source_value=feature_column,
                data_semantics_name="Numerical",
                data_structure_name="Vector",
            )
        )

    label_data_entity = exe_kg.create_data_entity(
        name=label_column,
        source_value=label_column,
        data_semantics_name="Categorical",
        data_structure_name="Vector",
    )

    pipeline_name = "MLPipeline"
    pipeline = exe_kg.create_pipeline_task(
        pipeline_name,
        input_data_path=HERE / "data" / "dummy_data.csv",
        plots_output_dir=HERE / "plots" / pipeline_name,
    )

    concatenate_task = exe_kg.add_task(
        kg_schema_short="ml",
        input_data_entity_dict={"DataInConcatenation": feature_data_entities},
        method="ConcatenationMethod",
        method_params_dict={},
        task="Concatenation",
    )

    data_splitting_task = exe_kg.add_task(
        kg_schema_short="ml",
        task="DataSplitting",
        input_data_entity_dict={
            "DataInDataSplittingX": [concatenate_task.output_dict["DataOutConcatenatedData"]],
            "DataInDataSplittingY": [label_data_entity],
        },
        method="TrainTestSplitMethod",
        method_params_dict={"hasParamTestSize": 0.2, "hasParamRandomState": 0},
    )

    train_x = data_splitting_task.output_dict["DataOutSplittedTrainDataX"]
    train_real_y = data_splitting_task.output_dict["DataOutSplittedTrainDataY"]
    test_x = data_splitting_task.output_dict["DataOutSplittedTestDataX"]
    test_real_y = data_splitting_task.output_dict["DataOutSplittedTestDataY"]

    knn_train_task = exe_kg.add_task(
        kg_schema_short="ml",
        task="BinaryClassification",
        input_data_entity_dict={
            "DataInTrainX": [train_x],
            "DataInTrainY": [train_real_y],
        },
        method="SVCMethod",
        method_params_dict={"hasParamRandomState": 0},
    )
    model = knn_train_task.output_dict["DataOutTrainModel"]
    # train_predicted_y = knn_train_task.output_dict["DataOutPredictedValueTrain"]

    knn_test_task = exe_kg.add_task(
        kg_schema_short="ml",
        task="Test",
        method="TestMethod",
        input_data_entity_dict={
            "DataInTestModel": [model],
            "DataInTestX": [test_x],
        },
        # method="SVC",
        method_params_dict={},
    )
    test_predicted_y = knn_test_task.output_dict["DataOutPredictedValueTest"]

    performance_calc_task = exe_kg.add_task(
        kg_schema_short="ml",
        task="PerformanceCalculation",
        input_data_entity_dict={
            "DataInRealY": [test_real_y],
            "DataInPredictedY": [test_predicted_y],
        },
        method="AccuracyScoreMethod",
        method_params_dict={},
    )
    test_accuracy = performance_calc_task.output_dict["DataOutScore"]

    performance_calc_task = exe_kg.add_task(
        kg_schema_short="ml",
        task="PerformanceCalculation",
        input_data_entity_dict={
            "DataInRealY": [test_real_y],
            "DataInPredictedY": [test_predicted_y],
        },
        method="F1ScoreMethod",
        method_params_dict={},
    )
    test_f1 = performance_calc_task.output_dict["DataOutScore"]

    performance_calc_task = exe_kg.add_task(
        kg_schema_short="ml",
        task="PerformanceCalculation",
        input_data_entity_dict={
            "DataInRealY": [test_real_y],
            "DataInPredictedY": [test_predicted_y],
        },
        method="PrecisionScoreMethod",
        method_params_dict={},
    )
    test_precision = performance_calc_task.output_dict["DataOutScore"]

    performance_calc_task = exe_kg.add_task(
        kg_schema_short="ml",
        task="PerformanceCalculation",
        input_data_entity_dict={
            "DataInRealY": [test_real_y],
            "DataInPredictedY": [test_predicted_y],
        },
        method="RecallScoreMethod",
        method_params_dict={},
    )
    test_recall = performance_calc_task.output_dict["DataOutScore"]

    exe_kg.add_task(
        kg_schema_short="visu",
        task="CanvasCreation",
        input_data_entity_dict={},
        method="CanvasMethod",
        method_params_dict={"hasParamLayout": "2 1", "hasParamFigureSize": "10 10"},
    )

    exe_kg.add_task(
        kg_schema_short="visu",
        task="BarPlotting",
        input_data_entity_dict={
            "DataInToPlot": [test_accuracy, test_f1],
        },
        method="BarMethod",
        method_params_dict={
            "hasParamTitle": "Test Accuracy & F1",
        },
    )

    exe_kg.add_task(
        kg_schema_short="visu",
        task="BarPlotting",
        input_data_entity_dict={
            "DataInToPlot": [test_precision, test_recall],
        },
        method="BarMethod",
        method_params_dict={
            "hasParamTitle": "Test Precision & Recall",
        },
    )

    exe_kg.save_created_kg(HERE / "pipelines")
