import os
import unittest
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../library'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from firebrew import *
from test_double.ansible_module_mock import *

class FirebrewTest(unittest.TestCase):
    def setUp(self):
        self.instance = Firebrew(AnsibleModuleMock)
    
    def assertion(self, params, callbacks):
        called = {'exit': False, 'fail': False}
        
        def exit_callback(*args, **kwargs):
            called['exit'] = True
            if 'exit' in callbacks:
                callbacks['exit'](*args, **kwargs)
        
        def fail_callback(*args, **kwargs):
            called['fail'] = True
            if 'fail' in callbacks:
                callbacks['fail'](*args, **kwargs)
        
        self.instance.module.test_data__ = {
            'callback': {'exit': exit_callback, 'fail': fail_callback},
            'command': callbacks['command']
        }
        
        self.instance.module.params['state'] = params['state']
        self.instance.module.params['name'] = params['name']
        self.instance.execute()
        self.assertEqual(called['exit'], 'exit' in callbacks)
        self.assertEqual(called['fail'], 'fail' in callbacks)
    
    def test_When_the_state_was_present_and_the_target_extension_not_existed__the_execute_method_should_return_changed_is_True(self):
        def exit(*args, **kwargs):
            self.assertEqual(kwargs['changed'], True)
        
        def command(args):
            self.assertEqual(args, 'firebrew install Vimperator')
            return (Firebrew.STATUS_SUCCESS,'','')
        
        self.assertion({'state': 'present', 'name': 'Vimperator'},{'exit': exit, 'command': command})
    
    def test_When_the_state_was_present_and_the_target_extension_was_already_installed__the_execute_method_should_return_changed_is_False(self):
        def exit(*args, **kwargs):
            self.assertEqual(kwargs['changed'], False)
        
        def command(args):
            self.assertEqual(args, 'firebrew install Vimperator')
            return (Firebrew.STATUS_NOT_CHANGED,'','')
        
        self.assertion({'state': 'present', 'name': 'Vimperator'},{'exit': exit, 'command': command})
    
    def test_When_the_state_was_present_and_the_command_was_failed__the_execute_method_should_return_failure(self):
        def fail(*args, **kwargs):
            self.assertEqual(kwargs['msg'], 'firebrew error message')
        
        def command(args):
            self.assertEqual(args, 'firebrew install Vimperator')
            return (Firebrew.STATUS_FAILURE,'','firebrew error message')
        
        self.assertion({'state': 'present', 'name': 'Vimperator'},{'fail': fail, 'command': command})
    
    def test_When_the_state_was_absent_and_the_target_extension_existed__the_execute_method_should_return_changed_is_True(self):
        def exit(*args, **kwargs):
            self.assertEqual(kwargs['changed'], True)
        
        def command(args):
            self.assertEqual(args, 'firebrew uninstall Vimperator')
            return (Firebrew.STATUS_SUCCESS,'','')
        
        self.assertion({'state': 'absent', 'name': 'Vimperator'},{'exit': exit, 'command': command})
    
    def test_When_the_state_was_absent_and_the_target_extension_not_existed__the_execute_method_should_return_changed_is_False(self):
        def exit(*args, **kwargs):
            self.assertEqual(kwargs['changed'], False)
        
        def command(args):
            self.assertEqual(args, 'firebrew uninstall Vimperator')
            return (Firebrew.STATUS_NOT_CHANGED,'','')
        
        self.assertion({'state': 'absent', 'name': 'Vimperator'},{'exit': exit, 'command': command})
    
    def test_When_the_state_was_absent_and_the_command_was_failed__the_execute_method_should_return_failure(self):
        def fail(*args, **kwargs):
            self.assertEqual(kwargs['msg'], 'firebrew error message')
        
        def command(args):
            self.assertEqual(args, 'firebrew uninstall Vimperator')
            return (Firebrew.STATUS_FAILURE,'','firebrew error message')
        
        self.assertion({'state': 'absent', 'name': 'Vimperator'},{'fail': fail, 'command': command})


suite = unittest.TestLoader().loadTestsFromTestCase(FirebrewTest)
unittest.TextTestRunner(verbosity=2).run(suite)
