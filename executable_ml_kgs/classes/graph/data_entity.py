from .entity import Entity


class DataEntity(Entity):
    def __init__(self, iri: str, parent_entity: Entity):
        super().__init__(iri, parent_entity)
        self.has_source = None
