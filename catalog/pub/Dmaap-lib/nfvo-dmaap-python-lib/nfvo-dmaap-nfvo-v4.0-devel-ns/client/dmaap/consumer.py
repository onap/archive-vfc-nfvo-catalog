# Copyright (c) 2019, CMCC Technologies Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import base64
import hmac
import json
import logging
import datetime
import requests
from hashlib import sha1

from client.pub.exceptions import DmaapClientException

logger = logging.getLogger(__name__)


class ConsumerClient:
    def __init__(self, host, topic, consumer_group, consumer_id, timeout_ms=-1, limit=-1, filter=''):
        self.host = host
        self.topic = topic
        self.group = consumer_group
        self.comsumer_id = consumer_id
        self.timeout_ms = timeout_ms
        self.limit = limit
        self.filter = filter

    def set_api_credentials(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def create_url(self):
        url = "http://%s/events/%s/%s/%s" % (self.host, self.topic, self.group, self.comsumer_id)
        add_url = ""
        if self.timeout_ms > -1:
            add_url += "timeout=%s" % self.timeout_ms
        if self.limit > -1:
            if add_url:
                add_url += "&"
            add_url += "limit=%s" % self.limit
        if self.filter:
            if add_url:
                add_url += "&"
            add_url += "filter=%s" % self.filter.encode("utf-8")
        if add_url:
            url = url + "?" + add_url

        return url

    def create_headers(self):
        data = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + '-04:00'
        hmac_code = hmac.new(self.api_secret.encode(), data.encode(), sha1).digest()
        signature = base64.b64encode(hmac_code).decode()
        auth = self.api_key + ':' + signature
        headers = {
            'X-CambriaDate': data,
            'X-CambriaAuth': auth
        }
        return headers

    def fetch(self):
        try:
            msgs = []
            url = self.create_url()
            if self.api_key:
                headers = self.create_headers()
                ret = requests.get(url=url, headers=headers)
            else:
                ret = requests.get(url)
            logger.info("Status code is %s, detail is %s.", ret.status_code, ret.json())
            if ret.status_code != 200:
                raise DmaapClientException('Call dmaap failed. Status code is %s, detail is %s.' % (ret.status_code, ret.json()))
            data = ret.json()
            for msg in data:
                msg = json.loads(msg)
                msgs.append(msg)
            return msgs
        except Exception as e:
            raise DmaapClientException(e.message)
