import rdflib


def execute_tasks(all_tasks: list, visualizer, statistics_analyzer, ML_analyser):
    """select the corresponding analyser for the task"""
    # print('all_tasks = ', all_tasks)
    for task_po in all_tasks:
        print("task_po = ", task_po)
        method_name = task_po["exeKG:hasMethod"][0]
        if "Visual" in method_name:
            out = visualizer.execute_task(task_po)
            print("output of " + str(method_name) + "\n", out)
        elif "Stats" in method_name:
            out = statistics_analyzer.execute_task(task_po)
            print("output of " + str(method_name) + "\n", out)
        elif "ML" in method_name:
            out = ML_analyser.execute_task(task_po)
            print("output of " + str(method_name) + "\n", out)
        # TODO: safer execution is needed for old KG
        else:
            analyzer = visualizer or statistics_analyzer or ML_analyser
            analyzer.execute_task(task_po)

        print("######## next task ######")


def parse_entity(graph, centity, dict_namespace, verbose=False) -> dict:

    # TODO: make the query a module
    centity = centity.split(":")[1]
    cquery = (
        "\nSELECT ?p ?o WHERE {exeKG:" + centity + " ?p ?o .}"
    )  # if "SELECT * ...", the order of the answer may be false
    list_ctask_property_object = graph.query(cquery)

    # print(centity)
    # for e in list_ctask_predicate_object:
    #     print(extract_entity(e))

    dict_ctask = {}
    for cpo in list_ctask_property_object:
        # print("cpo = ", cpo)
        if verbose == True:
            print(extract_entity(cpo, dict_namespace))
        cpredicate = extract_label(cpo[0], dict_namespace)

        # ignore rdf:type when constructing the dict_ctask
        if cpredicate != "rdf:type":
            cobject = extract_label(cpo[1], dict_namespace)
            if cpredicate not in dict_ctask:
                dict_ctask[cpredicate] = [cobject]
            else:
                dict_ctask[cpredicate].append(cobject)

    return dict_ctask


def extract_entity(cstatement, dict_namespace):
    # print([extract_label(e) for e in cstatement])
    return [extract_label(e, dict_namespace) for e in cstatement]


def extract_label(cstr, dict_namespace):
    """convert the input string to a readable format"""
    if isinstance(cstr, rdflib.term.Literal):
        return str(cstr)
    elif len(cstr.split("#")) > 1:
        cnamespace = cstr.split("#")[0] + "#"
        # print("cstr = ", cstr)
        # print("namespace = ", cnamespace)
        # print(" in extract label: ", dict_namespace[cnamespace] + cstr.split('#')[1])
        return dict_namespace[cnamespace] + cstr.split("#")[1]
    else:
        return "BLANK"


def parse_namespace(graph):
    """
    parse namespace used for readable information
    Args:
        graph: the rdflib Graph object
    return:
        a dictionary mapping the namespace fullnames to shortcuts

    """
    dict_namespace = graph.namespace_manager.__dict__["_NamespaceManager__trie"].copy()
    for key in dict_namespace:
        if key == "http://www.w3.org/XML/1998/namespace":
            dict_namespace[key] = "xml:"
        elif key == "http://www.w3.org/1999/02/22-rdf-syntax-ns#":
            dict_namespace[key] = "rdf:"
        elif key == "http://www.w3.org/2000/01/rdf-schema#":
            dict_namespace[key] = "rdfs:"
        elif key == "http://www.w3.org/2001/XMLSchema#":
            dict_namespace[key] = "xsd:"
        elif key == "http://www.w3.org/2002/07/owl#":
            dict_namespace[key] = "owl:"
        else:
            dict_namespace[key] = key.split("/")[-1].replace("#", ":")
    return dict_namespace


def query(graph, cquery, dict_namespace):
    """Query defined by the cquery string, and transfer to a proper format."""

    pipeline = graph.query(cquery)
    pipeline = [extract_entity(e, dict_namespace) for e in pipeline][0]

    return pipeline
