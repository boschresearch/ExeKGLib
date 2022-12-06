from rdflib import URIRef


class Entity:
    def __init__(self, iri, parent_entity=None):
        self.iri = URIRef(iri)
        self.parent_entity = parent_entity
        self.namespace = self.get_namespace(iri)
        self.name = self.type = self.get_descriptor(iri)
        if parent_entity:
            self.type = self.get_descriptor(parent_entity.iri)

    @staticmethod
    def get_namespace(iri):
        return iri.split("#")[0]

    @staticmethod
    def get_descriptor(iri):
        return iri.split("#")[1]
