# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

import os
from io import TextIOWrapper
from pathlib import Path
from typing import Callable, Dict, List, Tuple, Union

from rdflib import RDF, Graph, URIRef

from exe_kg_lib.classes.data_entity import DataEntity
from exe_kg_lib.classes.entity import Entity
from exe_kg_lib.classes.exe_kg_serialization.pipeline import Pipeline
from exe_kg_lib.classes.kg_schema import KGSchema
from exe_kg_lib.classes.method import Method
from exe_kg_lib.classes.task import Task
from exe_kg_lib.utils.kg_creation_utils import (add_data_entity_instance,
                                                add_relation,
                                                field_value_to_literal,
                                                load_exe_kg, save_exe_kg)
from exe_kg_lib.utils.kg_edit_utils import (update_metric_values,
                                            update_pipeline_input_path)
from exe_kg_lib.utils.query_utils import get_pipeline_and_first_task_iri


class ExeKGEditMixin:
    # see exe_kg_lib/classes/exe_kg_base.py for the definition of these attributes
    exe_kg: Graph
    input_kg: Graph
    top_level_schema: KGSchema
    bottom_level_schemata: Dict[str, KGSchema]
    atomic_task: Entity
    pipeline_serializable: Pipeline
    task_type_dict: Dict[str, int]
    data: Entity
    pipeline: Entity
    # see exe_kg_lib/classes/exe_kg_mixins/exe_kg_construction_mixin.py for the definition of these attributes
    create_exe_kg_from_json: Callable[[Union[Path, TextIOWrapper, str]], Graph]
    add_task: Callable[
        [
            str,
            Dict[str, Union[List[DataEntity], Method]],
            Dict[str, Union[str, int, float, dict]],
            str,
            str,
        ],
        Task,
    ]
    clear_created_kg: Callable[[], None]

    def __init__(self, input_exe_kg_path: str = None) -> None:
        super().__init__()

        if input_exe_kg_path:
            self.load_exe_kg(input_exe_kg_path)

    def load_exe_kg(self, input_exe_kg_path: str) -> None:
        """
        Resets ExeKG creation state and loads an ExeKG from the specified path.

        Args:
            input_exe_kg_path (str): The path to the input executable knowledge graph.

        Returns:
            None
        """
        self.input_exe_kg_path = input_exe_kg_path

        self.clear_created_kg()
        self.exe_kg = load_exe_kg(
            input_exe_kg_path, self.create_exe_kg_from_json if input_exe_kg_path.endswith(".json") else None
        )

    def update_metric_values(self, output_name_value_dict: Dict[str, Union[str, int, float, bool]]) -> None:
        """
        Updates the metric values in the ExeKG instance.

        Args:
            output_name_value_dict (Dict[str, Union[str, int, float, bool]]): A dictionary containing the metric names as keys
                and their corresponding values as values. The values can be of type str, int, float, or bool.

        Returns:
            None
        """
        update_metric_values(
            self.exe_kg,
            output_name_value_dict,
            self.bottom_level_schemata["ml"].namespace,
            self.top_level_schema.namespace,
        )

    def update_param_values(
        self, method_info_params_dict: Dict[Tuple[str, str], Dict[str, Union[str, int, float, bool]]]
    ):
        """
        Update the parameter values for a given method in the knowledge graph.

        Args:
            method_info_params_dict (Dict[Tuple[str, str], Dict[str, Union[str, int, float, bool]]]):
                A dictionary containing the method information as keys and parameter dictionary as values.
                The method information is represented as a tuple of (method_ns_prefix, method_name).
                The parameter dictionary contains parameter names as keys and parameter values as values.

        Returns:
            None
        """
        for (method_ns_prefix, method_name), param_dict in method_info_params_dict.items():
            namespace = self.bottom_level_schemata[method_ns_prefix].namespace
            method_iri = URIRef(namespace + method_name)
            for param_name, param_value in param_dict.items():
                self.exe_kg.remove(
                    (
                        method_iri,
                        URIRef(namespace + param_name),
                        None,
                    )
                )
                self.exe_kg.add(
                    (
                        method_iri,
                        URIRef(namespace + param_name),
                        field_value_to_literal(param_value),
                    )
                )

    def update_dataset(
        self,
        new_dataset_path: str,
        new_feature_data_entities: List[DataEntity],
        new_label_data_entity: DataEntity,
    ):
        """
        Update the dataset used in the ExeKG.

        Args:
            new_dataset_path (str): The path to the new dataset.
            new_feature_data_entities (List[DataEntity]): The list of new feature data entities.
            new_label_data_entity (DataEntity): The new label data entity.

        Raises:
            ValueError: If the name of the label entity is not 'label'.
        """

        if new_label_data_entity.name != "label":
            raise ValueError("The name of the label entity should be 'label'")

        ml_namespace = self.bottom_level_schemata["ml"].namespace
        concat_task_iri = next(self.exe_kg.subjects(predicate=RDF.type, object=ml_namespace.Concatenation))
        next_to_concat_task_iri = next(
            self.exe_kg.objects(subject=concat_task_iri, predicate=self.top_level_schema.namespace.hasNextTask)
        )

        removal_types = [
            self.top_level_schema.namespace.DataEntity,
            ml_namespace.Concatenation,
            ml_namespace.DataInConcatenation,
            ml_namespace.DataOutConcatenatedData,
        ]

        # remove all instances of DataEntity, Concatenation, DataInConcatenation, and DataOutConcatenatedData
        for removal_type in removal_types:
            for entity_iri in self.exe_kg.subjects(predicate=RDF.type, object=removal_type):
                self.exe_kg.remove((entity_iri, None, None))

        pipeline_iri, input_data_path, _, _ = get_pipeline_and_first_task_iri(
            self.exe_kg, self.top_level_schema.namespace_prefix
        )

        pipeline_entity = Task(pipeline_iri, self.pipeline)

        # update the input data path of the pipeline
        update_pipeline_input_path(
            self.exe_kg,
            pipeline_iri,
            new_dataset_path,
            self.top_level_schema.namespace,
        )

        # or_last_created_task = self.last_created_task
        # or_concat_id = self.task_type_dict["Concatenation"]

        # update serializable pipeline name to avoid errors while creating names for new entities
        self.pipeline_serializable.name = pipeline_entity.name

        # update pipeline construction state to add task in the 1st position of the pipeline
        self.last_created_task = pipeline_entity
        self.task_type_dict["Concatenation"] = 1

        # add a new Concatenation task to the pipeline, which also adds the new feature DataEntities
        concatenate_task = self.add_task(
            kg_schema_short="ml",
            input_entity_dict={"DataInConcatenation": new_feature_data_entities},
            method_type="ConcatenationMethod",
            method_params_dict={},
            task_type="Concatenation",
        )

        # add the new label DataEntity to the pipeline
        add_data_entity_instance(
            self.exe_kg,
            self.data,
            self.top_level_schema.kg,
            self.top_level_schema.namespace,
            new_label_data_entity,
        )

        # link the new Concatenation task to the pipeline
        add_relation(
            self.exe_kg, concatenate_task, self.top_level_schema.namespace.hasNextTask, Entity(next_to_concat_task_iri)
        )

        # # reset construction state
        # self.last_created_task = or_last_created_task
        # self.task_type_dict["Concatenation"] = or_concat_id

    def update_pipeline_name(self, new_name: str):
        """
        Updates every instance of the pipeline name in the ExeKG.

        Args:
            new_name (str): The new name for the pipeline.

        Returns:
            None
        """

        pipeline_iri, _, _, _ = get_pipeline_and_first_task_iri(self.exe_kg, self.top_level_schema.namespace_prefix)

        pipeline_entity = Task(pipeline_iri, self.pipeline)

        old_name = pipeline_entity.name

        # collect triples to update
        triples_to_update = []
        for s, p, o in self.exe_kg:
            new_s, new_o = s, o
            # check and replace in subject URI
            if isinstance(s, URIRef) and old_name in str(s):
                new_s = URIRef(str(s).replace(old_name, new_name))
            # check and replace in object URI if it's a URIRef
            if isinstance(o, URIRef) and old_name in str(o):
                new_o = URIRef(str(o).replace(old_name, new_name))
            if new_s != s or new_o != o:
                triples_to_update.append((s, p, o, new_s, new_o))

        # Update the graph
        for old_s, p, old_o, new_s, new_o in triples_to_update:
            self.exe_kg.remove((old_s, p, old_o))
            self.exe_kg.add((new_s, p, new_o))

        self.pipeline_serializable.name = new_name

        return old_name, new_name

    def apply_changes_to_ttl(self, new_path: str = None, check_executability: bool = True) -> None:
        """
        Applies the changes made to the ExeKG and saves it to a TTL file.

        Args:
            new_path (str, optional): The new path to save the TTL file. If not provided, the input_exe_kg_path will be used. Defaults to None.
            check_executability (bool, optional): Flag indicating whether to check the executability of the saved TTL file. Defaults to True.
        """
        path_to_save = self.input_exe_kg_path if not new_path else new_path
        pipeline_name = os.path.basename(path_to_save).split(".")[0]

        save_exe_kg(
            self.exe_kg,
            self.input_kg,
            self.shacl_shapes_s,
            None,
            os.path.dirname(path_to_save),
            pipeline_name,
            check_executability,
            save_to_ttl=True,
            save_to_json=False,
        )
