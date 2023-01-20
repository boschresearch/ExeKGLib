# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from .entity import Entity


class DataEntity(Entity):
    """
    Abstraction of owl:class DataEntity.

    ❗ Important for contributors ❗
    The fields that contain "_" are by convention the snake-case conversions of the equivalent camel-case property names in the KG.
    e.g. has_source field corresponds to hasSource property in the KG.
    This is necessary for automatically mapping KG properties to Python object fields while parsing the KG.
    """

    def __init__(
        self,
        iri: str,
        parent_entity: Entity,
        has_source_value: str = None,
        has_data_semantics_iri: str = None,
        has_data_structure_iri: str = None,
        has_reference: str = None,
    ):
        super().__init__(iri, parent_entity)
        self.has_source = has_source_value  # used as column name to retrieve data from the pipeline's input file
        self.has_data_semantics = has_data_semantics_iri  # IRI of KG entity of type DataSemantics
        self.has_data_structure = has_data_structure_iri  # IRI of KG entity of type DataStructure
        self.has_reference = has_reference  # reference to another data entity in the KG, expecting an IRI
