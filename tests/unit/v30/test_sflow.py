# Copyright 2014,  Doug Wiegley,  A10 Networks.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock
import unittest2 as unittest

from acos_client.v30 import sflow


class TestSFlow(unittest.TestCase):
    def setUp(self):
        self.client = mock.MagicMock()
        self.target = sflow.SFlow(self.client)

    def test_collector_ip_create(self):
        self.target.collector.ip.create("127.0.0.1", 4242)
        expected = {"sflow-collector": {"ip": "127.0.0.1", "port": 4242}}
        actual = self.client.http.request.call_args[0]
        self.assertTrue(expected in actual)

    def test_collector_ip_get(self):
        self.target.collector.ip.get("127.0.0.1", 4242)
        expected = "/axapi/v3/sflow/collector/ip/ip/127.0.0.1+4242"
        actual = self.client.http.request.call_args[0]
        self.assertTrue(expected in actual)

    def test_setting_create(self):
        self.target.setting.create(60, False, 20, 600)
        expected = {'setting': {
                    'source-ip-use-mgmt': 0,
                    'counter-polling-interval': 600,
                    'packet-sampling-rate': 20,
                    'max-header': 60}}
        actual = self.client.http.request.call_args[0]
        self.assertTrue(expected in actual)

    def _test_polling_create(self, http_counter=False):
        self.target.polling.create(http_counter)
        expected = {'polling': {'http-counter': int(http_counter)}}
        actual = self.client.http.request.call_args[0]
        self.assertTrue(expected in actual)

    def test_polling_create_http_counter_negative(self):
        self._test_polling_create()

    def test_polling_create_http_counter_positive(self):
        self._test_polling_create(True)
