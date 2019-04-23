# Copyright 2019 ZTE Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from catalog.pub.utils.toscaparser.vnfdparser.vnfd_sol_base import VnfdSOLBase
from catalog.pub.utils.toscaparser.vnfdparser.vnfd_sol_251 import VnfdSOL251


def CreateVnfdSOLParser(sol_version, etsi_vnfd_model):
    switcher = {
        "base": VnfdSOLBase(etsi_vnfd_model),
        "2.5.1": VnfdSOL251(etsi_vnfd_model)
    }
    return switcher.get(sol_version, lambda: "Invalid Version")
