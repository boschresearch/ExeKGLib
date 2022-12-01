import rdflib
import pandas as pd


class PipelineProcessor:
    def __init__(self):
        self.raw_data = None
        self.extra_data_list = {}
        print("PipelineProcessor initialized")

    def load_graph(self, kg_path=r"KG/exeKGOntology.ttl"):
        """load the KG from .ttl file into the object"""
        self.graph.parse(kg_path)

    def load_data(self, raw_path=r"data/a.csv"):
        """load the raw csv data
        Args:
            raw_path: csv file path
        """
        self.raw_data = pd.read_csv(raw_path, delimiter=",", encoding="ISO-8859-1")

    def parse_namespace(self):
        self.dict_namespace = parse_namespace(self.graph)

    def select_program(self, program, name: str = "WeldingProgramNumber"):
        # program must be int to be compared with excel data
        return (
            self.raw_data[name] == int(program)
            if (program and name)
            else [True] * len(self.raw_data)
        )

    def welding_program_filter(
        self, input, filter_value: int = 1, filter_name: str = "WeldingProgramNumber"
    ):
        """currently only used for distinguishing filtering different program numbers"""
        # if(filter_value and filter_name):
        #     #input = self.raw_data[data_source]
        #     filter_rows = self.raw_data[filter_name]==filter_value

        #     # optionally add new column to the data base while keep the same column and index
        #     # self.raw_data[data_source + '_' + str(filter_name) + '_' + str(filter_value)] = np.NaN
        #     # self.raw_data.loc[filter_rows, data_source + '_' + str(filter_name) + '_' + str(filter_value)] = input[filter_rows]
        #     # return self.raw_data[data_source + '_' + str(filter_name) + '_' + str(filter_value)][filter_rows]
        #     return input[filter_rows]

        # else:
        #     return input
        # print('input = ', input)
        # print('select_program = ',self.select_program(filter_value, filter_name) )
        return input[self.select_program(filter_value, filter_name)]


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


def execute_pipeline(pipelines: list, debug: bool = False, **kwargs):
    """parse and execute a whole pipeline, starting from hasStartTask, until no hasNextTask"""
    visualizer = kwargs.get("visualizer", None)
    statistics_analyzer = kwargs.get("statistics_analyzer", None)
    ML_analyser = kwargs.get("ML_analyser", None)

    assert (
        isinstance(visualizer, PipelineProcessor)
        or isinstance(statistics_analyzer, PipelineProcessor)
        or isinstance(ML_analyser, PipelineProcessor)
    )

    graph = (
        visualizer.graph
        if (visualizer)
        else statistics_analyzer.graph
        if (statistics_analyzer)
        else ML_analyser.graph
    )
    dict_namespace = (
        visualizer.dict_namespace
        if visualizer
        else statistics_analyzer.dict_namespace
        if statistics_analyzer
        else ML_analyser.dict_namespace
    )

    for pipeline_name in pipelines:
        pipeline_po = parse_entity(graph, pipeline_name, dict_namespace)
        if debug:
            print("pipeline_property_object: ", pipeline_po)

        # 4.1 the starting task
        all_tasks = []

        start_po = parse_entity(
            graph, pipeline_po["exeKG:hasStartTask"][0], dict_namespace
        )
        # print('start_po = ', start_po)
        # all_tasks[pipeline_po['exeKG:hasStartTask'][0]] = start_po
        all_tasks.append(start_po)
        # statistics_analyzer.execute_task(start_po)

        # 4.2 for the rest of the following plot tasks
        task_po = start_po
        while "exeKG:hasNextTask" in task_po:
            # append each task with corresponding properties to the plot_tasks
            next_task = task_po["exeKG:hasNextTask"][0]
            task_po = parse_entity(graph, next_task, dict_namespace)
            if task_po:
                all_tasks.append(task_po)

        # print("all_tasks: ", all_tasks)
        execute_tasks(all_tasks, visualizer, statistics_analyzer, ML_analyser)


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


def extract_label(cstr, dict_namesgpace):
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
    """query defined by the cquery string, and transfer to a proper format"""

    pipeline = graph.query(cquery)
    pipeline = [extract_entity(e, dict_namespace) for e in pipeline][0]

    return pipeline
