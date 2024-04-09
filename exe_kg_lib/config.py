from pathlib import Path

from exe_kg_lib.utils.string_utils import concat_paths

HERE = Path(__file__).parent

# KG_SCHEMAS_DIR = HERE / ".." / ".." / "ExeKGOntology"
# KG_SCHEMAS_DIR = "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main"
KG_SCHEMAS_DIR = "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/add-new-tasks-and-methods"

KG_SCHEMAS = {
    "Data Science": {
        "path": concat_paths(KG_SCHEMAS_DIR, "ds_exeKGOntology.ttl"),
        "namespace": "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/ds_exeKGOntology.ttl#",
        "namespace_prefix": "ds",
        "generated_schema_path": "",
    },
    "Visualization": {
        "path": concat_paths(KG_SCHEMAS_DIR, "visu_exeKGOntology.ttl"),
        "namespace": "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/visu_exeKGOntology.ttl#",
        "namespace_prefix": "visu",
        "generated_schema_path": concat_paths(KG_SCHEMAS_DIR, "generated_visu_ontologies_combined.ttl"),
    },
    "Statistics": {
        "path": concat_paths(KG_SCHEMAS_DIR, "stats_exeKGOntology.ttl"),
        "namespace": "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/stats_exeKGOntology.ttl#",
        "namespace_prefix": "stats",
        "generated_schema_path": concat_paths(KG_SCHEMAS_DIR, "generated_stats_ontologies_combined.ttl"),
    },
    "Machine Learning": {
        "path": concat_paths(KG_SCHEMAS_DIR, "ml_exeKGOntology.ttl"),
        "namespace": "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/ml_exeKGOntology.ttl#",
        "namespace_prefix": "ml",
        "generated_schema_path": concat_paths(KG_SCHEMAS_DIR, "generated_ml_ontologies_combined.ttl"),
    },
}
