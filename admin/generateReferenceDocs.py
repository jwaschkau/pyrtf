#!/usr/bin/env python
"""
This script introspects the RTF unit tests and generates the files that are
used for comparison when running those tests.

WARNING! Only run this script after manually verifying that the documents
created by the tests are correct, otherwise the tests will be useless.

Once verified and generated, these docs will be used in the unit tests as the
correct output. Thus any changes introduced into the code base that affect how
these docs are rendered may cause the tests to fail. For buggy code, this is
exactly what we want. For new features, we need to update the unit tests,
verify that they create the correct output, and then regenerate the reference
docs.
"""
import os
from unittest import TestCase

from rtfng.utils import findTests, importModule

from test.test_all import searchDirs, skipFiles

base = ['test', 'sources', 'rtfng']
pending = base + ['pending']
baseDir = os.path.join(*base)
pendingDir = os.path.join(*pending)

# iterate through the test files
for startDir in searchDirs:
    for testFile in findTests(startDir, skipFiles):
            modBase = os.path.splitext(testFile)[0]
            name = modBase.replace(os.path.sep, '.')
            # import the testFile as a module
            mod = importModule(name)
            # iterate through module objects, checking for TestCases
            for objName in dir(mod):
                if not objName.endswith('TestCase'):
                    continue
                obj = getattr(mod, objName)
                if not issubclass(obj, TestCase):
                    continue
                # iterate through the TestCase attrs, looking for make_*
                # methods
                for attrName in dir(obj):
                    if attrName.startswith('make_'):
                        filename = attrName.split('make_')[1] + '.rtf'
                        #import pdb;pdb.set_trace()
                        doc, ign = getattr(obj, attrName)()
                        fh = open(os.path.join(pendingDir, filename), 'w+')
                        doc.write(fh)
                        fh.close()

# write to the review directory if in validate mode, write to the sources dir
# if in generate mode
