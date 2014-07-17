class AnsibleModuleMock:
    def __init__(self, argument_spec, bypass_checks=False, no_log=False,
            check_invalid_arguments=True, mutually_exclusive=None, required_together=None,
            required_one_of=None, add_file_common_args=False, supports_check_mode=False):
        
        self.params = {}
        self.test_data__ = {}
        
        for k,v in argument_spec.items():
            if 'default' in v:
                if v['type'] == 'bool':
                    self.params[k] = True if v['default'] == 'yes' else False
                else:
                    self.params[k] = v['default']
    
    def exit_json(self, *args, **kwargs):
        callback = self.test_data__['callback'] or {}
        callback = callback['exit']
        if callback:
            callback(*args, **kwargs)
    
    def fail_json(self, *args, **kwargs):
        callback = self.test_data__['callback'] or {}
        callback = callback['fail']
        if callback:
            callback(*args, **kwargs)
    
    def get_bin_path(self, arg, required=False, opt_dirs=[]):
        return arg
     
    def run_command(self, args, check_rc=False, close_fds=False, executable=None, data=None, binary_data=False, path_prefix=None, cwd=None, use_unsafe_shell=False):
        callback = self.test_data__['command']
        if callback:
            return callback(args)
        return (0,'','')
