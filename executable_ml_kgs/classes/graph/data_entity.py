from .entity import Entity


class DataEntity(Entity):
    def __init__(
            self,
            iri: str,
            parent_entity: Entity,
            has_source: str = None,
            has_data_semantics: Entity = None,
            has_data_structure: Entity = None,
    ):
        super().__init__(iri, parent_entity)
        self.has_source = has_source
        self.has_data_semantics = has_data_semantics

        self.has_data_structure = has_data_structure
