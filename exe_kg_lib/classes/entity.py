# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from __future__ import annotations

from rdflib import URIRef


class Entity:
    """
    Abstraction of a KG entity with basic RDF properties plus its parent_entity (connected in KG with rdf:type).
    """

    def __init__(self, iri: str, parent_entity: Entity = None):
        self.iri = URIRef(iri)
        self.parent_entity = parent_entity
        self.namespace = self.get_namespace(iri)
        self.name = self.type = self.get_descriptor(iri)
        if parent_entity:
            self.type = parent_entity.name

    @staticmethod
    def get_namespace(iri: str) -> str:
        return iri.split("#")[0] + "#"

    @staticmethod
    def get_descriptor(iri: str) -> str:
        return iri.split("#")[1]
