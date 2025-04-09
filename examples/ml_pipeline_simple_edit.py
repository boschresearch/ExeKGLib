# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from pathlib import Path

from exe_kg_lib.classes.exe_kg_actors import ExeKGEditor

HERE = Path(__file__).resolve().parent

exe_kg_editor = ExeKGEditor(str(HERE / "pipelines" / "MLPipelineSimple.ttl"))

# NOTE: updating the metric values should be done with caution, as the values should be consistent with the actual performance of the pipeline
exe_kg_editor.update_metric_values({"DataOutScore_PerformanceCalculation2_MLPipelineSimple_F1ScoreMethod": 0.22})

feature_columns = ["feature_1", "feature_2"]
label_column = "label"

# create data entities for the new features and label
feature_data_entities = []
for feature_column in feature_columns:
    feature_data_entities.append(
        exe_kg_editor.create_data_entity(
            name=feature_column,
            source_value=feature_column,
            data_semantics_name="Numerical",
            data_structure_name="Vector",
        )
    )

label_data_entity = exe_kg_editor.create_data_entity(
    name=label_column,
    source_value=label_column,
    data_semantics_name="Categorical",
    data_structure_name="Vector",
)

# update the dataset with the new features and label
exe_kg_editor.update_dataset(
    new_dataset_path="examples/data/dummy_data.csv",
    new_feature_data_entities=feature_data_entities,
    new_label_data_entity=label_data_entity,
)

# update the parameter values for some of the pipeline's methods
exe_kg_editor.update_param_values(
    {
        ("visu", "CanvasMethod1_MLPipelineSimple"): {"hasParamFigureSize": "8 10"},
        ("ml", "TrainTestSplitMethod1_MLPipelineSimple"): {"hasParamRandomState": 1},
    }
)

exe_kg_editor.update_pipeline_name("MLPipelineSimpleUpdated")

exe_kg_editor.apply_changes_to_ttl(HERE / "pipelines" / "MLPipelineSimpleUpdated.ttl")
