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
import datetime
import hmac
import json
import logging
import time
from hashlib import sha1

import requests
from apscheduler.scheduler import Scheduler

from client.pub.exceptions import DmaapClientException

logger = logging.getLogger(__name__)


class BatchPublisherClient:
    def __init__(self, host, topic, partition="", contenttype="text/plain", max_batch_size=100, max_batch_age_ms=1000):
        self.host = host
        self.topic = topic
        self.partition = partition
        self.contenttype = contenttype
        self.max_batch_size = max_batch_size
        self.max_batch_age_ms = max_batch_age_ms
        self.pending = []
        self.closed = False
        self.dont_send_until_ms = 0
        self.scheduler = Scheduler(standalone=False)
        self.api_key = '',
        self.api_secret = ''

        @self.scheduler.interval_schedule(second=1)
        def crawl_job():
            self.send_message(False)
        self.scheduler.start()

    def set_api_credentials(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def send(self, partition, msg):
        try:
            if self.closed:
                raise DmaapClientException("The publisher was closed.")
            message = Message(partition, msg)
            self.pending.append(message)
            return len(self.pending)
        except Exception as e:
            raise DmaapClientException("append message failed: " + e.message)

    def send_message(self, force):
        if force or self.should_send_now():
            if not self.send_batch():
                logger.error("Send failed, %s message to send.", len(self.pending))

    def should_send_now(self):
        should_send = False
        if len(self.pending) > 0:
            now_ms = int(time.time() * 1000)
            should_send = len(self.pending) >= self.max_batch_size
            if not should_send:
                send_at_ms = self.pending[0].timestamp_ms
                should_send = send_at_ms <= now_ms

            should_send = should_send and now_ms >= self.dont_send_until_ms

        return should_send

    def send_batch(self):
        if len(self.pending) < 1:
            return True
        now_ms = int(time.time() * 1000)
        url = self.create_url()
        logger.info("sending %s msgs to %s . Oldest: %s ms", len(self.pending), url,
                    str(now_ms - self.pending[0].timestamp_ms))
        try:
            str_msg = ''
            if self.contenttype == "application/json":
                str_msg = self.parse_json()
            elif self.contenttype == "text/plain":
                for m in self.pending:
                    str_msg += m.msg
                    str_msg += '\n'
            elif self.contenttype == "application/cambria":
                for m in self.pending:
                    str_msg += str(len(m.partition))
                    str_msg += '.'
                    str_msg += str(len(m.msg))
                    str_msg += '.'
                    str_msg += m.partition
                    str_msg += m.msg
                    str_msg += '\n'
            else:
                for m in self.pending:
                    str_msg += m.msg
            msg = bytearray(str_msg)

            start_ms = int(time.time() * 1000)
            if self.api_key:
                headers = self.create_headers()
            else:
                headers = {'content-type': self.contenttype}
            ret = requests.post(url=url, data=msg, headers=headers)
            if ret.status_code < 200 or ret.status_code > 299:
                return False
            logger.info("MR reply ok (%s ms): %s", start_ms - int(time.time() * 1000), ret.json())
            self.pending = []
            return True

        except Exception as e:
            logger.error(e.message)
            return False

    def create_headers(self):
        data = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + '-04:00'
        hmac_code = hmac.new(self.api_secret.encode(), data.encode(), sha1).digest()
        signature = base64.b64encode(hmac_code).decode()
        auth = self.api_key + ':' + signature
        headers = {
            'X-CambriaDate': data,
            'X-CambriaAuth': auth,
            'content-type': self.contenttype
        }
        return headers

    def create_url(self):
        url = "http://%s/events/%s" % (self.host, self.topic)
        if self.partition:
            url = url + "?partitionKey=" + self.partition
        return url

    def parse_json(self):
        data = []
        for message in self.pending:
            msg = json.loads(message.msg)
            for m in msg:
                data.append(m)
        return json.dumps(data)

    def close(self, timeout):
        try:
            self.closed = True
            self.scheduler.shutdown()
            now_ms = int(time.time() * 1000)
            wait_in_ms = now_ms + timeout * 1000

            while int(time.time() * 1000) < wait_in_ms and len(self.pending) > 0:
                self.send_message(True)
                time.sleep(0.25)
            return self.pending
        except Exception as e:
            raise DmaapClientException("send message failed: " + e.message)


class Message:
    def __init__(self, partition, msg):
        if not partition:
            self.partition = ""
        else:
            self.partition = partition
        self.msg = msg
        self.timestamp_ms = int(time.time() * 1000)
