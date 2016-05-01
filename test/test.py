#!/usr/bin/env python

import sys
import mock
import unittest
import xml.etree.ElementTree as ET

import pexpect
from pyIOSXR import IOSXR
from pyIOSXR.exceptions import XMLCLIError, InvalidInputError, TimeoutError, EOFError, IteratorIDError


## XXX

# def __execute_rpc__(device, rpc_command, timeout):
# def __execute_show__(device, show_command, timeout):
# def __execute_config_show__(device, show_command, timeout):

# test class IOSXR
#     def __getattr__(self, item):

## XXX


#     def __init__(self, hostname, username, password, port=22, timeout=60, logfile=None, lock=True):

class TestInit(unittest.TestCase):

    def test_init(self):
        '''
        Test pyiosxr class init
        Should return True
        '''
        self.assertTrue(IOSXR(hostname='hostname', username='ejasinska', password='passwd'))

    def test_init_no_lock(self):
        '''
        Test pyiosxr class init - woithout locking
        Should return True
        '''
        self.assertTrue(IOSXR(hostname='hostname', username='ejasinska', password='passwd', lock=False))

    def test_init_log_stdout(self):
        '''
        Test pyiosxr class init - log to stdout
        Should return True
        '''
        self.assertTrue(IOSXR(hostname='hostname', username='ejasinska', password='passwd', logfile=sys.stdout))

    def test_init_log_file(self):
        '''
        Test pyiosxr class init - log to file
        Should return True
        '''
        self.assertTrue(IOSXR(hostname='hostname', username='ejasinska', password='passwd', logfile='filehandle'))

    def test_init_port(self):
        '''
        Test pyiosxr class init - pass port number
        Should return True
        '''
        self.assertTrue(IOSXR(hostname='hostname', username='ejasinska', password='passwd', port=22))

    def test_init_timeout(self):
        '''
        Test pyiosxr class init - pass timeout
        Should return True
        '''
        self.assertTrue(IOSXR(hostname='hostname', username='ejasinska', password='passwd', timeout=120))


#     def open(self):

class TestOpen(unittest.TestCase):

    @mock.patch('pyIOSXR.iosxr.pexpect.spawn')
    @mock.patch('pyIOSXR.iosxr.IOSXR.lock')
    def test_open(self, mock_lock, mock_spawn):
        '''
        Test pyiosxr class open
        Should return None
        '''
        device = IOSXR(hostname='hostname', username='ejasinska', password='passwd', port=22, timeout=60, logfile=None, lock=True)
        self.assertIsNone(device.open())

    @mock.patch('pyIOSXR.iosxr.pexpect.spawn')
    def test_open_no_lock(self, mock_spawn):
        '''
        Test pyiosxr class open - without lock
        Should return None
        '''
        device = IOSXR(hostname='hostname', username='ejasinska', password='passwd', port=22, timeout=60, logfile=None, lock=False)
        self.assertIsNone(device.open())

    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.__init__')
    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.expect')
    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.sendline')
    def test_open_ssh_key_yes(self, mock_sendline, mock_expect, mock_spawn):
        '''
        Test pyiosxr class open - with ssh key warning
        Should return Nona
        '''
        device = IOSXR(hostname='hostname', username='ejasinska', password='passwd', port=22, timeout=60, logfile=None, lock=False)
        mock_spawn.return_value = None
        mock_expect.return_value = 0
        self.assertIsNone(device.open())

    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.__init__')
    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.expect')
    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.sendline')
    def test_open_no_passwd(self, mock_sendline, mock_expect, mock_spawn):
        '''
        Test pyiosxr class open - pexpect.EOF
        Should return Nona
        '''
        device = IOSXR(hostname='hostname', username='ejasinska', password='passwd', port=22, timeout=60, logfile=None, lock=False)
        mock_spawn.return_value = None
        mock_expect.return_value = 3
        self.assertIsNone(device.open())

    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.__init__')
    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.expect')
    def test_open_TimeoutError(self, mock_expect, mock_spawn):
        '''
        Test pyiosxr class open - raising pexpect.TIMEOUT
        Should return TimeoutError
        '''
        device = IOSXR(hostname='hostname', username='ejasinska', password='passwd', port=22, timeout=60, logfile=None, lock=True)
        mock_spawn.return_value = None
        mock_expect.side_effect = pexpect.TIMEOUT('error')
        self.assertRaises(TimeoutError, device.open)

    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.__init__')
    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.expect')
    def test_open_EOFError(self, mock_expect, mock_spawn):
        '''
        Test pyiosxr class open - raising pexpect.EOF
        Should return EOFError
        '''
        device = IOSXR(hostname='hostname', username='ejasinska', password='passwd', port=22, timeout=60, logfile=None, lock=True)
        mock_spawn.return_value = None
        mock_expect.side_effect = pexpect.EOF('error')
        self.assertRaises(EOFError, device.open)

    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.__init__')
    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.expect')
    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.sendline')
    def test_open_XMLCLIError(self, mock_sendline, mock_expect, mock_spawn):
        '''
        Test pyiosxr class open - error as if XML not enabled on device: ERROR: 0x24319600
        Should return XMLCLIError
        '''
        device = IOSXR(hostname='hostname', username='ejasinska', password='passwd', port=22, timeout=60, logfile=None, lock=True)
        mock_spawn.return_value = None
        # expect returns 1 to raise XMLCLIError
        mock_expect.return_value = 1
        self.assertRaises(XMLCLIError, device.open)


#     def close(self):

class TestClose(unittest.TestCase):

    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.__init__')
    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.expect')
    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.sendline')
    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.close')
    def test_close(self, mock_close, mock_sendline, mock_expect, mock_spawn):
        '''
        Test pyiosxr class close
        Should return None
        '''
        device = IOSXR(hostname='hostname', username='ejasinska', password='passwd', port=22, timeout=60, logfile=None, lock=False)
        mock_spawn.return_value = None
        device.open()
        self.assertIsNone(device.close())

    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.__init__')
    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.expect')
    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.sendline')
    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.close')
    @mock.patch('pyIOSXR.iosxr.IOSXR.lock')
    @mock.patch('pyIOSXR.iosxr.__execute_rpc__')
    def test_close_locked(self, mock_rpc, mock_lock, mock_close, mock_sendline, mock_expect, mock_spawn):
        '''
        Test pyiosxr class close with lock
        Should return None
        '''
        device = IOSXR(hostname='hostname', username='ejasinska', password='passwd', port=22, timeout=60, logfile=None, lock=True)
        mock_spawn.return_value = None
        device.open()
        self.assertIsNone(device.close())


#     def lock(self):

class TestLock(unittest.TestCase):

    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.__init__')
    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.expect')
    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.sendline')
    @mock.patch('pyIOSXR.iosxr.__execute_rpc__')
    def test_lock(self, mock_rpc, mock_sendline, mock_expect, mock_spawn):
        '''
        Test pyiosxr class lock
        Should return None
        '''
        device = IOSXR(hostname='hostname', username='ejasinska', password='passwd', port=22, timeout=60, logfile=None, lock=False)
        mock_spawn.return_value = None
        device.open()
        self.assertIsNone(device.lock())


#     def unlock(self):

class TestUnlock(unittest.TestCase):

    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.__init__')
    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.expect')
    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.sendline')
    @mock.patch('pyIOSXR.iosxr.IOSXR.lock')
    @mock.patch('pyIOSXR.iosxr.__execute_rpc__')
    def test_unlock(self, mock_rpc, mock_lock, mock_sendline, mock_expect, mock_spawn):
        '''
        Test pyiosxr class unlock
        Should return None
        '''
        device = IOSXR(hostname='hostname', username='ejasinska', password='passwd', port=22, timeout=60, logfile=None, lock=True)
        mock_spawn.return_value = None
        device.open()
        device.locked = True
        self.assertIsNone(device.unlock())


#     def discard_config(self):

class TestDiscardConfig(unittest.TestCase):

    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.__init__')
    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.expect')
    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.sendline')
    @mock.patch('pyIOSXR.iosxr.__execute_rpc__')
    def test_discard_config(self, mock_rpc, mock_sendline, mock_expect, mock_spawn):
        '''
        Test pyiosxr class discard_config
        Should return None
        '''
        device = IOSXR(hostname='hostname', username='ejasinska', password='passwd', port=22, timeout=60, logfile=None, lock=False)
        mock_spawn.return_value = None
        device.open()
        self.assertIsNone(device.discard_config())


#     def rollback(self):

class TestRollback(unittest.TestCase):

    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.__init__')
    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.expect')
    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.sendline')
    @mock.patch('pyIOSXR.iosxr.__execute_rpc__')
    def test_rollback(self, mock_rpc, mock_sendline, mock_expect, mock_spawn):
        '''
        Test pyiosxr class rollback
        Should return None
        '''
        device = IOSXR(hostname='hostname', username='ejasinska', password='passwd', port=22, timeout=60, logfile=None, lock=False)
        mock_spawn.return_value = None
        device.open()
        self.assertIsNone(device.rollback())


#     def make_rpc_call(self, rpc_command):

class TestMakeRpcCall(unittest.TestCase):

    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.__init__')
    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.expect')
    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.sendline')
    @mock.patch('pyIOSXR.iosxr.__execute_rpc__')
    def test_make_rpc_call(self, mock_rpc, mock_sendline, mock_expect, mock_spawn):
        '''
        Test pyiosxr class make_rpc_call
        Should return True
        '''
        device = IOSXR(hostname='hostname', username='ejasinska', password='passwd', port=22, timeout=60, logfile=None, lock=False)
        mock_spawn.return_value = None
        mock_rpc.return_value = ET.fromstring('<xml></xml>')
        device.open()
        self.assertTrue(device.make_rpc_call("<Get><Operational><LLDP><NodeTable></NodeTable></LLDP></Operational></Get>"))


#     def load_candidate_config(self, filename=None, config=None):

class TestLoadCandidateConfig(unittest.TestCase):

    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.__init__')
    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.expect')
    @mock.patch('pyIOSXR.iosxr.pexpect.spawn.sendline')
    @mock.patch('pyIOSXR.iosxr.__execute_rpc__')
    def test_load_candidate_config(self, mock_rpc, mock_sendline, mock_expect, mock_spawn):
        '''
        Test pyiosxr class load_candidate_config
        Should return None
        '''
        device = IOSXR(hostname='hostname', username='ejasinska', password='passwd', port=22, timeout=60, logfile=None, lock=False)
        mock_spawn.return_value = None
        device.open()
        self.assertIsNone(device.load_candidate_config(filename='test/config.txt'))

## XXX

#     def compare_config(self):
#     def compare_replace_config(self):
#     def commit_config(self, label=None, comment=None, confirmed=None):
#     def commit_replace_config(self, label=None, comment=None, confirmed=None):
#     def get_candidate_config(self, merge=False, formal=False):

## XXX


if __name__ == '__main__':
    unittest.main()
