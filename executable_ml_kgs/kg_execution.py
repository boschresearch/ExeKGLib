import time

import matplotlib.pyplot as plt
import pandas as pd

from classes.pipeline_execution import MLAnalyser
from classes.pipeline_execution import StatsiticsAnalyzer
from classes.pipeline_execution import Visualizer
from classes.pipeline_execution.utils import parse_namespace, query
from classes.pipeline_execution.pipeline_processor import execute_pipeline


def visu_pipeline(
        raw_data_path=r"data/singlefeatures_wm1.csv",
        ontology_path=r"kg/testVisualKG.ttl",
        debug=True,
        out_name="plot.jpg",
        show=True,
        **kwargs,
):
    """visu task pipeline for debugging"""

    # 1. build current knowledge graph

    visualizer = Visualizer()
    visualizer.load_graph(ontology_path)
    visualizer.load_data(raw_data_path)
    visualizer.program = kwargs.get("program", None)

    if debug:
        print(visualizer.graph)
        print(visualizer.raw_data)

    start_time = time.time()

    # 2. namespace dictionary for mapping namespaces to shortcuts
    visualizer.dict_namespace = parse_namespace(visualizer.graph)
    if debug:
        print(visualizer.dict_namespace)

    # 3. query the visu pipeline
    graph = visualizer.graph
    cquery = "\nSELECT ?s WHERE {?s rdf:type exeKG:Pipeline}"
    visu_pipeline = query(visualizer.graph, cquery, visualizer.dict_namespace)

    if debug:
        print("visu_pipeline:", visu_pipeline)

    # 4. construct the canvas task + plot task
    execute_pipeline(visu_pipeline, True, visualizer=visualizer)

    # for pipeline_name in visu_pipeline:
    #     pipeline_po = parse_entity(visualizer.graph, pipeline_name, visualizer.dict_namespace)
    #     if(debug):
    #         print('pipeline_property_object: ',pipeline_po)

    #     # 4.1 the starting task, normally Canvas Task
    #     start_po = parse_entity(visualizer.graph, pipeline_po['exeKG:hasStartTask'][0], visualizer.dict_namespace)
    #     if(debug):
    #         print('starting_task_property_object: ', start_po)

    #     fig, grid = visualizer.canvas_task(start_po)

    #     # 4.2 for the rest of the following plot tasks
    #     plot_tasks = []
    #     task_po = start_po
    #     while('exeKG:hasNextTask' in task_po):
    #         # append each task with corresponding properties to the plot_tasks
    #         next_task = task_po['exeKG:hasNextTask'][0]
    #         task_po = parse_entity(visualizer.graph, next_task, visualizer.dict_namespace)
    #         if(task_po):
    #             plot_tasks.append(task_po)
    #             visualizer.plot_task(task_po, fig, grid, out_name)
    #     print("plot_tasks: ", plot_tasks)

    # plt.savefig(visualizer.dir_out + r'/'+ out_name)
    end_time = time.time()
    print("total time for visu_pipeline = ", end_time - start_time)

    if show:
        plt.legend()
        plt.show()

    return end_time - start_time


def stats_visu_pipeline(
        raw_data_path=r"data/singlefeatures_wm1.csv",
        ontology_path=r"kg/testStatsVisuKG.ttl",
        debug=False,
        out_name="statistics.jpg",
        show=False,
        **kwargs,
):
    """the statistics pipeline for debugging only, currently outlier detection pipeline from the paper"""

    # 1. build current knowledge graph
    program = kwargs.get("program", "")
    program = "" if (program is None) else program
    statistics_analyzer = StatsiticsAnalyzer()
    statistics_analyzer.program = program
    statistics_analyzer.load_graph(ontology_path)
    statistics_analyzer.load_data(raw_data_path)
    data_source = "QVALUEActual"
    selected_rows = statistics_analyzer.select_program(program, "WeldingProgramNumber")
    visu = Visualizer()

    start_time = time.time()

    # 2. namespace dictionary for mapping namespaces to shortcuts
    statistics_analyzer.dict_namespace = parse_namespace(statistics_analyzer.graph)
    # print(statistics_analyzer.dict_namespace)

    # 3. query the stats pipeline
    graph = statistics_analyzer.graph
    # cquery = "\nSELECT ?s WHERE {?s rdf:type exeKG:Pipeline}"
    cquery = "\nSELECT ?s WHERE {?s rdf:type exeKG:Pipeline}"
    stats_pipelines = query(graph, cquery, statistics_analyzer.dict_namespace)

    # 4. execute pipeline
    # for i in execute_pipeline(stats_pipelines, statistics_analyzer, True):
    #     print('i = ', i)
    execute_pipeline(stats_pipelines, True, statistics_analyzer=statistics_analyzer)

    # print(statistics_analyzer.extra_data_list)
    # print(statistics_analyzer.raw_data)

    print(statistics_analyzer.extra_data_list)
    for i in statistics_analyzer.extra_data_list:
        visu.scatter_plot(input_data=statistics_analyzer.raw_data[i], label=i)

    end_time = time.time()
    print("stats_visu_pipeline time = ", end_time - start_time)

    plt.xlim([-10, 5000])
    plt.ylim([-50, 150])
    plt.xlabel("Number of Wielding operations")
    plt.ylabel("Q-Value")

    if show:
        plt.legend()
        plt.show()
    return end_time - start_time


def ML_pipeline(
        raw_data_path=r"data/singlefeatures_wm1.csv",
        ontology_path=r"KG_ML/exeKGExample.ttl",
        debug=True,
        out_name="statistics_extract.jpg",
        show=False,
        exp=3,
):
    """ML_pipeline for debugging only"""
    global num_exps
    num_exps = exp
    # 1. init
    ml_analyser = MLAnalyser()
    ml_analyser.load_data(raw_data_path)
    ml_analyser.load_graph(ontology_path)
    ml_analyser.parse_namespace()

    visualizer = Visualizer()
    visualizer.raw_data = ml_analyser.raw_data
    visualizer.graph = ml_analyser.graph
    visualizer.dict_namespace = ml_analyser.dict_namespace
    visualizer.extra_data_list = ml_analyser.extra_data_list

    statistics_analyzer = StatsiticsAnalyzer()
    statistics_analyzer.raw_data = ml_analyser.raw_data
    statistics_analyzer.graph = ml_analyser.graph
    statistics_analyzer.dict_namespace = ml_analyser.dict_namespace
    statistics_analyzer.extra_data_list = ml_analyser.extra_data_list

    start_time = time.time()
    # 2. query pipeline
    cquery = "\nSELECT ?s WHERE {?s rdf:type exeKG:Pipeline}"
    stats_pipelines = query(ml_analyser.graph, cquery, ml_analyser.dict_namespace)
    # print(stats_pipelines)

    # 3. execute pipeline
    execute_pipeline(
        stats_pipelines,
        True,
        visualizer=visualizer,
        statistics_analyzer=statistics_analyzer,
        ML_analyser=ml_analyser,
    )

    # print(ml_analyser.extra_data_list)
    end_time = time.time()

    if show:
        plt.legend()
        plt.show()

    return end_time - start_time


def main_ml_visu():
    # stats_visu_pipeline(program=1)#, show=True)
    # visu_pipeline(debug=False, out_name="Qvalue_line.jpg", program = 2)#, program=2)
    # visu_pipeline(debug=False, out_name="Qvalue_line.jpg", program=1)
    # visu_pipeline(r'data/singlefeatures_wm1.csv', r'KG/testVisualKG_scatter.ttl', True, out_name="Qvalue_scatter.jpg", scatter=True)
    ML_pipeline(ontology_path=r"KG_ML/exeKGExampleKNN.ttl", show=False)

    knn_kg_path = r"KG_ML/exeKGExampleKNN.ttl"
    time1 = []
    for i in range(10):
        time1.append(
            ML_pipeline(
                raw_data_path=r"data/singlefeatures_wm1.csv",
                ontology_path=knn_kg_path,
                show=False,
                exp=i + 3,
            )
        )
        # time.append(stats_visu_pipeline(program=1, debug=False, show=True))
        # time.append(visu_pipeline(debug=False, out_name="Qvalue_line.jpg"))#, show=True))

    print(time1)

    ##### MLP hyperparameters
    mlp_kg_path = r"KG_ML/exeKGExampleMLP.ttl"
    time2 = []
    for i in range(3):
        solver = ["lbfgs", "sgd", "adam"]
        for j in range(4):
            time2.append(
                ML_pipeline(
                    raw_data_path=r"data/singlefeatures_wm1.csv",
                    ontology_path=mlp_kg_path,
                    show=False,
                    exp=solver[i],
                )
            )
        # time.append(stats_visu_pipeline(program=1, debug=False, show=True))
        # time.append(visu_pipeline(debug=False, out_name="Qvalue_line.jpg"))#, show=True))

    print(time2)


def main_visu(input_path=r"kg/testVisualKG.ttl"):
    visu_pipeline(debug=False, out_name="Qvalue_line.jpg", program=1)
    times = []
    visu_ontology = input_path
    for i in range(3):
        times.append(
            visu_pipeline(
                ontology_path=visu_ontology,
                debug=False,
                out_name="Qvalue_line.jpg",
                program=1,
            )
        )
    for i in range(3):
        times.append(
            visu_pipeline(
                ontology_path=visu_ontology,
                debug=False,
                out_name="Qvalue_line.jpg",
                program=2,
            )
        )
    for i in range(4):
        times.append(
            visu_pipeline(
                ontology_path=visu_ontology,
                debug=False,
                out_name="Qvalue_line.jpg",
                program=None,
            )
        )
    print(times)


def main_visu_stats(input_path=r"kg/testStatsVisuKG.ttl"):
    visu_pipeline(debug=False, out_name="Qvalue_line.jpg", program=1)
    times = []
    for i in range(10):
        # time1.append(ML_pipeline(raw_data_path = r'data/singlefeatures_wm1.csv', ontology_path=input_path, show=False, exp = i+3))
        times.append(stats_visu_pipeline(program=1, debug=False, show=False))
        # time.append(visu_pipeline(debug=False, out_name="Qvalue_line.jpg"))#, show=True))

    print(times)


def main_stats(input_path=r"kg/testStatsOnly.ttl"):
    visu_pipeline(debug=False, out_name="Qvalue_line.jpg", program=1)
    times = []
    for i in range(10):
        # time1.append(ML_pipeline(raw_data_path = r'data/singlefeatures_wm1.csv', ontology_path=input_path, show=False, exp = i+3))
        times.append(stats_visu_pipeline(debug=False, show=False))
        # time.append(visu_pipeline(debug=False, out_name="Qvalue_line.jpg"))#, show=True))

    print(times)


def main_stats_ML():
    ML_pipeline(ontology_path=r"kg/exeKGExampleKNN_noVisu.ttl", show=False)

    # # LR
    # knn_kg_path = r"kg/exeKGExampleLR_noVisu.ttl"
    # time0 = []
    # for i in range(10):
    #     time0.append(
    #         ML_pipeline(
    #             raw_data_path=r"data/singlefeatures_wm1.csv",
    #             ontology_path=knn_kg_path,
    #             show=False,
    #             exp=i + 3,
    #         )
    #     )

    # knn
    knn_kg_path = r"kg/exeKGExampleKNN_noVisu.ttl"
    time1 = []
    for i in range(10):
        time1.append(
            ML_pipeline(
                raw_data_path=r"data/singlefeatures_wm1.csv",
                ontology_path=knn_kg_path,
                show=False,
                exp=i + 3,
            )
        )

    # ##### MLP hyperparameters
    # mlp_kg_path = r"kg/exeKGExampleMLP_noVisu.ttl"
    # time2 = []
    # for i in range(3):
    #     solver = ["lbfgs", "sgd", "adam"]
    #     for j in range(4):
    #         time2.append(
    #             ML_pipeline(
    #                 raw_data_path=r"data/singlefeatures_wm1.csv",
    #                 ontology_path=mlp_kg_path,
    #                 show=False,
    #                 exp=solver[i],
    #             )
    #         )
    # time.append(stats_visu_pipeline(program=1, debug=False, show=True))
    # time.append(visu_pipeline(debug=False, out_name="Qvalue_line.jpg"))#, show=True))

    # print(time0)
    print(time1)
    # print(time2)


from classes.graph import ExeKG

exe_kg_namespaces_and_ontologies = {
    "Data Science": (
        "http://www.semanticweb.org/ontologies/ds#",
        "https://raw.githubusercontent.com/baifanzhou/ExeKGOntology/main/ds_exeKGOntology.ttl",
    ),
    "Visual": (
        "http://www.semanticweb.org/ontologies/visu#",
        "https://raw.githubusercontent.com/baifanzhou/ExeKGOntology/main/visu_exeKGOntology.ttl",
    ),
    "Statistics": (
        "http://www.semanticweb.org/ontologies/stats#",
        "https://raw.githubusercontent.com/baifanzhou/ExeKGOntology/main/stats_exeKGOntology.ttl",
    ),
    "Machine Learning": (
        "http://www.semanticweb.org/ontologies/ml#",
        "https://raw.githubusercontent.com/baifanzhou/ExeKGOntology/main/ml_exeKGOntology.ttl",
    ),
    "generic": (
        "http://www.semanticweb.org/zhuoxun/ontologies/exeKG#",
        "./kg/testVisualKG.ttl",
        # "./kg/exeKGExampleKNN_noVisu.ttl",
    ),
}

if __name__ == "__main__":
    # main_stats_ML()
    # main_stats()
    # main_visu()
    # main_ml()
    # main_visu_stats()

    chosen_exe_kg_type = "generic"  # TODO: get user input
    namespace_iri, ontology_url = exe_kg_namespaces_and_ontologies[chosen_exe_kg_type]

    input_data = pd.read_csv(
        r"data/singlefeatures_wm1.csv", delimiter=",", encoding="ISO-8859-1"
    )  # TODO: read data dynamically

    exe_kg = ExeKG(namespace_iri, ontology_url)
    # exe_kg.parse_ontology("https://raw.githubusercontent.com/baifanzhou/ExeKGOntology/main/ds_exeKGOntology.ttl")

    pipeline_iri, next_task_iri = exe_kg.get_pipeline_and_first_task_iri()
    canvas_method = None
    task_output_dict = {}
    while next_task_iri is not None:
        next_task = exe_kg.parse_task_by_iri(next_task_iri, canvas_method)
        output = next_task.run_method(task_output_dict,  input_data)
        if output:
            task_output_dict.update(output)
        # TODO: plot results of tasks for stats pipeline

        if next_task.type == "CanvasTask":
            canvas_method = next_task

        next_task_iri = next_task.has_next_task
