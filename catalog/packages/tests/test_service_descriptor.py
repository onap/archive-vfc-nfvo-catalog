# Copyright (c) 2019, CMCC Technologies. Co., Ltd.
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
import json
import logging

from django.test import TestCase
from mock import mock

from catalog.packages.biz.service_descriptor import ServiceDescriptor
from catalog.packages.const import PKG_STATUS
from catalog.pub.database.models import ServicePackageModel, VnfPackageModel, PnfPackageModel
from catalog.pub.exceptions import PackageNotFoundException
from catalog.pub.utils import toscaparser
from .const import sd_data

logger = logging.getLogger(__name__)


class TestServiceDescription(TestCase):

    def setUp(self):
        self.user_defined_data = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3',
        }
        self.data = {
            'userDefinedData': self.user_defined_data,
        }
        self.sd_data = sd_data
        ServicePackageModel.objects.filter().delete()

    def tearDown(self):
        pass

    def test_create(self):
        result_data = ServiceDescriptor().create(self.data)
        self.assertIsNotNone(result_data['id'])
        service_package = ServicePackageModel.objects.filter(servicePackageId=result_data['id'])[0]
        self.assertIsNotNone(service_package)
        self.assertEqual(PKG_STATUS.DISABLED, service_package.operationalState)
        self.assertEqual(PKG_STATUS.CREATED, service_package.onboardingState)
        self.assertEqual(PKG_STATUS.NOT_IN_USE, service_package.usageState)

    def test_create_with_csarid(self):
        csar_id = '0b667470-e6b3-4ee8-8f08-186317a04dc2'
        result_data = ServiceDescriptor().create(self.data, csar_id)
        self.assertEqual(csar_id, result_data['id'])
        service_package = ServicePackageModel.objects.filter(servicePackageId=csar_id)[0]
        self.assertIsNotNone(service_package)
        self.assertEqual(PKG_STATUS.DISABLED, service_package.operationalState)
        self.assertEqual(PKG_STATUS.CREATED, service_package.onboardingState)
        self.assertEqual(PKG_STATUS.NOT_IN_USE, service_package.usageState)

    @mock.patch.object(toscaparser, 'parse_sd')
    def test_parse_serviced_and_save(self, mock_parse_sd):
        mock_parse_sd.return_value = json.JSONEncoder().encode(self.sd_data)
        servcie_desc = ServiceDescriptor()
        csar_id = '0b667470-e6b3-4ee8-8f08-186317a04dc2'
        servcie_desc.create(self.data, csar_id)
        VnfPackageModel(vnfPackageId="1", vnfdId="cd557883-ac4b-462d-aa01-421b5fa606b1").save()
        PnfPackageModel(pnfPackageId="1", pnfdId="m6000_s").save()
        local_file_name = "/test.csar"
        servcie_desc.parse_serviced_and_save(csar_id, local_file_name)

        service_package = ServicePackageModel.objects.filter(servicePackageId=csar_id)[0]
        self.assertIsNotNone(service_package)

    def test_delete_single(self):
        servcie_desc = ServiceDescriptor()
        csar_id = '0b667470-e6b3-4ee8-8f08-186317a04dc2'
        servcie_desc.create(self.data, csar_id)

        servcie_desc.delete_single(csar_id)
        self.assertTrue(len(ServicePackageModel.objects.filter(servicePackageId=csar_id)) == 0)
        self.assertFalse(ServicePackageModel.objects.filter(servicePackageId=csar_id).exists())

    def test_delete_single_not_exists(self):
        csar_id = "8000"
        try:
            ServiceDescriptor().delete_single(csar_id)
        except Exception as e:
            self.assertTrue(isinstance(e, PackageNotFoundException))
            self.assertEqual("Service package[8000] not Found.", e.message)
