# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from .entity import Entity


class DataEntity(Entity):
    """
    Abstraction of owl:class ds:DataEntity.

    ❗ Important for contributors: See Section "Naming conventions" in README.md of "classes.tasks" package before extending the code's functionality.
    """

    def __init__(
        self,
        iri: str,
        parent_entity: Entity,
        source_value: str = None,
        data_semantics_iri: str = None,
        data_structure_iri: str = None,
        reference: str = None,
    ):
        super().__init__(iri, parent_entity)
        self.source = source_value  # used as column name to retrieve data from the pipeline's input file
        self.data_semantics = data_semantics_iri  # IRI of KG entity of type DataSemantics
        self.data_structure = data_structure_iri  # IRI of KG entity of type DataStructure
        self.reference = reference  # reference to another data entity in the KG, expecting an IRI
