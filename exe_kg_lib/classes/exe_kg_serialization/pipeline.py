# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

import json
import os
from io import TextIOWrapper
from pathlib import Path
from typing import Dict, List, Union

from exe_kg_lib.classes.data_entity import DataEntity
from exe_kg_lib.classes.exe_kg_serialization.data_entity import \
    DataEntity as DataEntitySerializable
from exe_kg_lib.classes.exe_kg_serialization.method import \
    Method as MethodSerializable
from exe_kg_lib.classes.exe_kg_serialization.task import \
    Task as TaskSerializable
from exe_kg_lib.classes.method import Method


class Pipeline:
    """
    Represents a simplified version of a pipeline for serialization purposes. Can be converted to and from JSON.
    """

    def __init__(
        self,
        name: str = "",
        input_data_path: str = "",
        output_plots_dir: str = "",
        data_entities: List[DataEntitySerializable] = None,
        tasks: List[TaskSerializable] = None,
    ):
        """
        Initializes a Pipeline object.

        Args:
            name (str): The name of the pipeline.
            input_data_path (str): The path to the input dataset.
            output_plots_dir (str): The directory to save output plots.
            data_entities (List[DataEntitySerializable]): A list of data entities.
            tasks (List[TaskSerializable]): A list of tasks.
        """
        self.name = name
        self.input_data_path = input_data_path
        self.output_plots_dir = output_plots_dir

        if data_entities is None:
            data_entities = []
        self.data_entities = data_entities

        if tasks is None:
            tasks = []
        self.tasks = tasks

    @classmethod
    def from_json(cls, source: Union[Path, TextIOWrapper, str]):
        """
        Deserializes a JSON source and creates an instance of the class.

        Args:
            source (Union[Path, TextIOWrapper, str]): The JSON source containing the pipeline.

        Returns:
            cls: An instance of the class with the deserialized data.
        """
        obj_dict = None
        try:
            # if source is a path
            if isinstance(source, TextIOWrapper):
                obj_dict = json.load(source)
            elif isinstance(source, Path) or Path(str(source)).exists():
                with open(source) as file:
                    obj_dict = json.load(file)
        except OSError:
            pass

        if obj_dict is None and isinstance(source, str):
            obj_dict = json.loads(source)

        if obj_dict is None:
            raise ValueError("Invalid source type. Must be a valid Path, TextIOWrapper, or str.")

        data_entities = []
        for data_entity_dict in obj_dict["data_entities"]:
            data_entity = DataEntitySerializable()
            data_entity.__dict__ = data_entity_dict
            data_entities.append(data_entity)

        tasks = []
        for task_dict in obj_dict["tasks"]:
            task = TaskSerializable.from_dict(task_dict)
            tasks.append(task)

        return cls(obj_dict["name"], obj_dict["input_data_path"], obj_dict["output_plots_dir"], data_entities, tasks)

    def to_json(self) -> str:
        """
        Converts the Pipeline object to a JSON string.

        Returns:
            str: The JSON representation of the Pipeline object.
        """
        obj_dict = self.__dict__
        obj_dict["data_entities"] = [data_entity.__dict__ for data_entity in self.data_entities]
        obj_dict["tasks"] = [task.to_dict() for task in self.tasks]
        return json.dumps(obj_dict, indent=4)

    def add_data_entity(self, name: str, source_value: str, data_semantics_name: str, data_structure_name: str):
        """
        Adds a data entity to the pipeline.

        Args:
            name (str): The name of the data entity.
            source_value (str): The source value of the data entity (i.e. column of the input dataset).
            data_semantics_name (str): The name of the data semantics.
            data_structure_name (str): The name of the data structure.
        """
        data_entity_ser = DataEntitySerializable(name, source_value, data_semantics_name, data_structure_name)

        self.data_entities.append(data_entity_ser)

    def add_task(
        self,
        kg_schema_short: str,
        task_type: str,
        method_type: str,
        method_params_dict: Dict[str, Union[str, int, float, dict]],
        input_entity_dict: Dict[str, Union[List[DataEntity], Method]],
        output_names: List[str],
    ):
        """
        Adds a task to the pipeline.

        Args:
            kg_schema_short (str): The short name of the KG schema (e.g. "ml" for Machine Learning).
            task_type (str): The type of the task.
            method_type (str): The type of the method.
            method_params_dict (Dict[str, Union[str, int, float]]): A dictionary of method parameters.
            input_entity_dict (Dict[str, Union[List[DataEntity], Method]]): A dictionary of input data entities.
            output_names (List[str]): A list of output names.
        """
        task_ser = TaskSerializable(kg_schema_short, task_type, method_type, method_params_dict, output_names)

        for input_entity_name, input_entity_value in input_entity_dict.items():
            if isinstance(input_entity_value, Method):  # provided input is a method
                input_method = input_entity_value

                task_ser.input_entity_info_dict[input_entity_name] = MethodSerializable(
                    input_method.name, input_method.params_dict
                )
            elif isinstance(input_entity_value, list) and all(
                isinstance(elem, DataEntity) for elem in input_entity_value
            ):  # provided input is list of data entities
                input_data_entity_list = input_entity_value
                input_data_entity_names = []
                for input_data_entity in input_data_entity_list:
                    input_data_entity_names.append(input_data_entity.name)

                task_ser.input_entity_info_dict[input_entity_name] = input_data_entity_names

        self.tasks.append(task_ser)
