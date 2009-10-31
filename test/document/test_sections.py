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
