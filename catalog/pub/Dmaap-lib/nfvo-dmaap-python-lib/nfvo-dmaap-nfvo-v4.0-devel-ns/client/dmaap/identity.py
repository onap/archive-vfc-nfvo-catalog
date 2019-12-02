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


import json
import logging
import requests

from client.pub.exceptions import DmaapClientException

logger = logging.getLogger(__name__)


class IdentityClient:
    def __init__(self, host):
        self.host = host

    def create_apikey(self, email, description):
        try:
            headers = {'content-type': 'application/json;charset=UTF-8'}
            data = {
                'email': email,
                'description': description
            }
            data = json.JSONEncoder().encode(data)
            url = "http://%s/apiKeys/create" % (self.host)
            ret = requests.post(url=url, data=data, headers=headers)
            logger.info('create apiKey, response status_code: %s, body: %s', ret.status_code, ret.json())
            if ret.status_code != 200:
                raise DmaapClientException(ret.json())
            ret = ret.json()
            resp_data = {
                'apiKey': ret.get('key', ''),
                'apiSecret': ret.get('secret', ''),
            }
            return resp_data
        except Exception as e:
            raise DmaapClientException('create apikey from dmaap failed: ' + e.message)
