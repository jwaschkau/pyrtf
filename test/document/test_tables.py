#!/usr/bin/env python

from rtfng.utils import RTFTestCase
from rtfng.Elements import Document

from rtfng.document.section import Section
from rtfng.document.paragraph import Cell, Paragraph, Table
from rtfng.PropertySets import BorderPropertySet, FramePropertySet, TabPropertySet

def initializeDoc():
    doc = Document()
    section = Section()
    doc.Sections.append(section)
    return (doc, section, doc.StyleSheet)

class TableTestCase(RTFTestCase):
 
    def make_tables():
        doc, section, styles = initializeDoc()
        p = Paragraph( styles.ParagraphStyles.Heading1 )
        p.append( 'Example 3' )
        section.append( p )

        # changes what is now the default style of Heading1 back to Normal
        p = Paragraph( styles.ParagraphStyles.Normal )
        p.append( 'Example 3 demonstrates tables, tables represent one of the '
                  'harder things to control in RTF as they offer alot of '
                  'flexibility in formatting and layout.' )
        section.append( p )

        section.append( 'Table columns are specified in widths, the following example '
                        'consists of a table with 3 columns, the first column is '
                        '7 tab widths wide, the next two are 3 tab widths wide. '
                        'The widths chosen are arbitrary, they do not have to be '
                        'multiples of tab widths.' )

        table = Table( TabPropertySet.DEFAULT_WIDTH * 7,
                       TabPropertySet.DEFAULT_WIDTH * 3,
                       TabPropertySet.DEFAULT_WIDTH * 3 )
        c1 = Cell( Paragraph( 'Row One, Cell One'   ) )
        c2 = Cell( Paragraph( 'Row One, Cell Two'   ) )
        c3 = Cell( Paragraph( 'Row One, Cell Three' ) )
        table.AddRow( c1, c2, c3 )

        c1 = Cell( Paragraph( styles.ParagraphStyles.Heading2, 'Heading2 Style'   ) )
        c2 = Cell( Paragraph( styles.ParagraphStyles.Normal, 'Back to Normal Style'   ) )
        c3 = Cell( Paragraph( 'More Normal Style' ) )
        table.AddRow( c1, c2, c3 )

        c1 = Cell( Paragraph( styles.ParagraphStyles.Heading2, 'Heading2 Style'   ) )
        c2 = Cell( Paragraph( styles.ParagraphStyles.Normal, 'Back to Normal Style'   ) )
        c3 = Cell( Paragraph( 'More Normal Style' ) )
        table.AddRow( c1, c2, c3 )

        section.append( table )
        section.append( 'Different frames can also be specified for each cell in the table '
                        'and each frame can have a different width and style for each border.' )

        thin_edge  = BorderPropertySet( width=20, style=BorderPropertySet.SINGLE )
        thick_edge = BorderPropertySet( width=80, style=BorderPropertySet.SINGLE )

        thin_frame  = FramePropertySet( thin_edge,  thin_edge,  thin_edge,  thin_edge )
        thick_frame = FramePropertySet( thick_edge, thick_edge, thick_edge, thick_edge )
        mixed_frame = FramePropertySet( thin_edge,  thick_edge, thin_edge,  thick_edge )

        table = Table( TabPropertySet.DEFAULT_WIDTH * 3, TabPropertySet.DEFAULT_WIDTH * 3, TabPropertySet.DEFAULT_WIDTH * 3 )
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

        p = Paragraph( styles.ParagraphStyles.Normal, thin_frame )
        p.append( 'This whole paragraph is in a frame.' )
        section.append( p )
        return doc

    make_tables = staticmethod(make_tables)

    def test_tables(self):
        self.doTest()

