# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from typing import Dict

import requests
from rdflib import Graph, Namespace


class KGSchema:
    """
    Stores a Graph object and some metadata corresponding to a KG schema
    """

    def __init__(
        self,
        path: str,
        shacl_shapes_path: str,
        generated_schema_path: str,
        generated_shacl_shapes_path: str,
        namespace: str,
        namespace_prefix: str,
    ):
        self.path = path  # path of the main KG schema definition, can be local or remote
        self.generated_schema_path = (
            generated_schema_path  # path of file containing generated schema for this schema, can be local or remote
        )
        self.namespace = Namespace(namespace)
        self.namespace_prefix = namespace_prefix

        self.kg = Graph(bind_namespaces="rdflib")
        self.kg.parse(self.path, format="n3")

        self.generated_schema_kg = Graph(bind_namespaces="rdflib")
        if self.generated_schema_path:
            self.generated_schema_kg.parse(self.generated_schema_path, format="n3")

        # shacl
        self.shacl_shapes_path = shacl_shapes_path  # path of file containing main shacl shapes, can be local or remote
        self.generated_shacl_shapes_path = (
            generated_shacl_shapes_path  # path of file containing generated shacl shapes, can be local or remote
        )

        self.shacl_shapes_s = self.read_shacl_shapes(self.shacl_shapes_path)  # shacl shapes are stored as string

        if self.generated_shacl_shapes_path:
            self.shacl_shapes_s += self.read_shacl_shapes(self.generated_shacl_shapes_path)

    @classmethod
    def from_schema_info(cls, schema_info: Dict[str, str]):
        return cls(
            schema_info["path"],
            schema_info["shacl_shapes_path"],
            schema_info["generated_schema_path"],
            schema_info["generated_shacl_shapes_path"],
            schema_info["namespace"],
            schema_info["namespace_prefix"],
        )

    @staticmethod
    def read_shacl_shapes(path: str):
        if path.startswith("http"):
            return requests.get(path).text
        else:
            with open(path) as f:
                return f.read()
