# Copyright (C) 2019 Verizon. All Rights Reserved
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

import logging

from catalog.pub.database.models import VnfPackageModel
from catalog.pub.exceptions import ResourceNotFoundException, ArtifactNotFoundException
from catalog.pub.utils import fileutil

logger = logging.getLogger(__name__)


class FetchVnfPkgArtifact(object):
    def fetch(self, vnfPkgId, artifactPath):
        logger.debug("FetchVnfPkgArtifact--get--single--artifact--biz::>"
                     "ID: %s path: %s" % (vnfPkgId, artifactPath))
        vnf_pkg = VnfPackageModel.objects.filter(vnfPackageId=vnfPkgId)
        if not vnf_pkg.exists():
            err_msg = "NF Package (%s) doesn't exists." % vnfPkgId
            raise ResourceNotFoundException(err_msg)
        vnf_pkg = vnf_pkg.get()
        local_path = vnf_pkg.localFilePath
        if local_path.endswith(".csar") or local_path.endswith(".zip"):
            vnf_extract_path = fileutil.unzip_csar_to_tmp(local_path)
            artifact_path = fileutil.get_artifact_path(vnf_extract_path, artifactPath)
            if not artifact_path:
                raise ArtifactNotFoundException("Couldn't artifact %s" % artifactPath)
            with open(artifact_path, 'rb') as f:
                file_content = f.read()
        else:
            raise ArtifactNotFoundException("NF Package format is not csar or zip")
        return file_content
