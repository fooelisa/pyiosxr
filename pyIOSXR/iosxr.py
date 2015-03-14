# Copyright 2015 Netflix. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import pexpect
import exceptions

def __execute_rpc__(device, rpc_command):
    rpc_command = '<?xml version="1.0" encoding="UTF-8"?><Request MajorVersion="1" MinorVersion="0">'+rpc_command+'</Request>'
    device.sendline(rpc_command)
    device.expect("<Response.*</Response>")
    response = device.match.group()
    return response


class IOSXR:

    def __init__(self, hostname, username, password):
        """
        Device running IOS-XR.

        :param hostname:  IP or FQDN of the device you want to connect to
        :param username:  Username
        :param password:  Password
        """
        self.hostname = hostname
        self.username = username
        self.password = password

    def open(self):
        """
        Opens a connection to an IOS-XR device.
        """
        device = pexpect.spawn('ssh ' + self.username + '@' + self.hostname)
        index = device.expect(['\(yes\/no\)\?', pexpect.TIMEOUT])
        if index == 0:
          device.sendline('yes')
        elif index == 1:
          pass
        device.expect('password:')
        device.sendline(self.password)
        device.expect('#')
        device.sendline('xml')
        device.expect('XML>')
        self.device = device
        rpc_command = '<Lock/>'
        response = __execute_rpc__(self.device, rpc_command)
        print response

    def close(self):
        """
        Closes the connection to the IOS-XR device.
        """
        rpc_command = '<Unlock/>'
        response = __execute_rpc__(self.device, rpc_command)
        print response
        self.device.close()

    def load_candidate_config(self, filename=None, config=None):
        """
        Populates the attribute candidate_config with the desired
        configuration. You can populate it from a file or from a string. If
        you send both a filename and a string containing the configuration,
        the file takes precedence.

        :param filename:  Path to the file containing the desired
                          configuration. By default is None.
        :param config:    String containing the desired configuration.
        """
        # XXX

    def compare_config(self):
        """
        """
        # XXX

    def commit_config(self):
        """
        Commits the candidate config to the device.
        """
        rpc_command = '<Commit/>'
        response = __execute_rpc__(self.device, rpc_command)
        print response

    def discard_config(self):
        """
        """
        # XXX

    def rollback(self):
        """
        Used after a commit, the configuration will be reverted to the
        previous state.
        """
        rpc_command = '<Rollback/>'
        response = __execute_rpc__(self.device, rpc_command)
        print response


