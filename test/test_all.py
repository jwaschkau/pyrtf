import unittest

from test_doctests import suite as doctestSuite

suites = unittest.TestSuite([doctestSuite])
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suites)
