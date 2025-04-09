# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

import itertools
from pathlib import Path

from exe_kg_lib import ExeKGConstructor
from exe_kg_lib.config import KG_SCHEMAS
from exe_kg_lib.utils.query_utils import query_hierarchy_chain

HERE = Path(__file__).parent

OUTPUT_PATH = HERE / ".." / ".." / "docs" / "supported-tasks-and-methods.md"


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
        task_hierarchies_dict (dict): A dictionary representing the task hierarchy. Each key is a task IRI and each value is a dictionary (of the same structure) representing the sub-tasks of the key task.
        task_methods_dict (dict): A dictionary mapping task IRIs to their associated methods.
        task_inputs_dict (dict): A dictionary mapping task IRIs to their associated inputs.
        task_outputs_dict (dict): A dictionary mapping task IRIs to their associated outputs.
        method_params_dict (dict): A dictionary mapping method IRIs to their associated parameters.
        level (int, optional): The current level of the task hierarchy. Defaults to 0.
        top_task (str, optional): The top-level task in the hierarchy. Defaults to None.

    Returns:
        str: Markdown representation containing the hierarchy of tasks with their methods, inputs, outputs, and method parameters.
    """
    if level == 0:
        md_text = "🗒️ **Note**: Parent tasks are marked with 📜. Only bottom-level tasks (marked with ☑️) can be used while creating a pipeline.\n\n"
    else:
        md_text = ""

    for task_iri, sub_tasks_dict in task_hierarchies_dict.items():
        task_name = task_iri.split("#")[-1]

        kg_schema_short = ""
        for _, kg_schema_info in KG_SCHEMAS.items():
            if task_iri.startswith(kg_schema_info["namespace"]):
                kg_schema_short = kg_schema_info["namespace_prefix"]
                break

        kg_schema_short_text = (
            f'<span style="float: right; font-weight: 100;"> 🗒️ belongs to KG schema with abbr. <code>{kg_schema_short}</code></span>'
            if level == 0
            else ""
        )

        md_text += "\t" * level + f"<details>\n"

        if task_iri not in task_methods_dict:  # task is a subclass of ds:Task but not of ds:AtomicTask
            md_text += "\t" * (level + 1) + f"<summary>{task_name} 📜{kg_schema_short_text}</summary>\n"

            md_text += "\t" * (level + 1) + f"<ul>\n"

            # save top_task for getting the inputs/outputs
            if level == 0:
                top_task = task_iri
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
            md_text += "\t" * (level + 1) + f"<summary>{task_name} ☑️{kg_schema_short_text}</summary>\n"
            md_text += "\t" * (level + 1) + f"<ul>\n"

            if level == 0:
                top_task = task_iri

            # handle the inputs attached to the task
            md_text += "\t" * (level + 2) + f"<details>\n"
            md_text += "\t" * (level + 3) + f"<summary>Inputs</summary>\n"
            if top_task in task_inputs_dict:
                # check top task of the hierarchy
                # open the list
                md_text += "\t" * (level + 3) + f"<ul>\n"
                for input_iri in task_inputs_dict[top_task]:
                    input_name = input_iri.split("#")[-1]
                    md_text += "\t" * (level + 4) + f"<li>{input_name}</li>\n"

            if task_iri in task_inputs_dict and task_iri != top_task:
                # check current task (bottom of the hierarchy)
                if top_task not in task_inputs_dict:
                    # open the list
                    md_text += "\t" * (level + 3) + f"<ul>\n"
                for input_iri in task_inputs_dict[task_iri]:
                    input_name = input_iri.split("#")[-1]
                    md_text += "\t" * (level + 4) + f"<li>{input_name}</li>\n"

            if top_task in task_inputs_dict or (task_iri in task_inputs_dict and task_iri != top_task):
                # close the list
                md_text += "\t" * (level + 3) + f"</ul>\n"
            md_text += "\t" * (level + 2) + f"</details>\n"

            # handle the outputs attached to the task
            md_text += "\t" * (level + 2) + f"<details>\n"
            md_text += "\t" * (level + 3) + f"<summary>Outputs</summary>\n"
            if top_task in task_outputs_dict:
                # check top task of the hierarchy
                # open the list
                md_text += "\t" * (level + 3) + f"<ul>\n"
                for output_iri in task_outputs_dict[top_task]:
                    output_name = output_iri.split("#")[-1]
                    md_text += "\t" * (level + 4) + f"<li>{output_name}</li>\n"

            if task_iri in task_outputs_dict and task_iri != top_task:
                # check current task (bottom of the hierarchy)
                if top_task not in task_outputs_dict:
                    # open the list
                    md_text += "\t" * (level + 3) + f"<ul>\n"
                for output_iri in task_outputs_dict[task_iri]:
                    output_name = output_iri.split("#")[-1]
                    md_text += "\t" * (level + 4) + f"<li>{output_name}</li>\n"

            if top_task in task_outputs_dict or (task_iri in task_outputs_dict and task_iri != top_task):
                # close the list
                md_text += "\t" * (level + 3) + f"</ul>\n"

            md_text += "\t" * (level + 2) + f"</details>\n"

            # handle the methods attached to the task
            md_text += "\t" * (level + 2) + f"<details>\n"
            md_text += "\t" * (level + 3) + f"<summary>Methods</summary>\n"
            md_text += "\t" * (level + 3) + f"<ul>\n"
            for method_iri in task_methods_dict[task_iri]:
                method_name = method_iri.split("#")[-1]
                md_text += "\t" * (level + 3) + f"<details>\n"
                md_text += "\t" * (level + 4) + f"<summary>{method_name}</summary>\n"
                if method_iri in method_params_dict:
                    md_text += "\t" * (level + 4) + f"<ul>\n"
                    for param_iri, param_datatypes in method_params_dict[method_iri].items():
                        param_name = param_iri.split("#")[-1]
                        md_text += (
                            "\t" * (level + 5)
                            + f"<li>{param_name} ({', '.join([datatype.split('#')[-1] for datatype in param_datatypes])})</li>\n"
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
        task_iris = sorted(list({elem[0] for elem in property_tasks_methods}))
        method_iris = sorted([elem[1] for elem in property_tasks_methods])

        # store methods attached to each task
        for task_iri in task_iris:
            if task_iri not in task_methods_dict:
                task_methods_dict[task_iri] = []

            task_methods_dict[task_iri].extend(method_iris)

        # get and store task hierarchies
        for task_iri in task_iris:
            task_hierarchy_chain = list(query_hierarchy_chain(exekg.input_kg, task_iri))
            task_hierarchy_chain = [row[0] for row in task_hierarchy_chain]
            task_hierarchy_chain.remove(exekg.top_level_schema.namespace.AtomicTask)
            task_hierarchy_chain.remove(exekg.top_level_schema.namespace.Task)
            task_hierarchy_chain = [task_iri] + task_hierarchy_chain
            task_hierarchy_chain.reverse()

            curr_hierarchy_level = task_hierarchies_dict
            for task_iri in task_hierarchy_chain:
                if task_iri not in curr_hierarchy_level:
                    curr_hierarchy_level[task_iri] = {}
                curr_hierarchy_level = curr_hierarchy_level[task_iri]

    # get and store inputs attached to each task
    task_inputs_dict = {}
    for task_iri, input_iris in get_grouped_input_properties(exekg.input_kg):
        task_inputs_dict[task_iri] = sorted([input_iri for input_iri in input_iris])

    # get and store outputs attached to each task
    task_outputs_dict = {}
    for task_iri, output_iris in get_grouped_output_properties(exekg.input_kg):
        task_outputs_dict[task_iri] = sorted([output_iri for output_iri in output_iris])

    # get and store parameters attached to each method
    method_params_dict = {}
    grouped_parameter_properties = get_grouped_parameter_properties(exekg.input_kg)
    for property_iri, property_methods_datatypes in grouped_parameter_properties:
        method_iris = sorted(list({elem[0] for elem in property_methods_datatypes}))
        property_datatype_iris = sorted(list({elem[1] for elem in property_methods_datatypes}))

        for method_iri in method_iris:
            if method_iri not in method_params_dict:
                method_params_dict[method_iri] = {}

            method_params_dict[method_iri][property_iri] = [datatype_iri for datatype_iri in property_datatype_iris]

    # generate markdown
    markdown_text = task_hierarchy_to_md(
        task_hierarchies_dict, task_methods_dict, task_inputs_dict, task_outputs_dict, method_params_dict
    )
    with open(OUTPUT_PATH, "wb+") as f:
        f.write(markdown_text.encode("utf8"))
