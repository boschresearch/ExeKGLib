# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from typing import Dict, Union


class Method:
    """
    Represents a simplified version of a method for serialization purposes.
    """

    def __init__(self, method_type: str, params_dict: Dict[str, Union[str, int, float, dict]]):
        self.method_type = method_type
        self.params_dict = params_dict
