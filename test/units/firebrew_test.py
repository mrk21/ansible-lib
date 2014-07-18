import os
import unittest
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from firebrew import *
from test_double.ansible_module_mock import *

class FirebrewTest(unittest.TestCase):
    def setUp(self):
        self.instance = Firebrew(AnsibleModuleMock)
    
    def test_build_command(self):
        self.instance.module.params = {
            'state': 'present',
            'name': 'name',
            'base_dir': '',
            'profile': None,
            'firefox': '   ',
        }
        self.assertEquals(self.instance.build_command(), 'firebrew install name')
    
    def test_build_command__With_options(self):
        self.instance.module.params = {
            'state': 'absent',
            'name': 'extension name',
            'base_dir': 'dir',
            'profile': 'profile',
            'firefox': 'path to/firefox',
        }
        self.assertEquals(self.instance.build_command(), "firebrew uninstall 'extension name' --base-dir=dir --profile=profile --firefox='path to/firefox'")
    
    def assert_execute(self, params, callbacks):
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
        
        self.instance.module.params = params
        self.instance.execute()
        self.assertEqual(called['exit'], 'exit' in callbacks)
        self.assertEqual(called['fail'], 'fail' in callbacks)
    
    def test_execute__When_the_state_was_present_and_the_target_extension_not_existed(self):
        def exit(*args, **kwargs):
            self.assertEqual(kwargs['changed'], True)
        
        def command(args):
            self.assertEqual(args, 'firebrew install Vimperator')
            return (Firebrew.STATUS_SUCCESS,'','')
        
        self.assert_execute({'state': 'present', 'name': 'Vimperator'},{'exit': exit, 'command': command})
    
    def test_execute__When_the_state_was_present_and_the_target_extension_was_already_installed(self):
        def exit(*args, **kwargs):
            self.assertEqual(kwargs['changed'], False)
        
        def command(args):
            self.assertEqual(args, 'firebrew install Vimperator')
            return (Firebrew.STATUS_NOT_CHANGED,'','')
        
        self.assert_execute({'state': 'present', 'name': 'Vimperator'},{'exit': exit, 'command': command})
    
    def test_execute__When_the_state_was_present_and_the_command_was_failed(self):
        def fail(*args, **kwargs):
            self.assertEqual(kwargs['msg'], 'firebrew error message')
        
        def command(args):
            self.assertEqual(args, 'firebrew install Vimperator')
            return (Firebrew.STATUS_FAILURE,'','firebrew error message')
        
        self.assert_execute({'state': 'present', 'name': 'Vimperator'},{'fail': fail, 'command': command})
    
    def test_execute__When_the_state_was_absent_and_the_target_extension_existed(self):
        def exit(*args, **kwargs):
            self.assertEqual(kwargs['changed'], True)
        
        def command(args):
            self.assertEqual(args, 'firebrew uninstall Vimperator')
            return (Firebrew.STATUS_SUCCESS,'','')
        
        self.assert_execute({'state': 'absent', 'name': 'Vimperator'},{'exit': exit, 'command': command})
    
    def test_execute__When_the_state_was_absent_and_the_target_extension_not_existed(self):
        def exit(*args, **kwargs):
            self.assertEqual(kwargs['changed'], False)
        
        def command(args):
            self.assertEqual(args, 'firebrew uninstall Vimperator')
            return (Firebrew.STATUS_NOT_CHANGED,'','')
        
        self.assert_execute({'state': 'absent', 'name': 'Vimperator'},{'exit': exit, 'command': command})
    
    def test_execute__When_the_state_was_absent_and_the_command_was_failed(self):
        def fail(*args, **kwargs):
            self.assertEqual(kwargs['msg'], 'firebrew error message')
        
        def command(args):
            self.assertEqual(args, 'firebrew uninstall Vimperator')
            return (Firebrew.STATUS_FAILURE,'','firebrew error message')
        
        self.assert_execute({'state': 'absent', 'name': 'Vimperator'},{'fail': fail, 'command': command})


suite = unittest.TestLoader().loadTestsFromTestCase(FirebrewTest)
unittest.TextTestRunner(verbosity=2).run(suite)
