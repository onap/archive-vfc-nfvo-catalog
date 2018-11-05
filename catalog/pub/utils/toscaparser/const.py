# Copyright 2018 ZTE Corporation.
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

NS_METADATA_SECTIONS = (NS_UUID, NS_INVARIANTUUID, NS_NAME, NS_VERSION, NS_DESIGNER, NSD_RELEASE_DATE) =\
    ("nsd_id", "nsd_invariant_id", "nsd_name", "nsd_file_structure_version", "nsd_designer", "nsd_release_date_time")
# ("id", "invariant_id", "name", "version", "designer", "description")

SDC_SERVICE_METADATA_SECTIONS = (SRV_UUID, SRV_INVARIANTUUID, SRV_NAME) = ('UUID', 'invariantUUID', 'name')

PNF_METADATA_SECTIONS = (PNF_UUID, PNF_INVARIANTUUID, PNF_NAME, PNF_METADATA_DESCRIPTION, PNF_VERSION, PNF_PROVIDER) = \
    ("descriptor_id", "descriptor_invariant_id", "name", "description", "version", "provider")
PNF_SECTIONS = (PNF_ID, PNF_METADATA, PNF_PROPERTIES, PNF_DESCRIPTION) = \
    ("pnf_id", "metadata", "properties", "description")

VNF_SECTIONS = (VNF_ID, VNF_METADATA, VNF_PROPERTIES, VNF_DESCRIPTION) = \
    ("vnf_id", "metadata", "properties", "description")

VL_SECTIONS = (VL_ID, VL_METADATA, VL_PROPERTIES, VL_DESCRIPTION) = \
    ("vl_id", "metadata", "properties", "description")
