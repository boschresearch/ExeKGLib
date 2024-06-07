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

    pipeline_name = "MLPipelineCrossValidation"
    pipeline = exe_kg.create_pipeline_task(
        pipeline_name,
        input_data_path=HERE / "data" / "dummy_data.csv",
        plots_output_dir=HERE / "plots" / pipeline_name,
    )

    concatenate_task = exe_kg.add_task(
        kg_schema_short="ml",
        input_entity_dict={"DataInConcatenation": feature_data_entities},
        method_type="ConcatenationMethod",
        method_params_dict={},
        task_type="Concatenation",
    )

    data_splitting_task = exe_kg.add_task(
        kg_schema_short="ml",
        task_type="DataSplitting",
        input_entity_dict={
            "DataInDataSplittingX": [concatenate_task.output_dict["DataOutConcatenatedData"]],
            "DataInDataSplittingY": [label_data_entity],
        },
        method_type="TrainTestSplitMethod",
        method_params_dict={"hasParamTestSize": 0.2, "hasParamRandomState": 0},
    )

    train_x = data_splitting_task.output_dict["DataOutSplittedTrainDataX"]
    train_real_y = data_splitting_task.output_dict["DataOutSplittedTrainDataY"]
    test_x = data_splitting_task.output_dict["DataOutSplittedTestDataX"]
    test_real_y = data_splitting_task.output_dict["DataOutSplittedTestDataY"]

    cv_task = exe_kg.add_task(
        kg_schema_short="ml",
        task_type="DataSplitting",
        input_entity_dict={
            "DataInDataSplittingX": [train_x],
            "DataInDataSplittingY": [train_real_y],
        },
        method_type="StratifiedKFoldMethod",
        method_params_dict={"hasParamNSplits": 3},
    )

    cv_train_x = cv_task.output_dict["DataOutSplittedTrainDataX"]
    cv_train_real_y = cv_task.output_dict["DataOutSplittedTrainDataY"]
    cv_test_x = cv_task.output_dict["DataOutSplittedTestDataX"]
    cv_test_real_y = cv_task.output_dict["DataOutSplittedTestDataY"]

    train_task = exe_kg.add_task(
        kg_schema_short="ml",
        task_type="BinaryClassification",
        input_entity_dict={
            "DataInTrainX": [cv_train_x],
            "DataInTrainY": [cv_train_real_y],
        },
        method_type="SVCMethod",
        method_params_dict={"hasParamRandomState": 0},
    )
    model = train_task.output_dict["DataOutTrainModel"]

    cv_test_task = exe_kg.add_task(
        kg_schema_short="ml",
        task_type="Test",
        method_type="TestMethod",
        input_entity_dict={
            "DataInTestModel": [model],
            "DataInTestX": [cv_test_x],
        },
        method_params_dict={},
    )
    cv_test_predicted_y = cv_test_task.output_dict["DataOutPredictedValueTest"]

    test_task = exe_kg.add_task(
        kg_schema_short="ml",
        task_type="Test",
        method_type="TestMethod",
        input_entity_dict={
            "DataInTestModel": [model],
            "DataInTestX": [test_x],
        },
        method_params_dict={},
    )
    test_predicted_y = test_task.output_dict["DataOutPredictedValueTest"]

    performance_calc_task = exe_kg.add_task(
        kg_schema_short="ml",
        task_type="PerformanceCalculation",
        input_entity_dict={
            "DataInRealY": [cv_test_real_y],
            "DataInPredictedY": [cv_test_predicted_y],
        },
        method_type="F1ScoreMethod",
        method_params_dict={},
    )
    cv_test_f1 = performance_calc_task.output_dict["DataOutScore"]

    performance_calc_task = exe_kg.add_task(
        kg_schema_short="ml",
        task_type="PerformanceCalculation",
        input_entity_dict={
            "DataInRealY": [test_real_y],
            "DataInPredictedY": [test_predicted_y],
        },
        method_type="F1ScoreMethod",
        method_params_dict={},
    )
    test_f1 = performance_calc_task.output_dict["DataOutScore"]

    exe_kg.add_task(
        kg_schema_short="visu",
        task_type="CanvasCreation",
        input_entity_dict={},
        method_type="CanvasMethod",
        method_params_dict={"hasParamLayout": "1 1", "hasParamFigureSize": "10 5"},
    )

    exe_kg.add_task(
        kg_schema_short="visu",
        task_type="BarPlotting",
        input_entity_dict={
            "DataInToPlot": [cv_test_f1, test_f1],
        },
        method_type="BarMethod",
        method_params_dict={
            "hasParamTitle": "Validation F1-score and Test F1-score",
        },
    )

    exe_kg.save_created_kg(HERE / "pipelines")
