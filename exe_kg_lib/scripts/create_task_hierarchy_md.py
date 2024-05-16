import itertools
from pathlib import Path

from exe_kg_lib import ExeKGConstructor
from exe_kg_lib.utils.query_utils import query_hierarchy_chain

HERE = Path(__file__).parent

OUTPUT_PATH = HERE / ".." / ".." / "task_hierarchy.md"


def query_has_method_properties(g):
    return g.query(
        """SELECT ?property ?task ?method
            WHERE {
                ?property rdfs:domain ?task ;
                          rdfs:range ?method ;
                          rdfs:subPropertyOf+ ds:hasMethod .
            }"""
    )


def query_has_parameter_properties(g):
    return g.query(
        """SELECT ?property ?method ?datatype
            WHERE {
                ?property rdfs:domain ?method ;
                          rdfs:range ?datatype ;
                          rdfs:subPropertyOf+ ds:hasParameter .
            }"""
    )


def query_has_input_properties(g):
    return g.query(
        """SELECT ?task ?input
            WHERE {
                ?property rdfs:domain ?task ;
                          rdfs:range ?input ;
                          rdfs:subPropertyOf+ ds:hasInput .
            }"""
    )


def query_has_output_properties(g):
    return g.query(
        """SELECT ?task ?output
            WHERE {
                ?property rdfs:domain ?task ;
                          rdfs:range ?output ;
                          rdfs:subPropertyOf+ ds:hasOutput .
            }"""
    )


def get_grouped_method_properties(g):
    properties = list(query_has_method_properties(g))
    properties = sorted(properties, key=lambda elem: elem[0])
    properties = [
        (key, [(elem[1], elem[2]) for elem in group])
        for key, group in itertools.groupby(properties, lambda elem: elem[0])
    ]
    return properties


def get_grouped_parameter_properties(g):
    properties = list(query_has_parameter_properties(g))
    properties = sorted(properties, key=lambda elem: elem[0])
    properties = [
        (key, [(elem[1], elem[2]) for elem in group])
        for key, group in itertools.groupby(properties, lambda elem: elem[0])
    ]
    return properties


def get_grouped_input_properties(g):
    properties = list(query_has_input_properties(g))
    properties = sorted(properties, key=lambda elem: elem[0])
    properties = [
        (key, [elem[1] for elem in group]) for key, group in itertools.groupby(properties, lambda elem: elem[0])
    ]
    return properties


def get_grouped_output_properties(g):
    properties = list(query_has_output_properties(g))
    properties = sorted(properties, key=lambda elem: elem[0])
    properties = [
        (key, [elem[1] for elem in group]) for key, group in itertools.groupby(properties, lambda elem: elem[0])
    ]
    return properties


def task_hierarchy_to_md(
    task_hierarchies_dict,
    task_methods_dict,
    task_inputs_dict,
    task_outputs_dict,
    method_params_dict,
    level=0,
    top_task=None,
):
    """
    Convert input dictionaries into a markdown representation.

    Args:
        task_hierarchies_dict (dict): A dictionary representing the task hierarchy.
        task_methods_dict (dict): A dictionary mapping task names to their associated methods.
        task_inputs_dict (dict): A dictionary mapping task names to their associated inputs.
        task_outputs_dict (dict): A dictionary mapping task names to their associated outputs.
        method_params_dict (dict): A dictionary mapping method names to their associated parameters.
        level (int, optional): The current level of the task hierarchy. Defaults to 0.
        top_task (str, optional): The top-level task in the hierarchy. Defaults to None.

    Returns:
        str: Markdown representation containing the hierarchy of tasks with their methods, inputs, outputs, and method parameters.
    """
    if level == 0:
        md_text = "### Hierarchy of supported tasks with their methods\n\n🗒️ **Note**: Only bottom-level tasks (marked with ☑️) can be used while creating a pipeline. Other tasks are marked with 📜.\n\n"
    else:
        md_text = ""

    for task_name, sub_tasks_dict in task_hierarchies_dict.items():
        md_text += "\t" * level + f"<details>\n"

        if task_name not in task_methods_dict:  # task is a subclass of ds:Task but not of ds:AtomicTask
            md_text += "\t" * (level + 1) + f"<summary>{task_name} 📜</summary>\n"
            md_text += "\t" * (level + 1) + f"<ul>\n"

            # save top_task for getting the inputs/outputs
            if level == 0:
                top_task = task_name
            # handle the rest of the tasks in the hierarchy
            md_text += task_hierarchy_to_md(
                sub_tasks_dict,
                task_methods_dict,
                task_inputs_dict,
                task_outputs_dict,
                method_params_dict,
                level + 2,
                top_task,
            )
        else:  # task has methods attached i.e. task is a subclass of ds:AtomicTask
            md_text += "\t" * (level + 1) + f"<summary>{task_name} ☑️</summary>\n"
            md_text += "\t" * (level + 1) + f"<ul>\n"

            if level == 0:
                top_task = task_name

            # handle the inputs attached to the task
            md_text += "\t" * (level + 2) + f"<details>\n"
            md_text += "\t" * (level + 3) + f"<summary>Inputs</summary>\n"
            if top_task in task_inputs_dict:
                md_text += "\t" * (level + 3) + f"<ul>\n"
                for input_name in task_inputs_dict[top_task]:
                    md_text += "\t" * (level + 4) + f"<li>{input_name}</li>\n"
                md_text += "\t" * (level + 3) + f"</ul>\n"
            md_text += "\t" * (level + 2) + f"</details>\n"

            # handle the outputs attached to the task
            md_text += "\t" * (level + 2) + f"<details>\n"
            md_text += "\t" * (level + 3) + f"<summary>Outputs</summary>\n"
            if top_task in task_outputs_dict:
                md_text += "\t" * (level + 3) + f"<ul>\n"
                for output_name in task_outputs_dict[top_task]:
                    md_text += "\t" * (level + 4) + f"<li>{output_name}</li>\n"
                md_text += "\t" * (level + 3) + f"</ul>\n"
            md_text += "\t" * (level + 2) + f"</details>\n"

            # handle the methods attached to the task
            md_text += "\t" * (level + 2) + f"<details>\n"
            md_text += "\t" * (level + 3) + f"<summary>Methods</summary>\n"
            md_text += "\t" * (level + 3) + f"<ul>\n"
            for method_name in task_methods_dict[task_name]:
                md_text += "\t" * (level + 3) + f"<details>\n"
                md_text += "\t" * (level + 4) + f"<summary>{method_name}</summary>\n"
                if method_name in method_params_dict:
                    md_text += "\t" * (level + 4) + f"<ul>\n"
                    for param_name, param_datatypes in method_params_dict[method_name].items():
                        md_text += (
                            "\t" * (level + 5)
                            + f"<li>{param_name} ({', '.join([datatype for datatype in param_datatypes])})</li>\n"
                        )
                    md_text += "\t" * (level + 4) + f"</ul>\n"
                else:
                    md_text += "\t" * (level + 4) + f"<ul>No parameters</ul>\n"
                md_text += "\t" * (level + 3) + f"</details>\n"
            md_text += "\t" * (level + 3) + f"</ul>\n"
            md_text += "\t" * (level + 2) + f"</details>\n"
        md_text += "\t" * (level + 1) + f"</ul>\n"

        md_text += "\t" * level + f"</details>\n"
    return md_text


if __name__ == "__main__":
    exekg = ExeKGConstructor()

    task_hierarchies_dict = {}
    task_methods_dict = {}  # stores methods attached to each task
    grouped_method_properties = get_grouped_method_properties(exekg.input_kg)
    for property_iri, property_tasks_methods in grouped_method_properties:
        property_name = property_iri.split("#")[-1]

        property_task_iris = sorted(list({elem[0] for elem in property_tasks_methods}))
        property_method_iris = sorted([elem[1] for elem in property_tasks_methods])

        property_task_names = [iri.split("#")[-1] for iri in property_task_iris]
        property_method_names = [iri.split("#")[-1] for iri in property_method_iris]

        # store methods attached to each task
        for task_name in property_task_names:
            if task_name not in task_methods_dict:
                task_methods_dict[task_name] = []

            task_methods_dict[task_name].extend(property_method_names)

        # get and store task hierarchies
        for task_iri in property_task_iris:
            task_hierarchy_chain = list(query_hierarchy_chain(exekg.input_kg, task_iri))
            task_hierarchy_chain = [str(row[0]).split("#")[-1] for row in task_hierarchy_chain]
            task_hierarchy_chain.remove("AtomicTask")
            task_hierarchy_chain.remove("Task")
            task_hierarchy_chain = [task_iri.split("#")[-1]] + task_hierarchy_chain
            task_hierarchy_chain.reverse()

            curr_hierarchy_level = task_hierarchies_dict
            for task_iri in task_hierarchy_chain:
                if task_iri not in curr_hierarchy_level:
                    curr_hierarchy_level[task_iri] = {}
                curr_hierarchy_level = curr_hierarchy_level[task_iri]

    # get and store inputs attached to each task
    task_inputs_dict = {}
    for task_iri, input_iris in get_grouped_input_properties(exekg.input_kg):
        task_name = task_iri.split("#")[-1]
        task_inputs_dict[task_name] = sorted([input_iri.split("#")[-1] for input_iri in input_iris])

    # get and store outputs attached to each task
    task_outputs_dict = {}
    for task_iri, output_iris in get_grouped_output_properties(exekg.input_kg):
        task_name = task_iri.split("#")[-1]
        task_outputs_dict[task_name] = sorted([output_iri.split("#")[-1] for output_iri in output_iris])

    # get and store parameters attached to each method
    method_params_dict = {}
    grouped_parameter_properties = get_grouped_parameter_properties(exekg.input_kg)
    for property_iri, property_methods_datatypes in grouped_parameter_properties:
        property_name = property_iri.split("#")[-1]

        property_method_iris = sorted(list({elem[0] for elem in property_methods_datatypes}))
        property_datatype_iris = sorted(list({elem[1] for elem in property_methods_datatypes}))

        for method_iri in property_method_iris:
            method_name = method_iri.split("#")[-1]

            if method_name not in method_params_dict:
                method_params_dict[method_name] = {}

            method_params_dict[method_name][property_name] = [
                datatype_iri.split("#")[-1] for datatype_iri in property_datatype_iris
            ]

    # generate markdown
    markdown_text = task_hierarchy_to_md(
        task_hierarchies_dict, task_methods_dict, task_inputs_dict, task_outputs_dict, method_params_dict
    )
    with open(OUTPUT_PATH, "wb+") as f:
        f.write(markdown_text.encode("utf8"))
