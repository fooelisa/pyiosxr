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

import re
import sys
import difflib
import pexpect
from exceptions import XMLCLIError, InvalidInputError, TimeoutError, EOFError, IteratorIDError

import xml.etree.ElementTree as ET


# Build and execute xml requests.
def __execute_rpc__(device, rpc_command, timeout):
    rpc_command = '<?xml version="1.0" encoding="UTF-8"?><Request MajorVersion="1" MinorVersion="0">'+rpc_command+'</Request>'
    try:
        device.sendline(rpc_command)
        index = device.expect_exact(["</Response>","ERROR: 0xa240fe00"], timeout = timeout)
        if index == 1:
            raise XMLCLIError('The XML document is not well-formed')
    except pexpect.TIMEOUT as e:
        raise TimeoutError("pexpect timeout error")
    except pexpect.EOF as e:
        raise EOFError("pexpect EOF error")

    #remove leading XML-agent prompt
    response_assembled = device.before+device.match
    response = re.sub('^[^<]*', '', response_assembled)

    root = ET.fromstring(response)
    if 'IteratorID' in root.attrib:
        raise IteratorIDError("Non supported IteratorID in Response object. \
Turn iteration off on your XML agent by configuring 'xml agent [tty | ssl] iteration off'. \
For more information refer to http://www.cisco.com/c/en/us/td/docs/ios_xr_sw/iosxr_r4-1/xml/programming/guide/xl41apidoc.pdf, \
7-99.Turn iteration off on your XML agent.")

    childs = [x.tag for x in list(root)]

    result_summary = root.find('ResultSummary')

    if result_summary is not None and int(result_summary.get('ErrorCount', 0)) > 0:

        if 'CLI' in childs:
            error_msg = root.find('CLI').get('ErrorMsg') or ''
        elif 'Commit' in childs:
            error_msg = root.find('Commit').get('ErrorMsg') or ''
        else:
            error_msg = root.get('ErrorMsg') or ''

        error_msg += '\nOriginal call was: %s' % rpc_command
        raise XMLCLIError(error_msg)

    if 'CLI' in childs:
        cli_childs = [x.tag for x in list(root.find('CLI'))]
        if 'Configuration' in cli_childs:
            output = root.find('CLI').find('Configuration').text
            if output is None:
                output = ''
            elif 'Invalid input detected' in output:
                raise InvalidInputError('Invalid input entered:\n%s' % output)

    return root

# Ecexute show commands not in config context.
def __execute_show__(device, show_command, timeout):
    rpc_command = '<CLI><Exec>'+show_command+'</Exec></CLI>'
    response = __execute_rpc__(device, rpc_command, timeout)
    return response.find('CLI').find('Exec').text.lstrip()

# Ecexute show commands not in config context.
def __execute_config_show__(device, show_command, timeout):
    rpc_command = '<CLI><Configuration>'+show_command+'</Configuration></CLI>'
    response = __execute_rpc__(device, rpc_command, timeout)
    return response.find('CLI').find('Configuration').text.lstrip()


class IOSXR:

    def __init__(self, hostname, username, password, port=22, timeout=60, logfile=None, lock=True):
        """
        A device running IOS-XR.

        :param hostname:  (str) IP or FQDN of the device you want to connect to
        :param username:  (str) Username
        :param password:  (str) Password
        :param port:      (int) SSH Port (default: 22)
        :param timeout:   (int) Timeout (default: 60 sec)
        :param logfile:   File-like object to save device communication to or None to disable logging
        :param lock:      (bool) Auto-lock config upon open() if set to True, connect without locking if False (default: True)
        """
        self.hostname = str(hostname)
        self.username = str(username)
        self.password = str(password)
        self.port     = int(port)
        self.timeout  = int(timeout)
        self.logfile  = logfile
        self.lock_on_connect = lock
        self.locked   = False

    def __getattr__(self, item):
        """
        Ok, David came up with this kind of dynamic method. It takes
        calls with show commands encoded in the name. I'll replacs the
        underscores for spaces and issues the show command... pretty neat!
        """
        def wrapper(*args, **kwargs):
            cmd = item.replace('_', ' ')
            response = __execute_show__(self.device, cmd, self.timeout)
            match = re.search(".*(!! IOS XR Configuration.*)</Exec>",response,re.DOTALL)
            if match is not None:
                response = match.group(1)
            return response

        if item.startswith('show'):
            return wrapper
        else:
            raise AttributeError("type object '%s' has no attribute '%s'" % (self.__class__.__name__, item))

    def make_rpc_call(self, rpc_command):
        """
        Allow a user to query a device directly using XML-requests
        """
        result = __execute_rpc__(self.device, rpc_command, self.timeout)
        return ET.tostring(result)

    def open(self):
        """
        Opens a connection to an IOS-XR device.
        """
        device = pexpect.spawn('ssh -o ConnectTimeout={} -p {} {}@{}'.format(self.timeout, self.port, self.username, self.hostname), logfile=self.logfile)
        try:
            index = device.expect(['\(yes\/no\)\?', 'password:', '#', pexpect.EOF], timeout = self.timeout)
            if index == 0:
                device.sendline('yes')
                index = device.expect(['\(yes\/no\)\?', 'password:', '#', pexpect.EOF], timeout = self.timeout)
            if index == 1:
                device.sendline(self.password)
            elif index == 3:
                pass
            if index != 2:
                device.expect('#', timeout = self.timeout)
            device.sendline('xml')
            index = device.expect(['XML>', 'ERROR: 0x24319600'], timeout = self.timeout)
            if index == 1:
                raise XMLCLIError('XML TTY agent has not been started. Please configure \'xml agent tty\'.')
        except pexpect.TIMEOUT as e:
            raise TimeoutError("pexpect timeout error")
        except pexpect.EOF as e:
            raise EOFError("pexpect EOF error")
        self.device = device
        if self.lock_on_connect:
            self.lock()

    def close(self):
        """
        Closes the connection to the IOS-XR device.
        """
        if self.lock_on_connect or self.locked:
            self.unlock()
        self.device.close()

    def lock(self):
        """
        Locks the IOS-XR device config.
        """
        if not self.locked:
            rpc_command = '<Lock/>'
            response = __execute_rpc__(self.device, rpc_command, self.timeout)
            self.locked = True

    def unlock(self):
        """
        Unlocks the IOS-XR device config.
        """
        if self.locked:
            rpc_command = '<Unlock/>'
            response = __execute_rpc__(self.device, rpc_command, self.timeout)
            self.locked = False

    def load_candidate_config(self, filename=None, config=None):
        """
        Populates the attribute candidate_config with the desired
        configuration and loads it into the router. You can populate it from
        a file or from a string. If you send both a filename and a string
        containing the configuration, the file takes precedence.

        :param filename:  Path to the file containing the desired
                          configuration. By default is None.
        :param config:    String containing the desired configuration.
        """
        configuration = ''

        if filename is None:
            configuration = config
        else:
            with open(filename) as f:
                configuration = f.read()

        rpc_command = '<CLI><Configuration>'+configuration+'</Configuration></CLI>'

        try:
            __execute_rpc__(self.device, rpc_command, self.timeout)
        except InvalidInputError as e:
            self.discard_config()
            raise InvalidInputError(e.message)

    def compare_config(self):
        """
        Compares executed candidate config with the running config and
        returns a diff, assuming the loaded config will be merged with the
        existing one.

        :return:  Config diff.
        """
        show_merge = __execute_config_show__(self.device, 'show configuration merge', self.timeout)
        show_run = __execute_config_show__(self.device, 'show running-config', self.timeout)

        diff = difflib.unified_diff(show_run.splitlines(1)[2:-2],show_merge.splitlines(1)[2:-2],n=0)
        diff = ''.join([x.replace('\r', '') for x in diff])
        return diff

    def compare_replace_config(self):
        """
        Compares executed candidate config with the running config and
        returns a diff, assuming the entire config will be replaced.

        :return:  Config diff.
        """
        diff = __execute_config_show__(self.device, 'show configuration changes diff', self.timeout)

        return ''.join(diff.splitlines(1)[2:-2])

    def commit_config(self, label=None, comment=None, confirmed=None):
        """
        Commits the candidate config to the device, by merging it with the
        existing one.

        :param label:     Commit comment, displayed in the commit entry on the device.
        :param comment:   Commit label, displayed instead of the commit ID on the device.
        :param confirmed: Commit with auto-rollback if new commit is not made in 30 to 300 sec
        """
        rpc_command = '<Commit'
        if label:
            rpc_command += ' Label="%s"' % label
        if comment:
            rpc_command += ' Comment="%s"' % comment
        if confirmed:
            if 30 <= int(confirmed) <= 300:
                rpc_command += ' Confirmed="%d"' % int(confirmed)
            else: raise InvalidInputError('confirmed needs to be between 30 and 300')
        rpc_command += '/>'

        response = __execute_rpc__(self.device, rpc_command, self.timeout)

    def commit_replace_config(self, label=None, comment=None, confirmed=None):
        """
        Commits the candidate config to the device, by replacing the existing
        one.

        :param comment:   User comment saved on this commit on the device
        :param label:     User label saved on this commit on the device
        :param confirmed: Commit with auto-rollback if new commit is not made in 30 to 300 sec
        """
        rpc_command = '<Commit Replace="true"'
        if label:
            rpc_command += ' Label="%s"' % label
        if comment:
            rpc_command += ' Comment="%s"' % comment
        if confirmed:
            if 30 <= int(confirmed) <= 300:
                rpc_command += ' Confirmed="%d"' % int(confirmed)
            else: raise InvalidInputError('confirmed needs to be between 30 and 300')
        rpc_command += '/>'
        response = __execute_rpc__(self.device, rpc_command, self.timeout)

    def discard_config(self):
        """
        Clears uncommited changes in the current session.
        """
        rpc_command = '<Clear/>'
        response = __execute_rpc__(self.device, rpc_command, self.timeout)

    def rollback(self):
        """
        Used after a commit, the configuration will be reverted to the
        previous committed state.
        """
        rpc_command = '<Unlock/><Rollback><Previous>1</Previous></Rollback><Lock/>'
        response = __execute_rpc__(self.device, rpc_command, self.timeout)
