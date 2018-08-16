# Copyright 2017 ZTE Corporation.
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

# Micro service of nfvo catalog.

1. Code structure guide
   ./         project files
   ./docker   docker related scripts
   ./logs     log file
   ./catalog  catalog management
       ./packages      package life cycle API& logic
             ./               API url definition
             ./views          API related views, each operation is a view
             ./serializers    API related request and response parametes.
                              Suggest related to sol003/sol005, each datatype is a file.
                              Common datatypes are put into the common file
             ./biz            Package mangement busyness logic files
             ./tests          All the test case. At least each API should have a test case
       ./jobs      Related job
       ./pub       Common class, including database, external micro service API, utils, and config parameters.
       ./samples   Catalog micro service health check
       ./swagger   Auto-generate catalog swagger json or yaml files
   ./static/catalog  package storage
