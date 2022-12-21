import ast
import re
from typing import Union, Tuple, Optional, Any

from rdflib import URIRef, RDF, Namespace, Literal, Graph, query

# from .visual_tasks import CanvasTask, PlotTask
from .task import Task
from .entity import Entity
from . import visual_tasks, statistic_tasks, ml_tasks
from .data_entity import DataEntity


class ExeKG:
    def __init__(
        self,
        input_kg_namespace_iri: str,
        input_kg_path: str,
        input_kg_namespace_prefix: str,
        top_level_kg_namespace_iri: str,
        top_level_kg_path: str,
        top_level_kg_namespace_prefix: str,
    ):
        self.output_kg = Graph(bind_namespaces="rdflib")
        self.top_level_kg_namespace = Namespace(top_level_kg_namespace_iri)
        self.top_level_kg_namespace_prefix = top_level_kg_namespace_prefix
        self.output_kg.bind(
            self.top_level_kg_namespace_prefix, self.top_level_kg_namespace
        )

        self.input_kg_namespace = Namespace(input_kg_namespace_iri)
        self.input_kg_namespace_prefix = input_kg_namespace_prefix

        self.atomic_task = Entity(self.top_level_kg_namespace.AtomicTask)
        self.atomic_method = Entity(self.top_level_kg_namespace.AtomicMethod)
        self.data_entity = Entity(self.top_level_kg_namespace.DataEntity)
        self.pipeline = Entity(self.top_level_kg_namespace.Pipeline)

        self.task_type_dict = {}
        self.method_type_dict = {}
        self.data_entity_dict = {}
        self.atomic_task_list = []
        self.atomic_method_list = []
        self.data_type_list = []
        self.task_instances_list = []

        self.input_kg = Graph(bind_namespaces="rdflib")
        self.input_kg_path = input_kg_path
        self.parse_input_kg(input_kg_path)

        self.top_level_kg = Graph(bind_namespaces="rdflib")
        self.top_level_kg.parse(top_level_kg_path, format="n3")

    def parse_input_kg(self, path: str) -> None:
        self.input_kg.parse(path, format="n3")

        atomic_task_subclasses = self.get_atomic_task_subclasses()
        for t in list(atomic_task_subclasses):
            task = Entity(t[0], self.atomic_task)
            self.atomic_task_list.append(task)
            self.task_type_dict[task.name] = 1

        atomic_method_subclasses = self.get_atomic_method_subclasses()
        for m in list(atomic_method_subclasses):
            method = Entity(m[0], self.atomic_method)
            self.atomic_method_list.append(method)
            self.method_type_dict[method.name] = 1

        data_entity = Entity(self.top_level_kg_namespace.Data)
        data_type_subclasses = self.get_data_type_subclasses()
        for d in list(data_type_subclasses):
            data_type = Entity(d[0], data_entity)
            self.data_type_list.append(data_type)

    def create_pipeline_task(self, pipeline_name: str) -> Entity:
        pipeline = Entity(
            self.input_kg_namespace + pipeline_name,
            self.pipeline,
        )
        self.add_instance(pipeline)

        prompt = "Enter inputs of the pipeline, enter 'quit' to stop input: "
        input_str = input(prompt)
        while input_str != "quit":
            self.add_data_input_to_instance(
                pipeline, input_str, "Array", "?"
            )  # TODO: make hardcoded values dynamic

            input_str = input(prompt)

        return pipeline

    def create_next_task(self, prompt: str, prev_task: Entity) -> Union[None, Entity]:
        # Next Entity
        print(prompt)
        for i, t in enumerate(self.atomic_task_list):
            print("\t{}. {}".format(str(i), t.name))
        print("\t{}. End pipeline".format(str(-1)))
        next_task_id = int(input())
        if next_task_id == -1:
            return None

        next_task_parent = self.atomic_task_list[next_task_id]
        relation_iri = (
            self.top_level_kg_namespace.hasNextTask
            if prev_task.type != "Pipeline"
            else self.top_level_kg_namespace.hasStartTask
        )
        return self.add_instance_from_parent_with_exe_kg_relation(
            next_task_parent, relation_iri, prev_task
        )

    def create_method(self, task_to_attach_to: Entity) -> None:
        # Entity
        print("Please choose a method for {}:".format(task_to_attach_to.type))

        results = list(self.get_method_properties_and_methods(task_to_attach_to.parent_entity.iri))
        for i, pair in enumerate(results):
            tmp_method = pair[1].split("#")[1]
            print("\t{}. {}".format(str(i), tmp_method))

        method_id = int(input())
        selected_property_and_method = results[method_id]
        method_parent = next(
            filter(
                lambda m: m.iri == selected_property_and_method[1],
                self.atomic_method_list,
            ),
            None,
        )
        self.add_instance_from_parent_with_exe_kg_relation(
            method_parent,
            selected_property_and_method[0],
            task_to_attach_to,
        )

        # data
        # pick data from dataEntityDict, according to allowedDataStructure of methodType

        # DatatypeProperty
        property_list = self.get_data_properties_plus_inherited_by_class_iri(
            method_parent.iri
        )

        if property_list:
            print(
                "Please enter requested properties for {}:".format(method_parent.name)
            )
            for pair in property_list:
                property_instance = URIRef(pair[0])
                range = pair[1].split("#")[1]
                range_instance = URIRef(pair[1])
                input_property = Literal(
                    lexical_or_value=input(
                        "\t{} in range({}): ".format(pair[0].split("#")[1], range)
                    ),
                    datatype=range_instance,
                )
                self.add_literal(task_to_attach_to, property_instance, input_property)

    def start_pipeline_creation(self, pipeline_name: str) -> None:
        pipeline = self.create_pipeline_task(pipeline_name)

        prompt = "Please choose the first Entity:"
        prev_task = pipeline
        while True:
            next_task = self.create_next_task(prompt, prev_task)
            if next_task is None:
                break

            self.create_method(next_task)

            prompt = "Please choose the next Entity:"
            prev_task = next_task

    def save(self, file_path: str) -> None:
        all_kgs = self.input_kg + self.output_kg
        all_kgs.serialize(destination=file_path)

    def query_input_kg(self, q: str, init_bindings: dict = None) -> query.Result:
        return self.input_kg.query(q, initBindings=init_bindings)

    def query_output_kg(self, q: str) -> query.Result:
        return self.output_kg.query(q)

    def get_data_properties_plus_inherited_by_class_iri(self, class_iri: str):
        property_list = list(self.get_data_properties_by_entity_iri(class_iri))
        method_parent_classes = list(self.query_method_parent_classes(class_iri))
        for method_class_result_row in method_parent_classes:
            property_list += list(
                self.get_data_properties_by_entity_iri(method_class_result_row[0])
            )

        return property_list

    def get_data_properties_by_entity_iri(self, entity_iri: str) -> query.Result:
        return self.query_input_kg(
            "\nSELECT ?p ?r WHERE {?p rdfs:domain ?entity_iri . "
            "?p rdfs:range ?r . "
            "?p rdf:type owl:DatatypeProperty . }",
            init_bindings={"entity_iri": URIRef(entity_iri)},
        )

    def get_method_properties_and_methods(self, entity_parent_iri: str) -> query.Result:
        return self.query_input_kg(
            "\nSELECT ?p ?m WHERE {?p rdfs:domain ?entity_parent_iri . "
            "?p rdfs:range ?m . "
            "?m rdfs:subClassOf "
            + self.top_level_kg_namespace_prefix
            + ":AtomicMethod . }",
            init_bindings={"entity_iri": URIRef(entity_parent_iri)},
        )  # method property

    def get_atomic_method_subclasses(self) -> query.Result:
        return self.query_input_kg(
            "\nSELECT ?t WHERE {?t rdfs:subClassOf "
            + self.top_level_kg_namespace_prefix
            + ":AtomicMethod . }"
        )

    def get_atomic_task_subclasses(self) -> query.Result:
        return self.query_input_kg(
            "\nSELECT ?t WHERE {?t rdfs:subClassOf "
            + self.top_level_kg_namespace_prefix
            + ":AtomicTask . }"
        )

    def get_data_type_subclasses(self) -> query.Result:
        return self.query_input_kg(
            "\nSELECT ?t WHERE {?t rdfs:subClassOf "
            + self.top_level_kg_namespace_prefix
            + ":Data . }"
        )

    def add_data_input_to_instance(
        self,
        instance: Entity,
        data_instance_name: str,
        data_structure: str,
        data_semantics: str,
    ) -> None:
        data_instance = Entity(
            self.input_kg_namespace + data_instance_name, self.data_entity
        )
        self.add_instance(data_instance)

        data_structrure_instance = Entity(self.top_level_kg_namespace + data_structure)
        self.add_exe_kg_relation(
            data_instance,
            self.top_level_kg_namespace.hasDataStructure,
            data_structrure_instance,
        )

        data_semantics_instance = Entity(self.top_level_kg_namespace + data_semantics)
        self.add_exe_kg_relation(
            data_instance,
            self.top_level_kg_namespace.hasDataSemantics,
            data_semantics_instance,
        )

        self.add_exe_kg_relation(
            instance, self.top_level_kg_namespace.hasInput, data_instance
        )

    def add_instance_from_parent_with_exe_kg_relation(
        self, instance_parent: Entity, relation_iri: str, related_entity: Entity
    ) -> Entity:
        instance_name = self.name_instance(instance_parent)
        instance_iri = self.input_kg_namespace + instance_name
        instance = Entity(instance_iri, instance_parent)
        self.add_instance(instance)
        self.add_exe_kg_relation(related_entity, relation_iri, instance)

        return instance

    def add_instance(self, entity_instance: Entity) -> None:
        if (
            entity_instance.parent_entity
            and (entity_instance.iri, None, None) not in self.output_kg
        ):
            self.output_kg.add(
                (entity_instance.iri, RDF.type, entity_instance.parent_entity.iri)
            )

    def add_exe_kg_relation(
        self, from_entity: Entity, relation_iri: str, to_entity: Entity
    ) -> None:
        self.output_kg.add(
            (
                from_entity.iri,
                URIRef(relation_iri),
                to_entity.iri,
            )
        )

    def add_literal(self, from_entity: Entity, relation: str, literal: Literal) -> None:
        self.output_kg.add((from_entity.iri, relation, literal))

    def name_instance(self, parent_entity: Entity) -> Union[None, str]:
        if parent_entity.type == "AtomicTask":
            entity_type_dict = self.task_type_dict
        elif parent_entity.type == "AtomicMethod":
            entity_type_dict = self.method_type_dict
        else:
            print("Error: Invalid parent entity type")
            return None

        instance_name = parent_entity.name + str(entity_type_dict[parent_entity.name])
        entity_type_dict[parent_entity.name] += 1
        return instance_name

    @staticmethod
    def camel_to_snake(name: str) -> str:
        name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()

    def property_name_to_field_name(self, property_name: str) -> str:
        return self.camel_to_snake(property_name.split("#")[1])

    def property_value_to_field_value(
        self, property_value: str
    ) -> Union[str, DataEntity]:
        if "#" in property_value:
            data_entity = self.parse_data_entity_by_iri(property_value)
            if data_entity is None:
                return property_value
            return data_entity

        return property_value

    def get_method_by_task_iri(self, task_iri: str) -> Optional[Entity]:
        method_iri = self.get_first_query_result_if_exists(
            self.query_method_iri_by_task_iri, task_iri
        )
        method_parent_iri = self.get_first_query_result_if_exists(
            self.query_entity_parent_iri, method_iri, self.top_level_kg_namespace.Method
        )
        if method_parent_iri is None:
            return None

        return Entity(method_iri, Entity(method_parent_iri))

    def get_pipeline_and_first_task_iri(self) -> Tuple[str, str]:
        # assume one pipeline per file
        pipeline_iri, task_iri = list(
            self.query_input_kg(
                f"\nSELECT ?p ?t WHERE {{?p rdf:type {self.top_level_kg_namespace_prefix}:Pipeline ;"
                f"                       {self.top_level_kg_namespace_prefix}:hasStartTask ?t . }}"
            )
        )[0]

        return str(pipeline_iri), str(task_iri)

    def query_method_parent_classes(self, method_iri):
        return self.query_input_kg(
            f"SELECT ?c WHERE {{ ?method rdfs:subClassOf ?c . }}",
            init_bindings={"method": URIRef(method_iri)},
        )

    def query_entity_parent_iri(self, entity_iri: str, upper_class_uri_ref: URIRef):
        return self.query_input_kg(
            f"SELECT ?t WHERE {{ ?entity rdf:type ?t ."
            f"                   ?t rdfs:subClassOf* ?upper_class .}}",
            init_bindings={
                "entity": URIRef(entity_iri),
                "upper_class": upper_class_uri_ref,
            },
        )

    def query_method_iri_by_task_iri(self, task_iri: str):
        return self.query_input_kg(
            f"SELECT ?m WHERE {{ ?task ?m_property ?m ."
            f"                   ?m_property rdfs:subPropertyOf* {self.top_level_kg_namespace_prefix}:hasMethod .}}",
            init_bindings={"task": URIRef(task_iri)},
        )

    @staticmethod
    def get_first_query_result_if_exists(query_method, *args) -> Optional[str]:
        query_result = next(
            iter(list(query_method(*args))),
            None,
        )

        if query_result is None:
            return None

        return str(query_result[0])

    # def get_task_method_iri_if_exists(self, task_iri: str) -> Optional[str]:
    #     method_query_result = next(
    #         iter(list(self.query_method_iri_by_task_iri(task_iri))),
    #         None,
    #     )
    #
    #     if method_query_result is None:
    #         return None
    #
    #     return str(method_query_result[0])

    def parse_data_entity_by_iri(self, data_entity_iri: str) -> Optional[DataEntity]:
        data_entity_parent_iri = self.get_first_query_result_if_exists(
            self.query_entity_parent_iri,
            data_entity_iri,
            self.top_level_kg_namespace.DataEntity,
        )
        if data_entity_parent_iri is None:
            return None

        data_entity = DataEntity(data_entity_iri, Entity(data_entity_parent_iri))

        for s, p, o in self.input_kg.triples((URIRef(data_entity_iri), None, None)):
            field_name = self.property_name_to_field_name(str(p))
            if not hasattr(data_entity, field_name) or field_name == "type":
                continue
            field_value = self.property_value_to_field_value(str(o))
            setattr(data_entity, field_name, field_value)

        return data_entity

    def parse_task_by_iri(
        self, task_iri: str, canvas_method: visual_tasks.CanvasTaskCanvasMethod = None
    ) -> Optional[Task]:
        task_parent_iri = self.get_first_query_result_if_exists(
            self.query_entity_parent_iri, task_iri, self.top_level_kg_namespace.Task
        )

        task = Task(task_iri, Task(task_parent_iri))
        method = self.get_method_by_task_iri(task_iri)
        if method is None:
            print(f"Cannot retrieve method for task with iri: {task_iri}")

        class_name = task.type + method.type
        Class = getattr(visual_tasks, class_name, None)
        if Class is None:
            Class = getattr(statistic_tasks, class_name, None)
        if Class is None:
            Class = getattr(ml_tasks, class_name, None)

        if canvas_method:
            task = Class(task_iri, Task(task_parent_iri), canvas_method)
        else:
            task = Class(task_iri, Task(task_parent_iri))

        for s, p, o in self.input_kg.triples((URIRef(task_iri), None, None)):
            field_name = self.property_name_to_field_name(str(p))
            if not hasattr(task, field_name) or field_name == "type":
                continue
            field_value = self.property_value_to_field_value(str(o))
            print(field_name, field_value)
            if field_name == "has_input" or field_name == "has_output":
                getattr(task, field_name).append(field_value)
            else:
                setattr(task, field_name, field_value)

        return task
