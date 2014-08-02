# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import generators
from __future__ import division

import httplib
import socket

from test_double.ansible_module_mock import *

class HTTPClientMock(object):
    class HTTPResponseMock(object):
        def __init__(self, params):
            self.params = params
            self.status = self.params['status']
    
    class HTTPConnectionMock(object):
        def __init__(self, params):
            self.params = params
        
        def request(self, method, path):
            response = self.__current_response()
            if not response:
                raise socket.error()
            elif not response['status']:
                raise httplib.BadStatusLine(0)
        
        def getresponse(self):
            return HTTPClientMock.HTTPResponseMock(self.__current_response())
        
        def close(self):
            response = self.params['response']
            if isinstance(response,list) and len(response) > 1:
                response.pop(0)
        
        def __current_response(self):
            response = self.params['response']
            if isinstance(response,list):
                response = response[0]
            return response
    
    def __init__(self, module):
        self.params = module.test_data__['HTTPClientMock']
    
    def connect(self):
        return self.HTTPConnectionMock(self.params)
