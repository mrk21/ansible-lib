# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import generators
from __future__ import division

import os
import unittest
import sys

from ansible_lib.http_wait_for import *
from test_double.ansible_module_mock import *
from test_double.http_client_mock import *

class ProgressMock(object):
    def __init__(self):
        self.seconds = 0
    
    def elapsed(self):
        return self.seconds
    
    def wait(self, value):
        self.seconds += value

class HTTPWaitForTest(unittest.TestCase):
    TIMEOUT = 60
    INTERVAL = 3
    HTTP_OK_STATUS = 200
    HTTP_NOT_OK_STATUS = 503
    RESULT_OK_STATUS = 1
    RESULT_TIMEOUT_STATUS = 2
    RESULT_NON_HTTP_STATUS = 3
    
    def setUp(self):
        self.instance = HTTPWaitFor(AnsibleModuleMock, HTTPClientMock, ProgressMock)
        self.instance.module.params['status'] = self.HTTP_OK_STATUS
        self.instance.module.params['timeout'] = self.TIMEOUT
        self.instance.module.params['interval'] = self.INTERVAL
    
    def test_execute_should_exit_when_http_status_is_ok(self):
        def callback(*args, **kwargs):
            self.assertEqual(kwargs['status'], self.RESULT_OK_STATUS)
            self.assertEqual(kwargs['elapsed'], 0)
        
        self.instance.module.test_data__ = {
            'HTTPClientMock': {
                'response': [{'status': self.HTTP_OK_STATUS}],
            },
            'callback': {'exit': callback}
        }
        
        self.instance.execute()
    
    def test_execute_should_fail_when_http_status_is_not_ok(self):
        def callback(*args, **kwargs):
            self.assertEqual(kwargs['status'], self.RESULT_TIMEOUT_STATUS)
            self.assertEqual(kwargs['elapsed'], self.TIMEOUT)
        
        self.instance.module.test_data__ = {
            'HTTPClientMock': {
                'response': [{'status': self.HTTP_NOT_OK_STATUS}],
            },
            'callback': {'fail': callback}
        }
        
        self.instance.execute()
    
    def test_execute_should_fail_when_not_connected(self):
        def callback(*args, **kwargs):
            self.assertEqual(kwargs['status'], self.RESULT_TIMEOUT_STATUS)
            self.assertEqual(kwargs['elapsed'], self.TIMEOUT)
        
        self.instance.module.test_data__ = {
            'HTTPClientMock': {
                'response': [None],
            },
            'callback': {'fail': callback}
        }
        
        self.instance.execute()
    
    def test_execute_should_fail_when_connected_server_is_non_http(self):
        def callback(*args, **kwargs):
            self.assertEqual(kwargs['status'], self.RESULT_NON_HTTP_STATUS)
            self.assertEqual(kwargs['elapsed'], 0)
        
        self.instance.module.test_data__ = {
            'HTTPClientMock': {
                'response': [{'status': None}],
            },
            'callback': {'fail': callback}
        }
        
        self.instance.execute()
