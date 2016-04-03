#!/usr/bin/env python

import mock
import unittest

from pyIOSXR import IOSXR
from pyIOSXR.exceptions import XMLCLIError, InvalidInputError, TimeoutError, EOFError, IteratorIDError


# def __execute_rpc__(device, rpc_command, timeout):
# def __execute_show__(device, show_command, timeout):
# def __execute_config_show__(device, show_command, timeout):

# test class IOSXR
#     def __init__(self, hostname, username, password, port=22, timeout=60, logfile=None, lock=True):
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

