from rdflib import URIRef, RDF, Namespace, Literal, Graph

from .entity import Entity


class ExeKG:
    def __init__(self, exe_kg_namespace_iri, ontology_path):
        self.exe_kg = Graph(bind_namespaces="rdflib")
        self.exe_kg_namespace = Namespace(exe_kg_namespace_iri)
        self.exe_kg_namespace_prefix = exe_kg_namespace_iri.split("/")[-1][:-1]
        self.exe_kg.bind(self.exe_kg_namespace_prefix, self.exe_kg_namespace)

        self.atomic_task = Entity(self.exe_kg_namespace.AtomicTask)
        self.atomic_method = Entity(self.exe_kg_namespace.AtomicMethod)
        self.data_entity = Entity(self.exe_kg_namespace.DataEntity)
        self.pipeline = Entity(self.exe_kg_namespace.Pipeline)

        self.next_task_flag_type_dict = {
            0: "CanvasTask",
            1: "StatisticTask",
            2: "MLTask",
        }

        self.task_type_dict = {}
        self.method_type_dict = {}
        self.data_entity_dict = {}
        self.atomic_task_list = []
        self.atomic_method_list = []
        self.data_type_list = []
        self.task_instances_list = []

        self.ontology = Graph(bind_namespaces="rdflib")
        self.ontology_path = ontology_path
        self.parse_ontology(ontology_path)

    def parse_ontology(self, iri):
        self.ontology.parse(iri, format="n3")

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

        data_entity = Entity(self.exe_kg_namespace.Data)
        data_type_subclasses = self.get_data_type_subclasses()
        for d in list(data_type_subclasses):
            data_type = Entity(d[0], data_entity)
            self.data_type_list.append(data_type)

    def create_pipeline_task(self, pipeline_name):
        pipeline = Entity(
            self.exe_kg_namespace + pipeline_name,
            self.pipeline,
        )
        self.add_instance(pipeline)

        prompt = "Enter inputs of the pipeline, enter 'quit' to stop input: "
        input_str = input(prompt)
        while input_str != "quit":
            self.data_entity_dict[input_str] = {
                "DataStructure": "Array",
                "DataSemantics": "?",
            }  # TODO: input system

            self.add_data_input_to_instance(
                pipeline, input_str, "Array", "?"
            )  # TODO: make hardcoded values dynamic

            input_str = input(prompt)

        return pipeline

    def create_next_task(self, prompt, prev_task):
        # Next Entity
        print(prompt)
        for i, t in enumerate(self.atomic_task_list):
            print("\t{}. {}".format(str(i), t.name))
        print("\t{}. End pipeline".format(str(-1)))
        next_task_id = int(input())
        if next_task_id == -1:
            return None

        next_task_parent = self.atomic_task_list[next_task_id]
        relation_name = (
            "hasNextTask" if prev_task.type != "Pipeline" else "hasStartTask"
        )
        return self.add_instance_from_parent_with_exe_kg_relation(
            next_task_parent, relation_name, prev_task
        )

    def create_method(self, task_to_attach_to):
        # Entity
        print("Please choose a method for {}:".format(task_to_attach_to.type))
        results = list(self.get_method_properties_and_methods(task_to_attach_to.type))
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
            selected_property_and_method[0].split("#")[1],
            task_to_attach_to,
        )

        # data
        # pick data from dataEntityDict, according to allowedDataStructure of methodType

        # DatatypeProperty
        property_list = list(self.get_method_datatype_properties(method_parent.name))
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

    def start_pipeline_creation(self, pipeline_name):
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

    def save(self, file_path):
        exe_kg_with_ontology = self.ontology + self.exe_kg
        exe_kg_with_ontology.serialize(destination=file_path)

    def query_ontology(self, query):
        return self.ontology.query(query)

    def get_method_datatype_properties(self, entity_type):
        return self.query_ontology(
            "\nSELECT ?p ?r WHERE {?p rdfs:domain "
            + self.exe_kg_namespace_prefix
            + ":"
            + entity_type
            + " . "
            "?p rdfs:range ?r . "
            "?p rdf:type owl:DatatypeProperty . }"
        )

    def get_method_properties_and_methods(self, entity_type):
        return self.query_ontology(
            "\nSELECT ?p ?m WHERE {?p rdfs:domain "
            + self.exe_kg_namespace_prefix
            + ":"
            + entity_type
            + " . "
            "?p rdfs:range ?m . "
            "?m rdfs:subClassOf " + self.exe_kg_namespace_prefix + ":AtomicMethod . }"
        )  # method property

    def get_atomic_method_subclasses(self):
        return self.query_ontology(
            "\nSELECT ?t WHERE {?t rdfs:subClassOf "
            + self.exe_kg_namespace_prefix
            + ":AtomicMethod . }"
        )

    def get_atomic_task_subclasses(self):
        return self.query_ontology(
            "\nSELECT ?t WHERE {?t rdfs:subClassOf "
            + self.exe_kg_namespace_prefix
            + ":AtomicTask . }"
        )

    def get_data_type_subclasses(self):
        return self.query_ontology(
            "\nSELECT ?t WHERE {?t rdfs:subClassOf "
            + self.exe_kg_namespace_prefix
            + ":Data . }"
        )

    def add_data_input_to_instance(
        self, instance, data_instance_name, data_structure, data_semantics
    ):
        data_instance_iri = self.exe_kg_namespace + data_instance_name
        data_instance = Entity(data_instance_iri, self.data_entity)
        self.add_instance(data_instance)

        data_structure_iri = URIRef(self.exe_kg_namespace + data_structure)
        data_structrure_instance = Entity(data_structure_iri)
        self.add_exe_kg_relation(
            data_instance,
            "hasDataStructure",
            data_structrure_instance,
        )

        data_semantics_iri = URIRef(self.exe_kg_namespace + data_semantics)
        data_semantics_instance = Entity(data_semantics_iri)
        self.add_exe_kg_relation(
            data_instance,
            "hasDataSemantics",
            data_semantics_instance,
        )

        self.add_exe_kg_relation(instance, "hasInput", data_instance)

    def add_instance_from_parent_with_exe_kg_relation(
        self, instance_parent, relation_name, related_entity
    ):
        instance_name = self.name_instance(instance_parent)
        instance_iri = self.exe_kg_namespace + instance_name
        instance = Entity(instance_iri, instance_parent)
        self.add_instance(instance)
        self.add_exe_kg_relation(related_entity, relation_name, instance)

        return instance

    def add_instance(self, entity_instance):
        if (
            entity_instance.parent_entity
            and (entity_instance.iri, None, None) not in self.exe_kg
        ):
            self.exe_kg.add(
                (entity_instance.iri, RDF.type, entity_instance.parent_entity.iri)
            )

    def add_exe_kg_relation(self, from_entity, relation_name, to_entity):
        self.exe_kg.add(
            (
                from_entity.iri,
                URIRef(self.exe_kg_namespace + relation_name),
                to_entity.iri,
            )
        )

    def add_literal(self, from_entity, relation, literal):
        self.exe_kg.add((from_entity.iri, relation, literal))

    def name_instance(self, parent_entity):
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
