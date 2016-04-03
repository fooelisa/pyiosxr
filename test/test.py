#!/usr/bin/env python

import sys
import mock
import unittest

from pyIOSXR import IOSXR
from pyIOSXR.exceptions import XMLCLIError, InvalidInputError, TimeoutError, EOFError, IteratorIDError


# def __execute_rpc__(device, rpc_command, timeout):
# def __execute_show__(device, show_command, timeout):
# def __execute_config_show__(device, show_command, timeout):

# test class IOSXR
#     def __getattr__(self, item):
#     def make_rpc_call(self, rpc_command):
#     def open(self):
#     def close(self):
#     def lock(self):
#     def unlock(self):
#     def load_candidate_config(self, filename=None, config=None):
#     def compare_config(self):
#     def compare_replace_config(self):
#     def commit_config(self, label=None, comment=None, confirmed=None):
#     def commit_replace_config(self, label=None, comment=None, confirmed=None):
#     def discard_config(self):
#     def rollback(self):


#     def __init__(self, hostname, username, password, port=22, timeout=60, logfile=None, lock=True):

class Test__init__(unittest.TestCase):

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
        self.assertTrue(IOSXR(hostname='hostname', username='ejasinska', password='passwd', logfile='filename'))

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


if __name__ == '__main__':
    unittest.main()
