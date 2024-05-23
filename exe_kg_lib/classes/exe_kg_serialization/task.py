from typing import Dict, List, Union


class Task:
    """
    Represents a simplified version of a pipeline's task for serialization purposes.
    """

    def __init__(
        self,
        kg_schema_short: str,
        task_type: str,
        method_type: str,
        method_params_dict: Dict[str, Union[str, int, float]],
        output_names: List[str],
    ):
        self.kg_schema_short = kg_schema_short
        self.task_type = task_type
        self.method_type = method_type
        self.method_params_dict = method_params_dict
        self.input_data_entity_dict: Dict[
            str, List[str]
        ] = {}  # contains input names as keys and lists of data entity names as values
        self.output_names = output_names
