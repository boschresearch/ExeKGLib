# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from glob import glob
from typing import Dict

from rdflib import Graph, Namespace


class KGSchema:
    """
    Stores a Graph object and some metadata corresponding to a KG schema
    """

    def __init__(self, path: str, generated_schemata_dir: str, namespace: str, namespace_prefix: str):
        self.path = path  # path of the KG schema definition, can be local or remote
        self.generated_schemata_dir = (
            generated_schemata_dir  # path of generated KG schemata definitions, can be local or remote
        )
        self.namespace = Namespace(namespace)
        self.namespace_prefix = namespace_prefix

        self.kg = Graph(bind_namespaces="rdflib")
        self.kg.parse(self.path, format="n3")

        self.generated_kgs = []
        for gen_schema_path in glob(f"{self.generated_schemata_dir}/*.ttl"):
            gen_kg = Graph(bind_namespaces="rdflib")
            gen_kg.parse(gen_schema_path, format="n3")
            self.generated_kgs.append(gen_kg)

    @classmethod
    def from_schema_info(cls, schema_info: Dict[str, str]):
        return cls(
            schema_info["path"],
            schema_info["generated_schemata_dir"],
            schema_info["namespace"],
            schema_info["namespace_prefix"],
        )
