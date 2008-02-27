import unittest
import doctest

# to add a new module to the test runner, simply include is in the list below:
modules = [
    'rtfng.parser.grammar',
    'rtfng.parser.base',
]

def importModule(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

suite = unittest.TestSuite()
for modname in modules:
    mod = importModule(modname)
    suite.addTest(doctest.DocTestSuite(mod))

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


