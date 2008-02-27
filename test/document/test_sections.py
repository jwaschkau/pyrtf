#!/usr/bin/env python
from unittest import TestCase

from rtfng import *

class SimpleSectionsTestCase(TestCase):
    def test_trueTest(self):
        self.assertEqual(1,1)
    def test_falseTest(self):
        self.assertEqual(0,1)

def MakeExample1() :
    doc     = Document()
    ss      = doc.StyleSheet
    section = Section()
    doc.Sections.append( section )

    #    text can be added directly to the section
    #    a paragraph object is create as needed
    section.append( 'Example 1' )

    #    blank paragraphs are just empty strings
    section.append( '' )

    #    a lot of useful documents can be created
    #    with little more than this
    section.append( 'A lot of useful documents can be created '
                    'in this way, more advance formating is available '
                    'but a lot of users just want to see their data come out '
                    'in something other than a text file.' )
    return doc

def OpenFile( name ) :
    return file( '%s.rtf' % name, 'w' )

if __name__ == '__main__' :
    DR = Renderer()

    doc1 = MakeExample1()

    DR.Write( doc1, OpenFile( '1' ) )

    print "Finished"

