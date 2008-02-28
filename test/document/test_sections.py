#!/usr/bin/env python
import os
from unittest import TestCase
from StringIO import StringIO

from rtfng.Elements import Document
from rtfng.document.section import Section

def getDocAndFirstSection():
    doc = Document()
    section = Section()
    doc.Sections.append(section)
    return (doc, section)

class SectionTestCase(TestCase) :
    """
    This class may look like it's doing a bit of magic, so let me explain:

        * an external script needs to be able to call methods on this class to
          get the generated RTF data;
        * there's no reason the script and the tests can't make use of the same
          RTF-generating code;
        * these two give us the 'make_*()' methods;
        * each test that is run knows it's own name (e.g., the test runner
          keeps track of each test and what it's called);
        * thus, the appropriate make_ method can be determined by the test
          method that called it (as long as we name them with the same suffix);
        * also, since the name is all that is needed to get the reference data
          (since we're also naming the reference files with that same suffix),
          that can be implemented generally too;
        * with all of this generalization, there's no need to have any
          test-specific code in the test_*() methods, so that can all make the
          same call (the only thing that changes is the name, and only the name
          is needed to generate/get the necessary data).
    """
    def setUp(self):
        base = ('test', 'sources', 'rtfng')
        self.sourceDir = os.path.join(*base)

    def getReferenceData(self, name):
        fh = open(os.path.join(self.sourceDir, name + '.rtf'))
        data = fh.read()
        fh.close()
        return data

    def getData(self):
        name = self._TestCase__testMethodName.split('test_')[1]
        doc, section = getattr(self, 'make_%s' % name)()
        result = StringIO()
        doc.write(result)
        testData = result.getvalue()
        refData = self.getReferenceData(name)
        return (testData, refData)

    def make_sectionEmpty():
        """
        Used by a script to generate docs.
        """
        return getDocAndFirstSection()
    make_sectionEmpty = staticmethod(make_sectionEmpty)

    def doTest(self):
        testData, refData = self.getData()
        self.assertEqual(testData, refData)

    def test_sectionEmpty(self):
        self.doTest()

    def make_sectionWithSmallPara():
        doc, section = getDocAndFirstSection()
        # text can be added directly to the section a paragraph object is
        # create as needed
        section.append('Small paragraph.')
        return (doc, section)
    make_sectionWithSmallPara = staticmethod(make_sectionWithSmallPara)

    def test_sectionWithSmallPara(self):
        self.doTest()

    def make_sectionWithBlankPara():
        doc, section = getDocAndFirstSection()
        section.append('Small paragraph.')
        # blank paragraphs are just empty strings
        section.append('')
        return (doc, section)
    make_sectionWithBlankPara = staticmethod(make_sectionWithBlankPara)

    def test_sectionWithBlankPara(self):
        self.doTest()

    def test_sectionWithParas(self):
        doc, section = getDocAndFirstSection()
        section.append('Small paragraph.')
        section.append('')
        # a lot of useful documents can be created with little more than this
        section.append(
            'A lot of useful documents can be created in this way, more '
            'advance formating is available but a lot of users just want to '
            'see their data come out in something other than a text file.')
