import imp
import os
import sys
import unittest

if __name__ == '__main__':
    current_dir = os.path.dirname(__file__)
    root_dir = os.path.join(current_dir, '..')
    units_dir = os.path.join(current_dir, 'units')
    
    sys.path.append(root_dir)
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    
    def add_test(suite, file):
        if os.path.isfile(file) and file.endswith('_test.py'):
            module = imp.load_source(os.path.splitext(file)[0], file)
            suite.addTest(loader.loadTestsFromModule(module))
    
    sys.argv.pop(0)
    
    if len(sys.argv) == 0:
        for file in os.listdir(units_dir):
            file = os.path.join(units_dir, file)
            add_test(suite, file)
    else:
        for file in sys.argv:
            file = os.path.abspath(file)
            file = file.replace(os.path.abspath(os.curdir)+'/','')
            add_test(suite, file)
    
    unittest.TextTestRunner(verbosity=2).run(suite)
