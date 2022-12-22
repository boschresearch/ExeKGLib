from .entity import Entity


class DataEntity(Entity):
    def __init__(
            self,
            iri: str,
            parent_entity: Entity,
            has_source_value: str = None,
            has_data_semantics_iri: str = None,
            has_data_structure_iri: str = None,
    ):
        super().__init__(iri, parent_entity)
        self.has_source = has_source_value
        self.has_data_semantics = has_data_semantics_iri
        self.has_data_structure = has_data_structure_iri
