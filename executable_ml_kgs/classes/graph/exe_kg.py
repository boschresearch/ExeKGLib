import ast
import re
from typing import Union, Tuple, Optional, Any, Callable, List

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
        self.data = Entity(self.top_level_kg_namespace.Data)
        self.data_semantics = Entity(self.top_level_kg_namespace.DataSemantics)
        self.data_structure = Entity(self.top_level_kg_namespace.DataStructure)

        self.task_type_dict = {}
        self.method_type_dict = {}
        self.atomic_task_list = []
        self.atomic_method_list = []
        self.data_type_list = []
        self.data_semantics_list = []
        self.data_structure_list = []

        self.top_level_kg = Graph(bind_namespaces="rdflib")
        self.top_level_kg.parse(top_level_kg_path, format="n3")

        self.input_kg = Graph(bind_namespaces="rdflib")
        self.input_kg.parse(input_kg_path, format="n3")

        self.parse_kgs()

    def parse_kgs(self) -> None:
        atomic_task_subclasses = self.get_subclasses_of(
            self.atomic_task.iri, self.input_kg
        )
        for t in list(atomic_task_subclasses):
            task = Entity(t[0], self.atomic_task)
            self.atomic_task_list.append(task)
            self.task_type_dict[task.name] = 1

        atomic_method_subclasses = self.get_subclasses_of(
            self.atomic_method.iri, self.input_kg
        )
        for m in list(atomic_method_subclasses):
            method = Entity(m[0], self.atomic_method)
            self.atomic_method_list.append(method)
            self.method_type_dict[method.name] = 1

        data_type_subclasses = self.get_subclasses_of(
            self.data_entity.iri, self.input_kg
        )
        for d in list(data_type_subclasses):
            data_type = Entity(d[0], self.data_entity)
            self.data_type_list.append(data_type)

        data_semantics_subclasses = self.get_subclasses_of(
            self.data_semantics.iri, self.top_level_kg
        )
        for d in list(data_semantics_subclasses):
            if d[0] == self.data_entity.iri:
                continue
            data_semantics = Entity(d[0], self.data_semantics)
            self.data_semantics_list.append(data_semantics)

        data_structure_subclasses = self.get_subclasses_of(
            self.data_structure.iri, self.top_level_kg
        )
        for d in list(data_structure_subclasses):
            if d[0] == self.data_entity.iri:
                continue
            data_structure = Entity(d[0], self.data_structure)
            self.data_structure_list.append(data_structure)

    def create_pipeline_entity(self, name: str):
        return Task(
            self.input_kg_namespace + name,
            self.pipeline,
        )

    @staticmethod
    def get_input_for_existing_data_entities(existing_data_entity_list: List[DataEntity]) -> Union[
        None, List[DataEntity]]:
        chosen_data_entity_list = []
        print("Select input for the task from existing data entities:")
        while True:
            for i, data_entity in enumerate(existing_data_entity_list):
                print("\t{}. {}".format(str(i), data_entity.name))
            print("\t{}. Continue to choose new input columns".format(str(-1)))
            chosen_data_entity_i = int(input())
            if chosen_data_entity_i == -1:
                break

            chosen_data_entity_list.append(existing_data_entity_list[chosen_data_entity_i])

        return chosen_data_entity_list

    def get_input_for_new_data_entities(self) -> Tuple[list, list, list]:
        source_list = []
        data_semantics_list = []
        data_structure_list = []

        prompt = "Enter input columns for the task, enter 'quit' to stop input: "
        source = input(prompt)
        while source != "quit":
            source_list.append(source)

            print(f"Choose data semantics for {source}:")
            for i, t in enumerate(self.data_semantics_list):
                print("\t{}. {}".format(str(i), t.name))
            chosen_data_semantics_id = int(input())
            data_semantics_list.append(self.data_semantics_list[chosen_data_semantics_id])

            print(f"Choose data structure for {source}:")
            for i, t in enumerate(self.data_structure_list):
                print("\t{}. {}".format(str(i), t.name))
            chosen_data_structure_id = int(input())
            data_structure_list.append(self.data_structure_list[chosen_data_structure_id])

            source = input(prompt)

        return source_list, data_semantics_list, data_structure_list

    def add_input_data_entity(self, data_entity: DataEntity, task_entity: Task) -> None:
        self.add_exe_kg_data_entity(data_entity)
        self.add_exe_kg_relation(
            task_entity, self.top_level_kg_namespace.hasInput, data_entity
        )

        task_entity.has_input.append(data_entity)

    def create_pipeline_task(self, pipeline_name: str) -> Task:
        pipeline = self.create_pipeline_entity(pipeline_name)
        self.add_instance(pipeline)

        source_list, data_semantics_list, data_structure_list = self.get_input_for_new_data_entities()

        for source, data_semantics, data_structure in zip(source_list, data_semantics_list, data_structure_list):
            data_entity = DataEntity(
                self.input_kg_namespace + source,
                self.data_entity,
                source,
                data_semantics,
                data_structure,
            )
            self.add_input_data_entity(data_entity, pipeline)

        return pipeline

    def create_next_task(self, prompt: str, prev_task: Task, existing_data_entity_list: List[DataEntity]) -> Union[
        None, Task]:
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
        task_entity = self.add_instance_from_parent_with_exe_kg_relation(
            next_task_parent, relation_iri, prev_task
        )

        task_entity = Task(task_entity.iri, task_entity.parent_entity)

        if prev_task.type == "Pipeline":
            for data_entity in prev_task.has_input:
                self.add_exe_kg_relation(
                    task_entity, self.top_level_kg_namespace.hasInput, data_entity
                )
                task_entity.has_input.append(data_entity)
        else:  # ask user
            chosen_data_entity_list = self.get_input_for_existing_data_entities(existing_data_entity_list)
            for chosen_data_entity in chosen_data_entity_list:
                self.add_input_data_entity(chosen_data_entity, task_entity)

            source_list, data_semantics_list, data_structure_list = self.get_input_for_new_data_entities()

            for source, data_semantics, data_structure in zip(source_list, data_semantics_list, data_structure_list):
                data_entity = DataEntity(
                    self.input_kg_namespace + source,
                    self.data_entity,
                    source,
                    data_semantics,
                    data_structure,
                )
                self.add_input_data_entity(data_entity, task_entity)
                existing_data_entity_list.append(data_entity)

        print("Enter names for the output values of the task, enter 'quit' to stop input:")
        output_name = input()
        while output_name != "quit":
            data_entity = DataEntity(self.input_kg_namespace + output_name, self.data_entity)
            self.add_instance(data_entity)
            self.add_exe_kg_relation(task_entity, self.top_level_kg_namespace.hasOutput, data_entity)
            task_entity.has_output.append(data_entity)

            existing_data_entity_list.append(data_entity)
            output_name = input()

        return task_entity

    def create_method(self, task_to_attach_to: Entity) -> None:
        # Entity
        print("Please choose a method for {}:".format(task_to_attach_to.type))

        results = list(
            self.get_method_properties_and_methods(task_to_attach_to.parent_entity.iri)
        )
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
                range_iri = pair[1]
                input_property = Literal(
                    lexical_or_value=input(
                        "\t{} in range({}): ".format(pair[0].split("#")[1], range)
                    ),
                    datatype=range_iri,
                )
                self.add_exe_kg_literal(
                    task_to_attach_to, property_instance, input_property
                )

    def start_pipeline_creation(self, pipeline_name: str) -> None:
        pipeline = self.create_pipeline_task(pipeline_name)

        prompt = "Please choose the first Task:"
        prev_task = pipeline
        data_entities_list = pipeline.has_input
        while True:
            next_task = self.create_next_task(prompt, prev_task, data_entities_list)
            if next_task is None:
                break

            self.create_method(next_task)

            prev_task = next_task

    def save(self, file_path: str) -> None:
        all_kgs = self.input_kg + self.output_kg
        all_kgs.serialize(destination=file_path)

    def query_input_kg(self, q: str, init_bindings: dict = None) -> query.Result:
        return self.input_kg.query(q, initBindings=init_bindings)

    def query_output_kg(self, q: str) -> query.Result:
        return self.output_kg.query(q)

    def query_top_level_kg(self, q: str, init_bindings: dict = None) -> query.Result:
        return self.top_level_kg.query(q, initBindings=init_bindings)

    def get_data_properties_plus_inherited_by_class_iri(self, class_iri: str):
        property_list = list(
            self.get_data_properties_by_entity_iri(class_iri, self.input_kg)
        )
        method_parent_classes = list(self.query_method_parent_classes(class_iri))
        for method_class_result_row in method_parent_classes:
            property_list += list(
                self.get_data_properties_by_entity_iri(
                    method_class_result_row[0], self.input_kg
                )
            )

        return property_list

    @staticmethod
    def get_data_properties_by_entity_iri(entity_iri: str, kg: Graph) -> query.Result:
        return kg.query(
            "\nSELECT ?p ?r WHERE {?p rdfs:domain ?entity_iri . "
            "?p rdfs:range ?r . "
            "?p rdf:type owl:DatatypeProperty . }",
            initBindings={"entity_iri": URIRef(entity_iri)},
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

    @staticmethod
    def get_subclasses_of(class_iri: str, kg: Graph) -> query.Result:
        return kg.query(
            "\nSELECT ?t WHERE {?t rdfs:subClassOf ?class_iri . }",
            initBindings={"class_iri": class_iri},
        )

    # def get_atomic_method_subclasses(self) -> query.Result:
    #     return self.query_input_kg(
    #         "\nSELECT ?t WHERE {?t rdfs:subClassOf "
    #         + self.top_level_kg_namespace_prefix
    #         + ":AtomicMethod . }"
    #     )
    #
    # def get_atomic_task_subclasses(self) -> query.Result:
    #     return self.query_input_kg(
    #         "\nSELECT ?t WHERE {?t rdfs:subClassOf "
    #         + self.top_level_kg_namespace_prefix
    #         + ":AtomicTask . }"
    #     )
    #
    # def get_data_type_subclasses(self) -> query.Result:
    #     return self.query_input_kg(
    #         "\nSELECT ?t WHERE {?t rdfs:subClassOf "
    #         + self.top_level_kg_namespace_prefix
    #         + ":Data . }"
    #     )

    def add_exe_kg_data_entity(self, data_entity: DataEntity) -> None:
        self.add_instance(data_entity)

        has_source_iri, range_iri = self.get_first_query_result_if_exists(
            self.get_data_properties_by_entity_iri, self.data.iri, self.top_level_kg
        )

        source_literal = Literal(
            lexical_or_value=data_entity.has_source,
            datatype=range_iri,
        )

        self.add_exe_kg_literal(data_entity, has_source_iri, source_literal)

        self.add_exe_kg_relation(
            data_entity,
            self.top_level_kg_namespace.hasDataStructure,
            data_entity.has_data_structure,
        )

        self.add_exe_kg_relation(
            data_entity,
            self.top_level_kg_namespace.hasDataSemantics,
            data_entity.has_data_semantics,
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

    def add_exe_kg_literal(
            self, from_entity: Entity, relation_iri: str, literal: Literal
    ) -> None:
        self.output_kg.add((from_entity.iri, URIRef(relation_iri), literal))

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
        method_iri = str(
            self.get_first_query_result_if_exists(
                self.query_method_iri_by_task_iri, task_iri
            )[0]
        )
        method_parent_iri = str(
            self.get_first_query_result_if_exists(
                self.query_entity_parent_iri,
                method_iri,
                self.top_level_kg_namespace.Method,
            )[0]
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

        return query_result

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
        data_entity_parent_iri = str(
            self.get_first_query_result_if_exists(
                self.query_entity_parent_iri,
                data_entity_iri,
                self.top_level_kg_namespace.DataEntity,
            )[0]
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
        task_parent_iri = str(
            self.get_first_query_result_if_exists(
                self.query_entity_parent_iri, task_iri, self.top_level_kg_namespace.Task
            )[0]
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
