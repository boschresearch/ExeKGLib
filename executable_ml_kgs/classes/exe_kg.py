from typing import Union, Tuple, List

from rdflib import RDF, Namespace, Literal

from utils.cli_utils import (
    get_input_for_existing_data_entities,
    get_input_for_new_data_entities,
)
from utils.query_utils import *
from utils.string_utils import property_name_to_field_name
from .data_entity import DataEntity
from .entity import Entity
from .task import Task
from .tasks import visual_tasks, statistic_tasks, ml_tasks

KG_SCHEMAS = {
    "Data Science": (
        "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/ds_exeKGOntology.ttl",  # path
        "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/ds_exeKGOntology.ttl#",  # namespace
        "ds",  # namespace prefix
    ),
    "Visual": (
        "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/visu_exeKGOntology.ttl",
        "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/visu_exeKGOntology.ttl#",
        "visu",
    ),
    "Statistics": (
        "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/stats_exeKGOntology.ttl",
        "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/stats_exeKGOntology.ttl#",
        "stats",
    ),
    "Machine Learning": (
        "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/ml_exeKGOntology.ttl",
        "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/ml_exeKGOntology.ttl#",
        "ml",
    ),
}


class ExeKG:
    def __init__(self, kg_schema_name: str = None, input_exe_kg_path: str = None):
        top_level_schema_info = KG_SCHEMAS["Data Science"]
        top_level_schema_path = top_level_schema_info[0]
        top_level_schema_namespace = top_level_schema_info[1]
        top_level_schema_namespace_prefix = top_level_schema_info[2]

        self.top_level_schema_namespace = Namespace(top_level_schema_namespace)
        self.top_level_schema_namespace_prefix = top_level_schema_namespace_prefix

        self.atomic_task = Entity(self.top_level_schema_namespace.AtomicTask)
        self.atomic_method = Entity(self.top_level_schema_namespace.AtomicMethod)
        self.data_entity = Entity(self.top_level_schema_namespace.DataEntity)
        self.pipeline = Entity(self.top_level_schema_namespace.Pipeline)
        self.data = Entity(self.top_level_schema_namespace.Data)
        self.data_semantics = Entity(self.top_level_schema_namespace.DataSemantics)
        self.data_structure = Entity(self.top_level_schema_namespace.DataStructure)

        self.top_level_kg = Graph(bind_namespaces="rdflib")
        self.top_level_kg.parse(top_level_schema_path, format="n3")

        self.input_kg = Graph(bind_namespaces="rdflib")
        if input_exe_kg_path:
            self.input_kg.parse(input_exe_kg_path, format="n3")
            all_ns = [n for n in self.input_kg.namespace_manager.namespaces()]
            schema_info_set = False
            for schema_name, schema_info in KG_SCHEMAS.items():
                if schema_name == "Data Science":
                    continue
                if (schema_info[2], URIRef(schema_info[1])) in all_ns:
                    bottom_level_schema_path = schema_info[0]
                    bottom_level_schema_namespace = schema_info[1]
                    bottom_level_schema_namespace_prefix = schema_info[2]
                    schema_info_set = True
                    break
            if not schema_info_set:
                print("Input executable KG did not have any bottom level KG schemas")
                exit(1)
        else:
            bottom_level_schema_info = KG_SCHEMAS[kg_schema_name]
            bottom_level_schema_path = bottom_level_schema_info[0]
            bottom_level_schema_namespace = bottom_level_schema_info[1]
            bottom_level_schema_namespace_prefix = bottom_level_schema_info[2]

        self.bottom_level_kg = Graph(bind_namespaces="rdflib")
        self.bottom_level_kg.parse(bottom_level_schema_path, format="n3")

        self.input_kg += self.top_level_kg + self.bottom_level_kg
        self.output_kg = Graph(bind_namespaces="rdflib")

        self.bottom_level_schema_namespace = Namespace(bottom_level_schema_namespace)
        self.bottom_level_schema_namespace_prefix = bottom_level_schema_namespace_prefix

        self.bottom_level_kg = Graph(bind_namespaces="rdflib")
        self.bottom_level_kg.parse(bottom_level_schema_path, format="n3")

        self.bind_top_bottom_level_namespaces([self.input_kg, self.output_kg])

        self.task_type_dict = {}
        self.method_type_dict = {}
        self.atomic_task_list = []
        self.atomic_method_list = []
        self.data_type_list = []
        self.data_semantics_list = []
        self.data_structure_list = []

        self.parse_kgs()

    def bind_top_bottom_level_namespaces(self, kgs: List[Graph]):
        for kg in kgs:
            kg.bind(
                self.top_level_schema_namespace_prefix, self.top_level_schema_namespace
            )
            kg.bind(
                self.bottom_level_schema_namespace_prefix,
                self.bottom_level_schema_namespace,
            )

    def parse_kgs(self) -> None:
        atomic_task_subclasses = get_subclasses_of(self.atomic_task.iri, self.input_kg)
        for t in list(atomic_task_subclasses):
            task = Entity(t[0], self.atomic_task)
            self.atomic_task_list.append(task)
            self.task_type_dict[task.name] = 1

        atomic_method_subclasses = get_subclasses_of(
            self.atomic_method.iri, self.input_kg
        )
        for m in list(atomic_method_subclasses):
            method = Entity(m[0], self.atomic_method)
            self.atomic_method_list.append(method)
            self.method_type_dict[method.name] = 1

        data_type_subclasses = get_subclasses_of(self.data_entity.iri, self.input_kg)
        for d in list(data_type_subclasses):
            data_type = Entity(d[0], self.data_entity)
            self.data_type_list.append(data_type)

        data_semantics_subclasses = get_subclasses_of(
            self.data_semantics.iri, self.top_level_kg
        )
        for d in list(data_semantics_subclasses):
            if d[0] == self.data_entity.iri:
                continue
            data_semantics = Entity(d[0], self.data_semantics)
            self.data_semantics_list.append(data_semantics)

        data_structure_subclasses = get_subclasses_of(
            self.data_structure.iri, self.top_level_kg
        )
        for d in list(data_structure_subclasses):
            if d[0] == self.data_entity.iri:
                continue
            data_structure = Entity(d[0], self.data_structure)
            self.data_structure_list.append(data_structure)

    def create_pipeline_entity(self, name: str):
        return Task(
            self.bottom_level_schema_namespace + name,
            self.pipeline,
        )

    def add_and_attach_data_entity(
        self, data_entity: DataEntity, relation: URIRef, task_entity: Task
    ) -> None:
        self.add_exe_kg_data_entity(data_entity)
        self.add_exe_kg_relation(task_entity, relation, data_entity)

    def create_pipeline_task(self, pipeline_name: str) -> Task:
        pipeline = self.create_pipeline_entity(pipeline_name)
        self.add_instance(pipeline)

        return pipeline

    def create_data_entity(
        self,
        name: str,
        source_value: str,
        data_semantics_name: str,
        data_structure_name: str,
    ):
        return DataEntity(
            self.bottom_level_schema_namespace + name,
            self.data_entity,
            source_value,
            self.top_level_schema_namespace + data_semantics_name,
            self.top_level_schema_namespace + data_structure_name,
        )

    def add_task(
        self,
        prev_task: Task,
        task_type: str,
        input_data_entities: List[DataEntity],
        method_type: str,
        data_properties: dict,
        existing_data_entity_list: List[DataEntity],
    ) -> Task:

        relation_iri = (
            self.top_level_schema_namespace.hasNextTask
            if prev_task.type != "Pipeline"
            else self.top_level_schema_namespace.hasStartTask
        )

        parent_task = Task(
            self.bottom_level_schema_namespace + task_type, self.atomic_task
        )
        added_entity = self.add_instance_from_parent_with_exe_kg_relation(
            parent_task, relation_iri, prev_task
        )
        next_task = Task.from_entity(added_entity)
        next_task.has_input = input_data_entities[:]

        for data_entity in next_task.has_input:
            self.add_and_attach_data_entity(
                data_entity,
                self.top_level_schema_namespace.hasInput,
                next_task,
            )

        self.add_outputs_to_task(next_task)

        method_parent = Entity(
            self.bottom_level_schema_namespace + method_type, self.atomic_method
        )
        results = list(
            get_method_properties_and_methods(
                self.input_kg,
                self.top_level_schema_namespace_prefix,
                next_task.parent_entity.iri,
            )
        )

        chosen_property_method = next(
            filter(lambda pair: pair[1].split("#")[1] == method_type, results), None
        )
        if chosen_property_method is None:
            print(
                f"Property connecting task of type {task_type} with method of type {method_type} not found"
            )
            exit(1)

        self.add_instance_from_parent_with_exe_kg_relation(
            method_parent,
            chosen_property_method[0],
            next_task,
        )

        property_list = self.get_data_properties_plus_inherited_by_class_iri(
            method_parent.iri
        )

        for pair in property_list:
            property_iri = pair[0]
            property_name = property_iri.split("#")[1]
            range_iri = pair[1]
            input_property = Literal(
                lexical_or_value=data_properties[property_name],
                datatype=range_iri,
            )
            self.add_exe_kg_literal(next_task, property_iri, input_property)

        return next_task

    def add_outputs_to_task(self, task_entity: Task) -> None:
        results = list(
            get_output_properties_and_outputs(
                self.input_kg,
                self.top_level_schema_namespace_prefix,
                task_entity.parent_entity.iri,
            )
        )

        # task_type_index was incremented when creating the task entity
        task_type_index = self.task_type_dict[task_entity.type] - 1
        for output_property, output_entity in results:
            data_entity_iri = output_entity + str(task_type_index)
            data_entity = DataEntity(
                data_entity_iri, self.data_entity
            )
            self.add_and_attach_data_entity(
                data_entity, self.top_level_schema_namespace.hasOutput, task_entity
            )

    def create_next_task_cli(
        self, prompt: str, prev_task: Task, existing_data_entity_list: List[DataEntity]
    ) -> Union[None, Task]:
        print(prompt)
        for i, t in enumerate(self.atomic_task_list):
            print("\t{}. {}".format(str(i), t.name))
        print("\t{}. End pipeline".format(str(-1)))
        next_task_id = int(input())
        if next_task_id == -1:
            return None

        next_task_parent = self.atomic_task_list[next_task_id]
        relation_iri = (
            self.top_level_schema_namespace.hasNextTask
            if prev_task.type != "Pipeline"
            else self.top_level_schema_namespace.hasStartTask
        )
        task_entity = self.add_instance_from_parent_with_exe_kg_relation(
            next_task_parent, relation_iri, prev_task
        )

        task_entity = Task(task_entity.iri, task_entity.parent_entity)

        chosen_data_entity_list = get_input_for_existing_data_entities(
            existing_data_entity_list
        )
        for chosen_data_entity in chosen_data_entity_list:
            self.add_and_attach_data_entity(
                chosen_data_entity,
                self.top_level_schema_namespace.hasInput,
                task_entity,
            )
            task_entity.has_input.append(chosen_data_entity)
        (
            source_list,
            data_semantics_iri_list,
            data_structure_iri_list,
        ) = get_input_for_new_data_entities(
            self.data_semantics_list, self.data_structure_list
        )

        for source, data_semantics_iri, data_structure_iri in zip(
            source_list, data_semantics_iri_list, data_structure_iri_list
        ):
            data_entity = DataEntity(
                self.bottom_level_schema_namespace + source,
                self.data_entity,
                source,
                data_semantics_iri,
                data_structure_iri,
            )
            self.add_and_attach_data_entity(
                data_entity, self.top_level_schema_namespace.hasInput, task_entity
            )
            task_entity.has_input.append(data_entity)
            existing_data_entity_list.append(data_entity)

        self.add_outputs_to_task(task_entity)

        return task_entity

    def create_method(self, task_to_attach_to: Entity) -> None:
        # Entity
        print("Please choose a method for {}:".format(task_to_attach_to.type))

        results = list(
            get_method_properties_and_methods(
                self.input_kg,
                self.top_level_schema_namespace_prefix,
                task_to_attach_to.parent_entity.iri,
            )
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
            next_task = self.create_next_task_cli(prompt, prev_task, data_entities_list)
            if next_task is None:
                break

            self.create_method(next_task)

            prev_task = next_task

    def save(self, file_path: str) -> None:
        all_kgs = self.output_kg
        all_kgs.serialize(destination=file_path)

    def get_data_properties_plus_inherited_by_class_iri(self, class_iri: str):
        property_list = list(
            get_data_properties_by_entity_iri(class_iri, self.input_kg)
        )
        method_parent_classes = list(
            query_method_parent_classes(self.input_kg, class_iri)
        )
        for method_class_result_row in method_parent_classes:
            property_list += list(
                get_data_properties_by_entity_iri(
                    method_class_result_row[0], self.input_kg
                )
            )

        return property_list

    def add_exe_kg_data_entity(self, data_entity: DataEntity) -> None:
        self.add_instance(data_entity)

        if data_entity.has_source:
            has_source_iri, range_iri = get_first_query_result_if_exists(
                get_data_properties_by_entity_iri, self.data.iri, self.top_level_kg
            )

            source_literal = Literal(
                lexical_or_value=data_entity.has_source,
                datatype=range_iri,
            )

            self.add_exe_kg_literal(data_entity, has_source_iri, source_literal)

        if data_entity.has_data_structure:
            self.add_exe_kg_relation(
                data_entity,
                self.top_level_schema_namespace.hasDataStructure,
                Entity(data_entity.has_data_structure),
            )

        if data_entity.has_data_semantics:
            self.add_exe_kg_relation(
                data_entity,
                self.top_level_schema_namespace.hasDataSemantics,
                Entity(data_entity.has_data_semantics),
            )

    def add_instance_from_parent_with_exe_kg_relation(
        self, instance_parent: Entity, relation_iri: str, related_entity: Entity
    ) -> Entity:
        instance = self.create_entity_from_parent(instance_parent)
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

    def create_entity_from_parent(self, parent_entity: Entity) -> Entity:
        entity_name = self.name_instance(parent_entity)
        entity_iri = self.bottom_level_schema_namespace + entity_name
        return Entity(entity_iri, parent_entity)

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
        query_result = get_first_query_result_if_exists(
            query_method_iri_by_task_iri,
            self.input_kg,
            self.top_level_schema_namespace_prefix,
            task_iri,
        )
        if query_result is None:
            return None

        method_iri = str(query_result[0])

        query_result = get_first_query_result_if_exists(
            query_entity_parent_iri,
            self.input_kg,
            method_iri,
            self.top_level_schema_namespace.Method,
        )
        if query_result is None:
            return None

        method_parent_iri = str(query_result[0])

        return Entity(method_iri, Entity(method_parent_iri))

    def get_pipeline_and_first_task_iri(self) -> Tuple[str, str]:
        # assume one pipeline per file
        query_result = get_first_query_result_if_exists(
            query_pipeline_and_first_task_iri,
            self.input_kg,
            self.top_level_schema_namespace_prefix,
        )
        if query_result is None:
            print("Error: Pipeline and first task not found")
            exit(1)

        pipeline_iri, task_iri = query_result

        return str(pipeline_iri), str(task_iri)

    def parse_data_entity_by_iri(self, data_entity_iri: str) -> Optional[DataEntity]:
        query_result = get_first_query_result_if_exists(
            query_entity_parent_iri,
            self.input_kg,
            data_entity_iri,
            self.top_level_schema_namespace.DataEntity,
        )
        if query_result is None:
            return None

        data_entity_parent_iri = str(query_result[0])

        data_entity = DataEntity(data_entity_iri, Entity(data_entity_parent_iri))

        for s, p, o in self.input_kg.triples((URIRef(data_entity_iri), None, None)):
            field_name = property_name_to_field_name(str(p))
            if not hasattr(data_entity, field_name) or field_name == "type":
                continue
            field_value = self.property_value_to_field_value(str(o))
            setattr(data_entity, field_name, field_value)

        return data_entity

    def parse_task_by_iri(
        self, task_iri: str, canvas_method: visual_tasks.CanvasTaskCanvasMethod = None
    ) -> Optional[Task]:
        query_result = get_first_query_result_if_exists(
            query_entity_parent_iri,
            self.input_kg,
            task_iri,
            self.top_level_schema_namespace.AtomicTask,
        )

        if query_result is None:
            print(f"Cannot retrieve parent of task with iri {task_iri}. Exiting...")
            exit(1)

        task_parent_iri = str(query_result[0])

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
            field_name = property_name_to_field_name(str(p))
            if not hasattr(task, field_name) or field_name == "type":
                continue
            field_value = self.property_value_to_field_value(str(o))
            print(field_name, field_value)
            if field_name == "has_input" or field_name == "has_output":
                getattr(task, field_name).append(field_value)
            else:
                setattr(task, field_name, field_value)

        return task
