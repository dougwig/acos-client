# Copyright 2016, A10 Networks
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

import base


class Interface(base.BaseV30):
    def __init__(self, client):
        super(Interface, self).__init__(client)
        self.url_prefix = "/interface/"

    def _url_from_ifnum(self, ifnum=None):
        return self.url_prefix + self._ifnum_to_str(ifnum)

    def _ifnum_to_str(self, ifnum=None):
        return str(ifnum if ifnum else "")

    def _build_payload(self, ifnum=None, ip_address=None, dhcp=True):
        rv = {
            "interface": {
                "ip": {
                }
            }
        }

        if ifnum:
            rv["interface"]["ifnum"] = ifnum

        if ip_address:
            rv["interface"]["ip"]["address"] = ip_address
        elif dhcp:
            rv["interface"]["ip"]["dhcp"] = 1 if dhcp else 0

        return rv

    def get_list(self):
        return self._get(self.url_prefix)

    def get(self, ifnum=None):
        return self._get(self._url_from_ifnum(ifnum))

    def delete(self, ifnum):
        url = self.url_prefix + self._ifnum_to_str(ifnum)
        return self._delete(url)

    def create(self, ifnum, ip_address=None, dhcp=True):
        payload = self._build_payload(ifnum, ip_address, dhcp)
        return self._post(self.url_prefix + self._ifnum_to_str(ifnum))

    def update(self, ifnum, ip_address=None, dhcp=True, enable=True, speed="auto"):
        payload = self._build_payload(ifnum, ip_address, dhcp)
        return self._post(self.url_prefix + self._ifnum_to_str(ifnum), payload)

    @property
    def ethernet(self):
        return EthernetInterface(self.client)

    @property
    def management(self):
        return ManagementInterface(self.client)


class EthernetInterface(Interface):
    def __init__(self, client):
        super(EthernetInterface, self).__init__(client)
        self.iftype = "ethernet"
        self.url_prefix = "{0}{1}/".format(self.url_prefix, self.iftype)


    def _build_payload(self, ifnum, ip_address=None, dhcp=True):
        rv = super(EthernetInterface, self)._build_payload(ifnum, ip_address, dhcp)
        # Allows us to use the Interface class for non-ethernet ifs
        rv[self.iftype] = rv.pop("interface")
        return rv


class ManagementInterface(Interface):
    def __init__(self, client):
        super(ManagementInterface, self).__init__(client)
        self.iftype = "management"
        self.url_prefix = "{0}{1}/".format(self.url_prefix, self.iftype)

    def _build_payload(self, ifnum, ip_address=None, dhcp=True):
        rv = super(ManagementInterface, self)._build_payload(None, ip_address, dhcp)
        # Allows us to use the Interface class for non-management ifs
        rv[self.iftype] = rv.pop("interface")
        return rv