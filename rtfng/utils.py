"""
Utility functions for rtf-ng.
"""
import os
from unittest import TestCase
from StringIO import StringIO

def importModule(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def fileIsTest(path, skipFiles=[]):
    if not os.path.isfile(path):
        return False
    filename = os.path.basename(path)
    if filename in skipFiles:
        return False
    if filename.startswith('test') and filename.endswith('.py'):
        return True

def find(start, func, skip=[]):
    for item in [os.path.join(start, x) for x in os.listdir(start)]:
        if func(item, skip):
            yield item
        if os.path.isdir(item):
            for subItem in find(item, func, skip):
                yield subItem

def findTests(startDir, skipFiles=[]):
    return find(startDir, fileIsTest, skipFiles)

class RTFTestCase(TestCase):

    def setUp(self):
        base = ('test', 'sources', 'rtfng')
        self.sourceDir = os.path.join(*base)

    def getReferenceData(self, name):
        fh = open(os.path.join(self.sourceDir, name + '.rtf'))
        data = fh.read()
        fh.close()
        return data

    def getTestName(self):
        #import pdb;pdb.set_trace()
        if hasattr(self, '_testMethodName'):
            return self._testMethodName.split('test_')[1]
        return self._TestCase__testMethodName.split('test_')[1]

    def getTestData(self, doc):
        result = StringIO()
        doc.write(result)
        testData = result.getvalue()
        result.close()
        return testData

    def callMake(self):
        return getattr(self, 'make_%s' % self.getTestName())()

    def getData(self):
        name = self.getTestName()
        doc = self.callMake()
        testData = self.getTestData(doc)
        refData = self.getReferenceData(name)
        return (testData, refData)

    def doTest(self):
        testData, refData = self.getData()
        self.assertEqual(testData, refData)

