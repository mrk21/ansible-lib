import os
import unittest
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from http_wait_for import *
from test_double.ansible_module_mock import *
from test_double.http_client_mock import *

class ProgressMock:
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
    
    def test_The_execute_method_exit_when_the_HTTP_status_is_ok(self):
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
    
    def test_The_execute_method_fail_when_the_HTTP_status_is_not_ok(self):
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
    
    def test_The_execute_method_fail_when_not_connected(self):
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
    
    def test_The_execute_method_fail_when_the_connected_server_is_non_HTTP(self):
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

suite = unittest.TestLoader().loadTestsFromTestCase(HTTPWaitForTest)
unittest.TextTestRunner(verbosity=2).run(suite)
