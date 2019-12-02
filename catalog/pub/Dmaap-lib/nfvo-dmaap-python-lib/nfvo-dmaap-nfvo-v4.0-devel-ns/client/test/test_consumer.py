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

import base64
import datetime
import hmac
import unittest
from _sha1 import sha1

from dmaap.consumer import ConsumerClient


class CreateApiKeyTest(unittest.TestCase):
    def setUp(self):
        self.apiKey = "7TuwzpLJ4QfQs4O"
        self.apiSecret = "7TuwzpLJ4QfQs4O"
        self.host = '127.0.0.1'
        self.topic = 'abc'
        self.group = 'def'
        self.comsumer_id = '123'
        self.timeout_ms = 3
        self.limit = 3
        self.filter = 'test'

    def tearDown(self):
        self.ret_url = ""

    def test_create_url(self):
        exp_url = 'http://127.0.0.1/events/abc/def/123'
        consumer = ConsumerClient(self.host, self.topic, self.group, self.comsumer_id)
        ret_url = consumer.create_url()
        self.assertEqual(exp_url, ret_url)

    def test_create_timeout_url(self):
        exp_url = 'http://127.0.0.1/events/abc/def/123?timeout=3'
        consumer = ConsumerClient(self.host, self.topic, self.group, self.comsumer_id, self.timeout_ms)
        ret_url = consumer.create_url()
        self.assertEqual(exp_url, ret_url)

    def test_create_limit_url(self):

        exp_url = 'http://127.0.0.1/events/abc/def/123?timeout=3&limit=3'
        consumer = ConsumerClient(self.host, self.topic, self.group, self.comsumer_id,
                                  self.timeout_ms, self.limit)
        ret_url = consumer.create_url()
        self.assertEqual(exp_url, ret_url)

    def test_create_filter_url(self):

        exp_url = "http://127.0.0.1/events/abc/def/123?timeout=3&limit=3&filter=b'test'"
        consumer = ConsumerClient(self.host, self.topic, self.group, self.comsumer_id,
                                  self.timeout_ms, self.limit, self.filter)
        ret_url = consumer.create_url()
        self.assertEqual(exp_url, ret_url)

    def test_create_headers(self):
        data = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + '-04:00'
        hmac_code = hmac.new(self.apiSecret.encode(), data.encode(), sha1).digest()
        signature = base64.b64encode(hmac_code).decode()
        auth = self.apiKey + ':' + signature
        exp_headers = {
            'X-CambriaDate': data,
            'X-CambriaAuth': auth
        }

        consumer = ConsumerClient(self.host, self.topic, self.group, self.comsumer_id,
                                  self.timeout_ms, self.limit, self.filter, self.apiKey, self.apiSecret)
        consumer.set_api_credentials(self.apiKey, self.apiSecret)
        rea_headers = consumer.create_headers()
        self.assertEqual(exp_headers, rea_headers)
