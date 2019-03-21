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

from django.test import TestCase, Client
from rest_framework import status

from catalog.packages.biz.sdc_service_package import ServicePackage
from catalog.pub.database.models import ServicePackageModel
from catalog.pub.exceptions import PackageNotFoundException, PackageHasExistsException


class TestServicePackage(TestCase):
    """ Test case for Service Package operations"""

    def setUp(self):
        self.client = Client()
        ServicePackageModel.objects.filter().delete()

    def tearDown(self):
        pass

    ###############################################################

    def test_service_pkg_distribute_when_pkg_exists(self):
        ServicePackageModel(servicePackageId="1", servicedId="2").save()
        csar_id = 1
        try:
            ServicePackage().on_distribute(csar_id)
        except PackageHasExistsException as e:
            self.assertEqual("Service CSAR(1) already exists.", e.message)

    def test_api_service_pkg_distribute_when_pkg_exists(self):
        ServicePackageModel(servicePackageId="1", servicedId="2").save()
        resp = self.client.post(
            "/api/parser/v1/service_packages", {"csarId": "1"}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("Service CSAR(1) already exists.", resp.data["errorMessage"])

    ###############################################################
    def test_service_pkg_get_all(self):
        ServicePackageModel(
            servicePackageId="13",
            servicedId="2",
            servicedDesigner="2",
            servicedVersion="2",
            servicePackageUri="13.csar",
            servicedModel="").save()
        ServicePackageModel(
            servicePackageId="14",
            servicedId="3",
            servicedDesigner="3",
            servicedVersion="3",
            servicePackageUri="14.csar",
            servicedModel="").save()
        csars = ServicePackage().get_csars()
        self.assertEqual(2, len(csars))

    def test_api_service_pkg_get_all(self):
        ServicePackageModel(
            servicePackageId="13",
            servicedId="2",
            servicedDesigner="2",
            servicedVersion="2",
            servicePackageUri="13.csar",
            servicedModel="").save()
        ServicePackageModel(
            servicePackageId="14",
            servicedId="3",
            servicedDesigner="3",
            servicedVersion="3",
            servicePackageUri="14.csar",
            servicedModel="").save()
        resp = self.client.get("/api/parser/v1/service_packages")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    ###############################################################

    def test_service_pkg_get_one(self):
        ServicePackageModel(
            servicePackageId="14",
            servicedId="2",
            servicedDesigner="3",
            servicedVersion="4",
            servicePackageUri="14.csar",
            servicedModel="").save()
        csar = ServicePackage().get_csar(14)
        self.assertEqual(14, csar['csarId'])

    def test_service_pkg_get_one_not_found(self):
        try:
            ServicePackage().get_csar(1000)
        except PackageNotFoundException as e:
            self.assertEqual("Service package[1000] not Found.", e.message)

    def test_api_service_pkg_get_one(self):
        ServicePackageModel(
            servicePackageId="14",
            servicedId="2",
            servicedDesigner="3",
            servicedVersion="4",
            servicePackageUri="14.csar",
            servicedModel="").save()
        resp = self.client.get("/api/parser/v1/service_packages/14")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_api_service_pkg_get_one_not_found(self):
        resp = self.client.get("/api/parser/v1/service_packages/22")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            {"errorMessage": "Service package[22] not Found.", 'error': 404},
            resp.data)

    ###############################################################

    def test_service_pkg_normal_delete(self):
        ServicePackageModel(servicePackageId="8", servicedId="2").save()
        sp = ServicePackageModel.objects.filter(servicePackageId=8)
        self.assertEqual(1, len(sp))
        ServicePackage().delete_csar("8")
        sp = ServicePackageModel.objects.filter(servicePackageId=8)
        self.assertEqual(0, len(sp))

    def test_service_pkg_normal_delete_not_found(self):
        try:
            ServicePackage().delete_csar("8000")
        except PackageNotFoundException as e:
            self.assertEqual("Service package[8000] not Found.", e.message)

    def test_api_service_pkg_normal_delete(self):
        ServicePackageModel(servicePackageId="8", servicedId="2").save()
        resp = self.client.delete("/api/parser/v1/service_packages/8")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
