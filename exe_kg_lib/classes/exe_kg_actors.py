# Copyright (c) 2022 Robert Bosch GmbH
# SPDX-License-Identifier: AGPL-3.0

from exe_kg_lib.classes.exe_kg_base import ExeKGBase
from exe_kg_lib.classes.exe_kg_mixins import (ExeKGConstructionCLIMixin,
                                              ExeKGConstructionMixin,
                                              ExeKGEditMixin,
                                              ExeKGExecutionMixin)


class ExeKGConstructor(ExeKGConstructionMixin, ExeKGBase):
    pass


class ExeKGConstructorCLI(ExeKGConstructionCLIMixin, ExeKGConstructionMixin, ExeKGBase):
    pass


class ExeKGExecutor(ExeKGExecutionMixin, ExeKGBase):
    pass


class ExeKGConExe(ExeKGConstructionMixin, ExeKGExecutionMixin, ExeKGBase):
    pass


class ExeKGEditor(ExeKGEditMixin, ExeKGConstructionMixin, ExeKGBase):
    pass
