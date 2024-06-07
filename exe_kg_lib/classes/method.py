# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

import importlib
from typing import Any, Dict, List, Union

from exe_kg_lib.classes.entity import Entity
from exe_kg_lib.utils.string_utils import camel_to_snake


class Method(Entity):
    """
    Abstraction of owl:class ds:AtomicMethod.

    ❗ Important for contributors: See Section "Naming conventions" in README.md of "classes.tasks" package before extending the code's functionality.
    """

    def __init__(
        self,
        iri: str,
        parent_entity: Entity,
        module_chain: List[str] = None,
        params_dict: Dict[str, Union[str, int, float]] = None,
        inherited_params_dict: Dict[str, Union[str, int, float]] = None,
    ):
        super().__init__(iri, parent_entity)

        if module_chain is None:
            module_chain = []
        self.module_chain = module_chain  # e.g. ['sklearn','model_selection', 'StratifiedShuffleSplit'] Used for resolving the Python module that contains the method to be executed

        if params_dict is None:
            params_dict = {}
        self.params_dict = params_dict  # used for storing method parameters during KG execution

        if inherited_params_dict is None:
            inherited_params_dict = {}
        self.inherited_params_dict = {}  # used for storing inherited method parameters during KG execution

    def resolve_module(self, module_name_to_snakecase=False) -> Any:
        """
        Resolves and returns the Python module specified by the method module chain.

        Args:
            module_name_to_snakecase (bool, optional): Whether to convert the last module name to snake case.
                                                      Defaults to False.

        Returns:
            Any: The resolved module.

        Raises:
            NotImplementedError: If the method module chain is not defined for the task.
        """
        if not self.module_chain:
            raise NotImplementedError(f"Method module chain not defined for task {self.name}.")

        module_chain = self.module_chain
        if module_name_to_snakecase:
            module_chain = self.module_chain[:-1] + [camel_to_snake(self.module_chain[-1])]

        module_chain_parents = ".".join(module_chain[:-1])
        module_chain_child = module_chain[-1]
        module_container = importlib.import_module(module_chain_parents)
        module = getattr(module_container, module_chain_child)
        return module
