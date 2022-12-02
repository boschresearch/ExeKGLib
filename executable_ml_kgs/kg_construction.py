from rdflib import Graph, URIRef, RDF, Namespace, Literal

g = Graph(bind_namespaces="rdflib")
g1 = Graph(bind_namespaces="rdflib")
exekg_namespace = Namespace("http://www.semanticweb.org/zhuoxun/ontologies/exeKG#")
g.bind("exeKG", exekg_namespace)
namespace_dict = {}
task_type_dict = {}
method_type_dict = {}
data_entity_dict = {}


def read_ontology(url):
    g1.parse("kg/" + url)
    namespace_dict = g1.namespace_manager.__dict__["_NamespaceManager__trie"].copy()
    for key in namespace_dict:
        if key == "http://www.w3.org/XML/1998/namespace":
            namespace_dict[key] = "xml:"
        elif key == "http://www.w3.org/1999/02/22-rdf-syntax-ns#":
            namespace_dict[key] = "rdf:"
        elif key == "http://www.w3.org/2000/01/rdf-schema#":
            namespace_dict[key] = "rdfs:"
        elif key == "http://www.w3.org/2001/XMLSchema#":
            namespace_dict[key] = "xsd:"
        elif key == "http://www.w3.org/2002/07/owl#":
            namespace_dict[key] = "owl:"
        else:
            namespace_dict[key] = key.split("/")[-1].replace("#", ":")
    return namespace_dict


def pipeline_creation():
    user_pipeline = "test"
    pipeline_name = user_pipeline + "Pipeline"
    output_file = "kg/" + pipeline_name + ".ttl"
    add_task(pipeline_name, "Pipeline")
    add_method(method_type_dict)
    add_data_entity(data_entity_dict)

    with open(output_file, "w") as f:
        f.write((g1 + g).serialize())


def add_task(item_name, item_type):
    new_item_name = URIRef(exekg_namespace + item_name)
    new_item_type = URIRef(exekg_namespace + item_type)
    g.add((new_item_name, RDF.type, new_item_type))
    if item_type == "Pipeline":
        prompt = "Enter inputs of the pipeline, enter 'quit' to stop input: "
        input_str = input(prompt)
        if input_str != "quit":
            data_entity_dict[input_str] = {
                "DataStructure": "Array",
                "DataSemantics": "?",
            }  # todo: input_system
            input_instance = URIRef(exekg_namespace + input_str)
            g.add((new_item_name, exekg_namespace.hasInput, input_instance))
        while input_str != "quit":
            input_str = input(prompt)
            if input_str != "quit":
                data_entity_dict[input_str] = {
                    "DataStructure": "Array",
                    "DataSemantics": "?",
                }  # TODO: input system
                input_instance = URIRef(exekg_namespace + input_str)
                g.add((new_item_name, exekg_namespace.hasInput, input_instance))

        next_task_flag = int(
            input(
                "Please enter the next task:\n\t0: Visual Task\n\t1: Statistic Task\n\t2. ML Task:\n"
            )
        )
        if (
            next_task_flag == 0
        ):  # TODO: only visualPipeline has initial Task(CanvasTask), maybe in ontology set a class as "initialTask"
            next_task_type = "CanvasTask"
            next_task_name = name_task_with_type(next_task_type, task_type_dict)
            next_task_instance = URIRef(exekg_namespace + next_task_name)
            g.add((new_item_name, exekg_namespace.hasStartTask, next_task_instance))
        if next_task_flag == 1:
            next_task_type = "StatisticTask"
            next_task_name = name_task_with_type(next_task_type, task_type_dict)
            next_task_instance = URIRef(exekg_namespace + next_task_name)
            g.add((new_item_name, exekg_namespace.hasStartTask, next_task_instance))
        if next_task_flag == 2:
            next_task_type = "MLTask"
            next_task_name = name_task_with_type(next_task_type, task_type_dict)
            next_task_instance = URIRef(exekg_namespace + next_task_name)
            g.add((new_item_name, exekg_namespace.hasStartTask, next_task_instance))

        add_task(next_task_name, next_task_type)
    else:
        # Method
        method_property_query = (
            "\nSELECT ?p ?m WHERE {?p rdfs:domain exeKG:" + item_type + " . "
            "?p rdfs:range ?m . "
            "?m rdfs:subClassOf exeKG:AtomicMethod . }"
        )  # method property
        i = 0
        method_list = []
        print("please_enter_available_method_for {}:".format(item_type))
        for pair in list(g1.query(method_property_query)):
            tmp_method = pair[1].split("#")[1]
            print("\t{}. {}".format(str(i), tmp_method))
            method_list.append(tmp_method)
            i += 1
        method_id = int(input())
        method_type = method_list[method_id]
        method_name = name_method_with_type(method_type, method_type_dict)
        has_method_instance = URIRef(pair[0])
        method_instance = URIRef(pair[1] + method_name)
        g.add((new_item_name, has_method_instance, method_instance))

        # data
        # pick data from dataEntityDict, according to allowedDataStructure of methodType

        # DatatypeProperty
        method_datatype_property_query = (
            "\nSELECT ?p ?r WHERE {?p rdfs:domain exeKG:" + method_type + " . "
            "?p rdfs:range ?r . "
            "?p rdf:type owl:DatatypeProperty . }"
        )
        property_list = list(g1.query(method_datatype_property_query))
        if property_list:
            print("Please enter requested properties for {}:".format(method_type))
            for pair in property_list:
                property_instance = URIRef(pair[0])
                range = pair[1].split("#")[1]
                range_instance = URIRef(pair[1])

                input_property = Literal(
                    input("\t{} in range({}): ".format(pair[0].split("#")[1], range)),
                    datatype=range_instance,
                )
                g.add((new_item_name, property_instance, input_property))

        # Next Task
        next_task_query = "\nSELECT ?t WHERE {?t rdfs:subClassOf exeKG:AtomicTask . }"
        i = 0
        atomic_task_list = []
        print("Please enter the next Task:")
        for t in list(g1.query(next_task_query)):
            tmp_task = t[0].split("#")[1]
            print("\t{}. {}".format(str(i), tmp_task))
            atomic_task_list.append(tmp_task)
            i += 1
        print("\t{}. End pipeline".format(str(-1)))
        task_id = int(input())
        if task_id != -1:
            task_type = atomic_task_list[task_id]
            task_name = name_task_with_type(task_type, task_type_dict)
            task_namespace = t[0].split("#")[0] + "#"
            task_instance = URIRef(task_namespace + task_name)
            g.add((new_item_name, exekg_namespace.hasNextTask, task_instance))
            add_task(task_name, task_type)


def name_task_with_type(item_type, item_type_dict):
    if item_type not in item_type_dict:
        item_type_dict[item_type] = 1
    else:
        item_type_dict[item_type] += 1
    item_name = item_type + str(item_type_dict[item_type])
    return item_name


def name_method_with_type(method_type, method_type_dict):
    if method_type not in method_type_dict:
        method_type_dict[method_type] = 0
    method_name = method_type + "0"
    return method_name


def add_method(method_type_dict):
    for method_type in method_type_dict.keys():
        method_instance = URIRef(
            exekg_namespace + name_method_with_type(method_type, method_type_dict)
        )
        method_type = URIRef(exekg_namespace + method_type)
        g.add((method_instance, RDF.type, method_type))


def add_data_entity(data_entity_dict):  # TODO
    for data_entity in data_entity_dict.keys():
        data_entity_instance = URIRef(exekg_namespace + data_entity)
        g.add((data_entity_instance, RDF.type, exekg_namespace.DataEntity))
        data_structure_type = URIRef(
            exekg_namespace + data_entity_dict[data_entity]["DataStructure"]
        )
        g.add((data_entity_instance, exekg_namespace.hasDataStructure, data_structure_type))
        data_semantics_type = URIRef(
            exekg_namespace + data_entity_dict[data_entity]["DataSemantics"]
        )
        g.add((data_entity_instance, exekg_namespace.hasDataSemantics, data_semantics_type))


if __name__ == "__main__":
    url = "exeKGOntology.ttl"
    namespace_dict = read_ontology(url)
    pipeline_creation()
