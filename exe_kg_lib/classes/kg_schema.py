from typing import Dict

from rdflib import Namespace, Graph


class KGSchema:
    def __init__(self, path: str, namespace: str, namespace_prefix: str):
        self.path = path
        self.namespace = Namespace(namespace)
        self.namespace_prefix = namespace_prefix

        self.kg = Graph(bind_namespaces="rdflib")
        self.kg.parse(self.path, format="n3")

    @classmethod
    def from_schema_info(cls, schema_info: Dict[str, str]):
        return cls(schema_info["path"], schema_info["namespace"], schema_info["namespace_prefix"])
