from classes.pipeline_execution import PipelineProcessor
from utils import parse_entity, execute_tasks


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
        visualizer.graph if (visualizer) else statistics_analyzer.graph if (statistics_analyzer) else ML_analyser.graph
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

        start_po = parse_entity(graph, pipeline_po["exeKG:hasStartTask"][0], dict_namespace)
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
