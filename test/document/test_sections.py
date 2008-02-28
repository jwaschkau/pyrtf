#!/usr/bin/env python
from unittest import TestCase
from StringIO import StringIO

from rtfng.Elements import Document
from rtfng.document.section import Section

class SectionTestCase(TestCase) :

    def getDocAndFirstSection(self):
        doc = Document()
        section = Section()
        doc.Sections.append(section)
        return (doc, section)

    def test_sectionEmpty(self):
        doc, section = self.getDocAndFirstSection()
        result = StringIO()
        doc.write(result)
        self.assertEqual('', result.getvalue())

    def test_sectionWithSmallPara(self):
        doc, section = self.getDocAndFirstSection()
        # text can be added directly to the section a paragraph object is
        # create as needed
        section.append('Small paragraph.')

    def test_sectionWithBlankPara(self):
        doc, section = self.getDocAndFirstSection()
        section.append('Small paragraph.')
        # blank paragraphs are just empty strings
        section.append('')

    def test_sectionWithParas(self):
        doc, section = self.getDocAndFirstSection()
        section.append('Small paragraph.')
        section.append('')
        # a lot of useful documents can be created with little more than this
        section.append(
            'A lot of useful documents can be created in this way, more '
            'advance formating is available but a lot of users just want to '
            'see their data come out in something other than a text file.')
