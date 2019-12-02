# Copyright (c) 2019, CMCC Technologies Co., Ltd.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import mock

from dmaap.identity import IdentityClient


class CreateApiKeyTest(unittest.TestCase):
    def setUp(self):
        self.apiKey = "7TuwzpLJ4QfQs4O"
        self.apiSecret = "7TuwzpLJ4QfQs4O"
        self.host = '127.0.0.1'

    def tearDown(self):
        self.ret_url = ""

    @mock.patch.object(IdentityClient, 'create_apikey')
    def test_create_apiKey(self, mock_create_apikey):
        mock_create_apikey.return_value = {
            'apiKey': "7TuwzpLJ4QfQs4O",
            'apiSecret': "7TuwzpLJ4QfQs4O"
        }
        resp_data = IdentityClient(self.host).create_apikey('', 'description')
        self.assertEqual(self.apiKey, resp_data.get("apiKey"))
        self.assertEqual(self.apiSecret, resp_data.get("apiSecret"))
