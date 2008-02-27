#!/usr/bin/env python

import sys
sys.path.append( '../' )

from rtfng import *

def MakeExample3() :
    doc     = Document()
    ss      = doc.StyleSheet
    section = Section()
    doc.Sections.append( section )

    p = Paragraph( ss.ParagraphStyles.Heading1 )
    p.append( 'Example 3' )
    section.append( p )

    # changes what is now the default style of Heading1 back to Normal
    p = Paragraph( ss.ParagraphStyles.Normal )
    p.append( 'Example 3 demonstrates tables, tables represent one of the '
              'harder things to control in RTF as they offer alot of '
              'flexibility in formatting and layout.' )
    section.append( p )

    section.append( 'Table columns are specified in widths, the following example '
                    'consists of a table with 3 columns, the first column is '
                    '7 tab widths wide, the next two are 3 tab widths wide. '
                    'The widths chosen are arbitrary, they do not have to be '
                    'multiples of tab widths.' )

    table = Table( TabPS.DEFAULT_WIDTH * 7,
                   TabPS.DEFAULT_WIDTH * 3,
                   TabPS.DEFAULT_WIDTH * 3 )
    c1 = Cell( Paragraph( 'Row One, Cell One'   ) )
    c2 = Cell( Paragraph( 'Row One, Cell Two'   ) )
    c3 = Cell( Paragraph( 'Row One, Cell Three' ) )
    table.AddRow( c1, c2, c3 )

    c1 = Cell( Paragraph( ss.ParagraphStyles.Heading2, 'Heading2 Style'   ) )
    c2 = Cell( Paragraph( ss.ParagraphStyles.Normal, 'Back to Normal Style'   ) )
    c3 = Cell( Paragraph( 'More Normal Style' ) )
    table.AddRow( c1, c2, c3 )

    c1 = Cell( Paragraph( ss.ParagraphStyles.Heading2, 'Heading2 Style'   ) )
    c2 = Cell( Paragraph( ss.ParagraphStyles.Normal, 'Back to Normal Style'   ) )
    c3 = Cell( Paragraph( 'More Normal Style' ) )
    table.AddRow( c1, c2, c3 )

    section.append( table )
    section.append( 'Different frames can also be specified for each cell in the table '
                    'and each frame can have a different width and style for each border.' )

    thin_edge  = BorderPS( width=20, style=BorderPS.SINGLE )
    thick_edge = BorderPS( width=80, style=BorderPS.SINGLE )

    thin_frame  = FramePS( thin_edge,  thin_edge,  thin_edge,  thin_edge )
    thick_frame = FramePS( thick_edge, thick_edge, thick_edge, thick_edge )
    mixed_frame = FramePS( thin_edge,  thick_edge, thin_edge,  thick_edge )

    table = Table( TabPS.DEFAULT_WIDTH * 3, TabPS.DEFAULT_WIDTH * 3, TabPS.DEFAULT_WIDTH * 3 )
    c1 = Cell( Paragraph( 'R1C1' ), thin_frame )
    c2 = Cell( Paragraph( 'R1C2' ) )
    c3 = Cell( Paragraph( 'R1C3' ), thick_frame )
    table.AddRow( c1, c2, c3 )

    c1 = Cell( Paragraph( 'R2C1' ) )
    c2 = Cell( Paragraph( 'R2C2' ) )
    c3 = Cell( Paragraph( 'R2C3' ) )
    table.AddRow( c1, c2, c3 )

    c1 = Cell( Paragraph( 'R3C1' ), mixed_frame )
    c2 = Cell( Paragraph( 'R3C2' ) )
    c3 = Cell( Paragraph( 'R3C3' ), mixed_frame )
    table.AddRow( c1, c2, c3 )

    section.append( table )

    section.append( 'In fact frames can be applied to paragraphs too, not just cells.' )

    p = Paragraph( ss.ParagraphStyles.Normal, thin_frame )
    p.append( 'This whole paragraph is in a frame.' )
    section.append( p )
    return doc

def OpenFile( name ) :
    return file( '%s.rtf' % name, 'w' )

if __name__ == '__main__' :
    DR = Renderer()

    doc3 = MakeExample3()

    DR.Write( doc3, OpenFile( '3' ) )

    print "Finished"
