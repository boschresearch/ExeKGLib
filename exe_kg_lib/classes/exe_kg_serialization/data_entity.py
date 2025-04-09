# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0


class DataEntity:
    """
    Represents a simplified version of a data entity for serialization purposes.
    """

    def __init__(self, name: str = "", source: str = "", data_semantics: str = "", data_structure: str = ""):
        self.name = name
        self.source = source
        self.data_semantics = data_semantics
        self.data_structure = data_structure
