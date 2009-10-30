#!/usr/bin/env python
from rtfng.utils import RTFTestCase
from rtfng.Elements import Document
from rtfng.document.section import Section

def initializeDoc():
    doc = Document()
    section = Section()
    doc.Sections.append(section)
    return (doc, section)

class SectionTestCase(RTFTestCase):
    """
    This class may look like it's doing a bit of magic, so let me explain:

        * an external script needs to be able to call methods on this class to
          get the generated RTF data;
        * there's no reason the script and the tests can't make use of the same
          RTF-generating code;
        * these two facts are the reason for the 'make_*()' methods;
        * each test that is run knows it's own name (e.g., the test runner
          keeps track of each test and what it's called);
        * thus, the appropriate make_ method can be determined by the test
          method that called it (as long as we name them with the same suffix);
        * also, since the name is all that is needed to get the reference data
          (since we're also naming the reference files with that same suffix),
          that can be determined without hard-coding filenames;
        * with all of these facts, we can generalize some code since there's no
          need to have any test-specific code in the test_*() methods;
        * this means that each test method can make the same, parameterless
          doTest() call (the only thing that changes is the name, and only the
          name is needed to generate/get the necessary data).
    """
    def make_sectionEmpty():
        """
        Used by a script to generate docs.
        """
        return initializeDoc()[0]
    make_sectionEmpty = staticmethod(make_sectionEmpty)

    def test_sectionEmpty(self):
        self.doTest()

    def make_sectionWithSmallPara():
        doc, section = initializeDoc()
        # text can be added directly to the section a paragraph object is
        # create as needed
        section.append('Small paragraph.')
        return doc
    make_sectionWithSmallPara = staticmethod(make_sectionWithSmallPara)

    def test_sectionWithSmallPara(self):
        self.doTest()

    def make_sectionWithBlankPara():
        doc, section = initializeDoc()
        section.append('Small paragraph.')
        # blank paragraphs are just empty strings
        section.append('')
        return doc
    make_sectionWithBlankPara = staticmethod(make_sectionWithBlankPara)

    def test_sectionWithBlankPara(self):
        self.doTest()

    def make_sectionWithParas():
        doc, section = initializeDoc()
        section.append('Small paragraph.')
        section.append('')
        # a lot of useful documents can be created with little more than this
        section.append(
            'A lot of useful documents can be created in this way. More '
            'advanced formatting is available, but a lot of users just want '
            'to see their data in something other than a text file.')
        return doc
    make_sectionWithParas = staticmethod(make_sectionWithParas)

    def test_sectionWithParas(self):
        self.doTest()
