#!/usr/bin/env python
from rtfng.utils import RTFTestCase
from rtfng.Elements import Document

def initializeDoc():
    doc = Document()
    section = Section()
    doc.Sections.append(section)
    return (doc, section, doc.StyleSheet)

class CharacterTestCase(RTFTestCase):
    def make_char():
        doc, section, styles = initializeDoc()
        p = Paragraph()
        p.append('It is also possible to provide overrides for element of a style. ',
                  'For example I can change just the font ',
                  TEXT('size', size=48),
                  ' or ',
                  TEXT('typeface', font=styles.Fonts.Impact) ,
                  '.')
        section.append(p)
        return doc
    make_char = staticmethod(make_char)

    def make_char():
        doc, section, styles = initializeDoc()

        section.append('Example 4')
        section.append('This example test changing the colour of fonts.')

        #
        #    text properties can be specified in two ways, either a
        #    Text object can have its text properties specified like:
        tps = TextPropertySet(colour=ss.Colours.Red)
        text = Text('RED', tps)
        p = Paragraph()
        p.append('This next word should be in ', text)
        section.append(p)
        return doc
    make_char = staticmethod(make_char)

    def make_char():
        doc, section, styles = initializeDoc()

        #    or the shortcut TEXT function can be used like:
        p = Paragraph()
        p.append('This next word should be in ', TEXT('Green', colour=ss.Colours.Green))
        section.append(p)

        #    when specifying colours it is important to use the colours from the
        #    style sheet supplied with the document and not the StandardColours object
        #    each document get its own copy of the stylesheet so that changes can be
        #    made on a document by document basis without mucking up other documents
        #    that might be based on the same basic stylesheet

        return doc
    make_char = staticmethod(make_char)
