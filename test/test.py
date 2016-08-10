#!/usr/bin/env python
# coding=utf-8
"""Unit tests for pyiosxr, a module to interact with Cisco devices running IOS-XR."""

import os
import sys
import unittest
from lxml import etree as ET

# ~~~ import pyIOSXR modules ~~~
from pyIOSXR import IOSXR
# private functions
from pyIOSXR.iosxr import __execute_rpc__
from pyIOSXR.iosxr import __execute_show__
from pyIOSXR.iosxr import __execute_config_show__
# exceptions
from pyIOSXR.exceptions import LockError
from pyIOSXR.exceptions import UnlockError
from pyIOSXR.exceptions import XMLCLIError
from pyIOSXR.exceptions import CommitError
from pyIOSXR.exceptions import ConnectError
from pyIOSXR.exceptions import TimeoutError
from pyIOSXR.exceptions import IteratorIDError
from pyIOSXR.exceptions import InvalidInputError
from pyIOSXR.exceptions import CompareConfigError
from pyIOSXR.exceptions import InvalidXMLResponse


class _MockedNetMikoDevice(object):

    """
    Defines the minimum attributes necessary to mock a SSH connection using netmiko.
    """

    def __init__(self):

        class _MockedParamikoTransport(object):
            def close(self):
                pass
        self.remote_conn = _MockedParamikoTransport()

    @staticmethod
    def get_mock_file(command, format='xml'):
        filename = \
            command.replace('<?xml version="1.0" encoding="UTF-8"?><Request MajorVersion="1" MinorVersion="0">', '')\
                   .replace('</Request>', '')\
                   .replace('<', '')\
                   .replace('>', '_')\
                   .replace('/', '')\
                   .replace('\n', '')\
                   .replace('.', '_')\
                   .replace(' ', '_')\
                   .replace('"', '_')\
                   .replace('=', '_')\
                   .replace('!', '')
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        filename = '{filename}.{fmt}'.format(
            filename=filename,
            fmt=format
        )
        fullpath = os.path.join(curr_dir, 'mock', filename)
        return open(fullpath).read()

    def find_prompt(self):
        return self.get_mock_file('\n', format='txt')

    def send_command(self,
                     command_string,
                     delay_factor=.1,
                     max_loops=150,
                     strip_prompt=True,
                     strip_command=True):
        return self.get_mock_file(command_string)

    def receive_data_generator(self):
        return ['', '']  # to have an iteration inside private method _netmiko_recv

    def send_command_expect(self,
                            command_string,
                            expect_string=None,
                            delay_factor=.2,
                            max_loops=500,
                            auto_find_prompt=True,
                            strip_prompt=True,
                            strip_command=True):
        # for the moment returns the output from send_command only
        # this may change in time
        return self.send_command(command_string)


class _MockedIOSXRDevice(IOSXR):

    """
    Overrides only the very basic methods from the main device driver, that cannot be mocked.
    """

    def open(self):
        self.device = _MockedNetMikoDevice()
        self._cli_prompt = self.device.find_prompt()
        self._enter_xml_mode()


class TestIOSXRDevice(unittest.TestCase):

    """
    Tests IOS-XR basic functions.
    """

    HOSTNAME = 'device.location'
    USERNAME = 'username'
    PASSWORD = 'password'
    PORT = 22
    TIMEOUT = 1  # for tests, smaller values are prefferred
    LOCK = False
    LOG = sys.stdout
    MOCK = True

    def __repr__(self):
        return 'Will connect to {user}@{host}:{port} and will timeout after {tout}'.format(
            user=self.USERNAME,
            host=self.HOSTNAME,
            port=self.PORT,
            tout=self.TIMEOUT
        ) if not self.MOCK else 'Simulates device behaviour using mocked data.'

    __str__ = __repr__

    @classmethod
    def setUpClass(cls):

        """
        Opens the connection with the IOS-XR device.
        """

        if cls.MOCK:
            __cls = _MockedIOSXRDevice
        else:
            __cls = IOSXR

        cls.device = __cls(cls.HOSTNAME,
                           cls.USERNAME,
                           cls.PASSWORD,
                           port=cls.PORT,
                           lock=cls.LOCK,
                           logfile=cls.LOG,
                           timeout=cls.TIMEOUT)
        cls.device.open()

    @classmethod
    def tearDownClass(cls):

        """
        Closes the connection with the device.
        """

        cls.device.close()

    def test_mock_lock_connection_open(self):

        if self.MOCK:
            self.device.lock_on_connect = True
            # because there's one single mock file
            # and it is already used for the lock test
            # will tesst if raises LockError on connect
            self.assertRaises(
                LockError,
                self.device.lock
            )
            # enough to see that will try to lock during connect

    def test_mock_close(self):

        """Testing if unlocking when connection is closed"""

        if self.MOCK:
            self.device.locked = True
            self.device.close()
            self.assertFalse(self.device.locked)

    def test_execute_rpc_method(self):

        """Testing private method _execute_rpc"""

        self.assertIsInstance(
            self.device._execute_rpc('<Get><Configuration><NTP></NTP></Configuration></Get>'),
            ET._Element
        )

    def test__getttr__show_(self):

        """Testing special attribute __getattr___ against valid show command"""

        self.assertIsInstance(
            self.device.show_ntp_ass(),
            str
        )

    def test__getttr__show_args(self):

        """Testing special attribute __getattr___ against valid show command with arguments"""

        self.assertIsInstance(
            self.device.show_ntp('ass'),
            str
        )

    def test__getattr_show_config(self):

        """Testing special attribute __getattr___ against valid show config command"""

        self.assertIsInstance(
            self.device.show_run_ntp(config=True),
            str
        )

    def test__getattr__no_show(self):

        """"Test special attribute __getattr__ agains a no-show command"""

        raised = False

        try:
            self.device.configure_exclusive()
        except AttributeError:
            raised = True

        self.assertTrue(raised)

    def test__execute_rpc__(self):

        """Testing private module function __execute_rpc___"""

        self.assertIsInstance(
            __execute_rpc__(self.device, '<Get><Configuration><NTP></NTP></Configuration></Get>', self.device.timeout),
            ET._Element
        )

    def test__execute_show__(self):

        """Testing private module function __execute_show__"""

        self.assertIsInstance(
            __execute_show__(self.device, 'show ntp ass', self.device.timeout),
            str
        )

    def test__execute_config_show__(self):

        """Testing private module function __execute_config_show__"""

        self.assertIsInstance(
            __execute_config_show__(self.device, 'show run ntp', self.device.timeout),
            str
        )

    def test_make_rpc_call_returns_XML(self):

        """Test if public method make_rpc_call returns str"""

        self.assertIsInstance(
            self.device.make_rpc_call('<Get><Configuration><NTP></NTP></Configuration></Get>'),
            str
        )

    def test_acquired_xml_agent(self):

        """Testing if raises TimeoutError if the XML agent is alredy acquired and released when exception thrown"""

        self.device._xml_agent_acquired = True  # acquiring the XML agent

        self.assertRaises(
            TimeoutError,
            self.device.make_rpc_call,
            '<Get><Operational><L2VPNForwarding></L2VPNForwarding></Operational></Get>'
        )

        self.assertFalse(self.device._xml_agent_acquired)  # Exception raised => xml agent released

    def test_try_to_read_till_timeout(self):

        """Testing if will try to read from the device till the timed out"""

        self.assertRaises(
            TimeoutError,
            self.device.make_rpc_call,
            '<This/><Does/><Not/><Exist/>'
        )

    def test_multiple_read_attempts_till_timeout(self):

        """Testing if will try to read non-empty replies from the device till timed out"""

        self.assertRaises(
            TimeoutError,
            self.device.make_rpc_call,
            '<Empty/><Reply/>'
        )

    def test_iterator_id_raises_IteratorIDError(self):

        """Testing if reply containing the IteratorID attribute raises IteratorIDError"""

        self.assertRaises(
            IteratorIDError,
            self.device.make_rpc_call,
            '<Get><Operational><L2VPNForwarding></L2VPNForwarding></Operational></Get>'
        )

    def test_channel_acquired_enter_xml_mode(self):

        """Test if raises ConnectError when the channel is busy with other requests"""

        self.device._xml_agent_acquired = True

        self.assertRaises(
            ConnectError,
            self.device._enter_xml_mode
        )

    def test_truncated_response_raises_InvalidXMLResponse(self):

        """Testing if truncated XML reply raises InvalidXMLResponse"""

        self.assertRaises(
            InvalidXMLResponse,
            self.device._execute_rpc,
            '<Get><Configuration><Fake/></Configuration></Get>'
        )

    def test_iosxr_bug_0x44318c06(self):

        """Tests if IOS-XR bug returns error 0x44318c06 and raise XMLCLIError"""

        self.assertRaises(
            XMLCLIError,
            self.device._execute_config_show,
            'show commit changes diff'
        )

    def test_empty_reply_raises_TimeoutError(self):

        """Testing if empty reply raises TimeoutError"""

        if self.MOCK:
            self.assertRaises(
                TimeoutError,
                self.device._execute_rpc,
                '<Empty/>'
            )

    def test_multiple_requests_raise_0xa3679e00(self):

        """Testing if simultaneuous requests trigger XMLCLIError"""

        if self.MOCK:
            self.assertRaises(
                XMLCLIError,
                self.device._execute_rpc,
                '<Get><Operational><ARP></ARP></Operational></Get>'
            )

    def test_execute_show(self):

        """Testing private method _execute_show"""

        self.assertIsInstance(
            self.device._execute_show('show ntp ass'),
            str
        )

    def test_execute_invalid_show_raises_InvalidInputError(self):

        """Testing if invalid show command raises InvalidInputError"""

        self.assertRaises(
            InvalidInputError,
            self.device._execute_show,
            'sh fake'
        )

    def test_execute_config_show(self):

        """Testing private method _execute_config_show"""

        self.assertIsInstance(
            self.device._execute_config_show('show run ntp'),
            str
        )

    def test_execute_invalid_config_show_raises_InvalidInputError(self):

        """Testing if invalid config show command raises InvalidInputError"""

        self.assertRaises(
            InvalidInputError,
            self.device._execute_config_show,
            'sh run fake'
        )

    def test_lock_raises_LockError(self):

        """Tests if DB already locked raises LockError"""

        if self.MOCK:
            self.assertRaises(
                LockError,
                self.device.lock
            )
            self.assertFalse(self.device.locked)
        else:
            try:
                self.device.lock()
            except LockError:
                self.assertFalse(self.device.locked)
            else:
                self.assertTrue(self.device.locked)

    def test_unlock(self):

        """Testing unlock feature"""

        if self.MOCK:
            self.device.lock = True  # make sure it is locked
            self.device.unlock()
            self.assertFalse(self.device.locked)
        else:
            try:
                self.device.lock()
            except UnlockError:
                self.assertTrue(self.device.locked)
            else:
                self.assertFalse(self.device.locked)

    def test_load_candidate_config(self):

        """Testing load candidate config"""

        self.device.load_candidate_config(config='ntp peer 172.17.17.1')

    def test_load_invalid_config_raises_InvalidInputError(self):

        """Testing if loading config with mistakes raises InvalidInputError"""

        self.assertRaises(
            InvalidInputError,
            self.device.load_candidate_config,
            config='ntp beer 256.257.258.259'
        )

    def test_load_candidate_config_file(self):

        """Testing loading candidate config from file"""

        self.device.load_candidate_config(
            filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mock', 'good.cfg'))

    def test_load_invalid_candidate_config_file_raises_InvalidInputError(self):

        """Testing if loading invalid config from a file raises InvalidInputError"""

        self.assertRaises(
            InvalidInputError,
            self.device.load_candidate_config,
            filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mock', 'bad.cfg')
        )

    def test_discard_config(self):

        """Testing discard config"""

        self.assertIsNone(self.device.discard_config())
        # nothing back, means no error

    def test_get_candidate_config(self):

        """Testing if able to retrieve candidate config"""

        self.assertIsInstance(
            self.device.get_candidate_config(),
            str
        )

    def test_get_candiate_config_merge(self):

        """Testing get_candidate_config using the merge option"""

        self.assertIsInstance(
            self.device.get_candidate_config(merge=True),
            str
        )

    def test_get_candidate_config_formal(self):

        """Testing get_candidate_config using the formal option"""

        self.assertIsInstance(
            self.device.get_candidate_config(formal=True),
            str
        )

    def test_compare_config(self):

        """Testing compare config"""

        # load some data
        cfg = (
            'no hostname edge01.yyz01\n'
            'hostname edge01.bjm01'
        )
        self.device.load_candidate_config(config=cfg)

        compare_result = self.device.compare_config()

        self.assertIsInstance(compare_result, str)
        # test if the result is string

        self.assertGreater(len(compare_result), 0)
        # test if len > 0

    def test_compare_replace_config(self):

        """Testing compare replace config"""

        self.assertIsInstance(self.device.compare_replace_config(), str)

    def test_commit_config(self):

        """Testing commit config"""

        self.assertIsNone(self.device.commit_config())

    def test_commit_config_message(self):

        """Testing commit config with comment message"""

        self.assertIsNone(self.device.commit_config(comment="good"))

    def test_commit_config_label(self):

        """Testing commit config with label"""

        self.assertIsNone(self.device.commit_config(label="test"))

    def test_commit_config_confirmed(self):

        """Testing commit confirmed"""

        self.assertIsNone(self.device.commit_config(confirmed=60))

    def test_commit_config_confirmed_raise_InvalidInputError(self):

        """Testing if incorrect value for confirmed commit time raises InvalidInputError"""

        self.assertRaises(
            InvalidInputError,
            self.device.commit_config,
            confirmed=1
        )

    def test_commit_empty_buffer_raises(self):

        """Testing if trying to commit empty changes raises CommitError"""

        self.assertRaises(
            CommitError,
            self.device.commit_config,
            comment="empty"
        )

    def test_commit_after_other_session_commit(self):

        """Testing if trying to commit after another process commited raises CommitError"""

        if self.MOCK:
            self.assertRaises(
                CommitError,
                self.device.commit_config,
                comment="parallel"
            )

    def test_commit_replace_config(self):

        """Testing commit replace config"""

        self.assertIsNone(self.device.commit_replace_config())

    def test_commit_replace_config_message(self):

        """Testing commit replace config with comment message"""

        self.assertIsNone(self.device.commit_replace_config(comment="good"))

    def test_commit_replace_config_label(self):

        """Testing commit replace config with label"""

        self.assertIsNone(self.device.commit_replace_config(label="test"))

    def test_commit_replace_config_confirmed(self):

        """Testing commit replace confirmed"""

        self.assertIsNone(self.device.commit_replace_config(confirmed=60))

    def test_commit_replace_config_confirmed_raise_InvalidInputError(self):

        """Testing if incorrect value for confirmed replace commit time raises InvalidInputError"""

        self.assertRaises(
            InvalidInputError,
            self.device.commit_replace_config,
            confirmed=500
        )

    def test_rollback(self):

        """Testing rollback"""

        self.device.rollback()


if __name__ == '__main__':
    unittest.main()
