# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from pathlib import Path

from exe_kg_lib.utils.string_utils import concat_paths

HERE = Path(__file__).parent

KG_SCHEMAS_DIR = "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main"
GENERATED_KG_SCHEMAS_DIR = concat_paths(KG_SCHEMAS_DIR, "generated_schemata")

KG_SCHEMAS = {
    "Data Science": {
        "path": concat_paths(KG_SCHEMAS_DIR, "ds_exeKGOntology.ttl"),
        "shacl_shapes_path": concat_paths(KG_SCHEMAS_DIR, "ds_shacl_shapes.ttl"),
        "namespace": "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/ds_exeKGOntology.ttl#",
        "namespace_prefix": "ds",
        "generated_schema_path": "",
        "generated_shacl_shapes_path": "",
    },
    "Visualization": {
        "path": concat_paths(KG_SCHEMAS_DIR, "visu_exeKGOntology.ttl"),
        "shacl_shapes_path": concat_paths(KG_SCHEMAS_DIR, "visu_shacl_shapes.ttl"),
        "namespace": "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/visu_exeKGOntology.ttl#",
        "namespace_prefix": "visu",
        "generated_schema_path": concat_paths(GENERATED_KG_SCHEMAS_DIR, "generated_visu_schemata_combined.ttl"),
        "generated_shacl_shapes_path": concat_paths(GENERATED_KG_SCHEMAS_DIR, "generated_visu_shacl_shapes.ttl"),
    },
    "Statistics": {
        "path": concat_paths(KG_SCHEMAS_DIR, "stats_exeKGOntology.ttl"),
        "shacl_shapes_path": concat_paths(KG_SCHEMAS_DIR, "stats_shacl_shapes.ttl"),
        "namespace": "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/stats_exeKGOntology.ttl#",
        "namespace_prefix": "stats",
        "generated_schema_path": concat_paths(GENERATED_KG_SCHEMAS_DIR, "generated_stats_schemata_combined.ttl"),
        "generated_shacl_shapes_path": concat_paths(GENERATED_KG_SCHEMAS_DIR, "generated_stats_shacl_shapes.ttl"),
    },
    "Machine Learning": {
        "path": concat_paths(KG_SCHEMAS_DIR, "ml_exeKGOntology.ttl"),
        "shacl_shapes_path": concat_paths(KG_SCHEMAS_DIR, "ml_shacl_shapes.ttl"),
        "namespace": "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/ml_exeKGOntology.ttl#",
        "namespace_prefix": "ml",
        "generated_schema_path": concat_paths(GENERATED_KG_SCHEMAS_DIR, "generated_ml_schemata_combined.ttl"),
        "generated_shacl_shapes_path": concat_paths(GENERATED_KG_SCHEMAS_DIR, "generated_ml_shacl_shapes.ttl"),
    },
}
