# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from typing import List

from rdflib import Graph

from exe_kg_lib.classes.exe_kg_serialization.pipeline import Pipeline
from exe_kg_lib.config import KG_SCHEMAS

from ..utils.query_utils import query_subclasses_of
from .entity import Entity
from .kg_schema import KGSchema


class ExeKGBase:
    def __init__(self):
        """

        Args:
            input_exe_kg_path: path of KG to be executed
                               acts as switch for KG execution mode (if filled, mode is on)
        """
        self.top_level_schema = KGSchema.from_schema_info(KG_SCHEMAS["Data Science"])  # top-level KG schema
        self.bottom_level_schemata = {}
        for schema_name, schema_info in KG_SCHEMAS.items():  # search for used bottom-level schema
            if (
                schema_name == "Data Science"  # or schema_name == "Visualization"
            ):  # skip top-level KG schema and Visualization schema that is always used
                continue

            self.bottom_level_schemata[schema_info["namespace_prefix"]] = KGSchema.from_schema_info(schema_info)

        # top-level KG schema entities
        self.atomic_task = Entity(self.top_level_schema.namespace.AtomicTask)
        self.task = Entity(self.top_level_schema.namespace.Task)
        self.atomic_method = Entity(self.top_level_schema.namespace.AtomicMethod)
        self.data_entity = Entity(self.top_level_schema.namespace.DataEntity)
        self.pipeline = Entity(self.top_level_schema.namespace.Pipeline)
        self.data = Entity(self.top_level_schema.namespace.Data)
        self.data_semantics = Entity(self.top_level_schema.namespace.DataSemantics)
        self.data_structure = Entity(self.top_level_schema.namespace.DataStructure)

        # self.input_kg: KG eventually filled with 3 KG schemas and the input executable KG in case of KG execution
        self.input_kg = Graph(bind_namespaces="rdflib")

        # self.shacl_shapes_s: string containing SHACL shapes of all KG schemas
        self.shacl_shapes_s = self.top_level_schema.shacl_shapes_s

        # bottom_level_schemata_kgs = [kg_schema.kg for kg_schema in self.bottom_level_schemata.values()]
        bottom_level_schemata_kgs = []
        for kg_schema in self.bottom_level_schemata.values():
            bottom_level_schemata_kgs.append(kg_schema.kg)
            bottom_level_schemata_kgs.append(kg_schema.generated_schema_kg)
            self.shacl_shapes_s += kg_schema.shacl_shapes_s

        self.input_kg += self.top_level_schema.kg  # + self.visu_schema.kg  # combine all KG schemas in input KG

        for bottom_level_schema_kg in bottom_level_schemata_kgs:
            self.input_kg += bottom_level_schema_kg

        self.exe_kg = Graph(bind_namespaces="rdflib")  # variable to store the constructed ExeKG
        self.pipeline_instance = None  # variable to store pipeline's metadata
        self.pipeline_serializable = Pipeline()  # simplified version of pipeline for serialization purposes

        self._bind_used_namespaces([self.input_kg, self.exe_kg])

        # below variables are filled in self._parse_kgs()
        self.task_type_dict = {}  # dict for uniquely naming each new pipeline task
        self.method_type_dict = {}  # dict for uniquely naming each new pipeline method
        self.atomic_task_list = []  # list for storing the available sub-classes of ds:AtomicTask
        self.atomic_method_list = []  # list for storing the available sub-classes of ds:AtomicMethod
        self.data_type_list = []  # list for storing the available sub-classes of ds:DataEntity
        self.data_semantics_list = []  # list for storing the available sub-classes of ds:DataSemantics
        self.data_structure_list = []  # list for storing the available sub-classes of ds:DataStructure

        self.existing_data_entity_list = (
            []
        )  # contains existing data entities that are output entities of previous tasks during KG construction
        self.last_created_task = (
            None  # last created pipeline task, for connecting consecutive pipeline tasks during KG construction
        )
        self.canvas_task_created = False  # indicates if canvas task was created during KG construction, and used for hiding the other Visualization tasks in CLI

        self._parse_kgs()

    def _bind_used_namespaces(self, kgs: List[Graph]):
        """
        Binds top-level and bottom-level KG schemas' namespaces with their prefixes
        Adds these bindings to the Graphs of kgs list

        Args:
            kgs: list of Graph objects to which the namespace bindings are added
        """
        for kg in kgs:
            kg.bind(self.top_level_schema.namespace_prefix, self.top_level_schema.namespace)
            for bottom_level_kg_schema in self.bottom_level_schemata.values():
                kg.bind(
                    bottom_level_kg_schema.namespace_prefix,
                    bottom_level_kg_schema.namespace,
                )

    def _parse_kgs(self) -> None:
        """
        Fills lists with subclasses of top-level KG schema classes and initializes dicts used for unique naming
        """
        atomic_task_subclasses = query_subclasses_of(self.atomic_task.iri, self.input_kg)
        for t in list(atomic_task_subclasses):
            task = Entity(t[0], self.atomic_task)
            self.atomic_task_list.append(task)
            self.task_type_dict[task.name] = 1

        atomic_method_subclasses = query_subclasses_of(self.atomic_method.iri, self.input_kg)
        for m in list(atomic_method_subclasses):
            method = Entity(m[0], self.atomic_method)
            self.atomic_method_list.append(method)
            self.method_type_dict[method.name] = 1

        data_type_subclasses = query_subclasses_of(self.data_entity.iri, self.input_kg)
        for d in list(data_type_subclasses):
            data_type = Entity(d[0], self.data_entity)
            self.data_type_list.append(data_type)

        data_semantics_subclasses = query_subclasses_of(self.data_semantics.iri, self.top_level_schema.kg)
        for d in list(data_semantics_subclasses):
            if d[0] == self.data_entity.iri:
                continue
            data_semantics = Entity(d[0], self.data_semantics)
            self.data_semantics_list.append(data_semantics)

        data_structure_subclasses = query_subclasses_of(self.data_structure.iri, self.top_level_schema.kg)
        for d in list(data_structure_subclasses):
            if d[0] == self.data_entity.iri:
                continue
            data_structure = Entity(d[0], self.data_structure)
            self.data_structure_list.append(data_structure)
