#!/usr/bin/env python

import sys
sys.path.append( '../' )

from rtfng import *

def MakeExample4() :
    doc     = Document()
    ss      = doc.StyleSheet
    section = Section()
    doc.Sections.append( section )

    section.append( 'Example 4' )
    section.append( 'This example test changing the colour of fonts.' )

    #
    #    text properties can be specified in two ways, either a
    #    Text object can have its text properties specified like:
    tps = TextPS( colour=ss.Colours.Red )
    text = Text( 'RED', tps )
    p = Paragraph()
    p.append( 'This next word should be in ', text )
    section.append( p )

    #    or the shortcut TEXT function can be used like:
    p = Paragraph()
    p.append( 'This next word should be in ', TEXT( 'Green', colour=ss.Colours.Green ) )
    section.append( p )

    #    when specifying colours it is important to use the colours from the
    #    style sheet supplied with the document and not the StandardColours object
    #    each document get its own copy of the stylesheet so that changes can be
    #    made on a document by document basis without mucking up other documents
    #    that might be based on the same basic stylesheet

    return doc


def OpenFile( name ) :
    return file( '%s.rtf' % name, 'w' )

if __name__ == '__main__' :
    DR = Renderer()

    doc4 = MakeExample4()

    DR.Write( doc4, OpenFile( '4' ) )

    print "Finished"
