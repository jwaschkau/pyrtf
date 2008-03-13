from rtfng.utils import RTFTestCase
from rtfng.Elements import Document

from rtfng.document.section import Section

def initializeDoc():
    doc = Document()
    section = Section()
    doc.Sections.append(section)
    return (doc, section, doc.StyleSheet)

class ParagraphTestCase(RTFTestCase):

    def make_():
        pass

def MakeExample5() :
    doc     = Document()
    ss      = doc.StyleSheet
    section = Section()
    doc.Sections.append( section )

    section.Header.append( 'This is the header' )
    section.Footer.append( 'This is the footer' )

    p = Paragraph( ss.ParagraphStyles.Heading1 )
    p.append( 'Example 5' )
    section.append( p )

    #    blank paragraphs are just empty strings
    section.append( '' )

    p = Paragraph( ss.ParagraphStyles.Normal )
    p.append( 'This document has a header and a footer.' )
    section.append( p )

    return doc

def MakeExample6() :
    doc     = Document()
    ss      = doc.StyleSheet
    section = Section()
    doc.Sections.append( section )

    section.FirstHeader.append( 'This is the header for the first page.' )
    section.FirstFooter.append( 'This is the footer for the first page.' )

    section.Header.append( 'This is the header that will appear on subsequent pages.' )
    section.Footer.append( 'This is the footer that will appear on subsequent pages.' )

    p = Paragraph( ss.ParagraphStyles.Heading1 )
    p.append( 'Example 6' )
    section.append( p )

    #    blank paragraphs are just empty strings
    section.append( '' )

    p = Paragraph( ss.ParagraphStyles.Normal )
    p.append( 'This document has different headers and footers for the first and then subsequent pages. '
              'If you insert a page break you should see a different header and footer.' )
    section.append( p )

    return doc

def MakeExample7() :
    doc     = Document()
    ss      = doc.StyleSheet
    section = Section()
    doc.Sections.append( section )

    section.FirstHeader.append( 'This is the header for the first page.' )
    section.FirstFooter.append( 'This is the footer for the first page.' )

    section.Header.append( 'This is the header that will appear on subsequent pages.' )
    section.Footer.append( 'This is the footer that will appear on subsequent pages.' )

    p = Paragraph( ss.ParagraphStyles.Heading1 )
    p.append( 'Example 7' )
    section.append( p )

    p = Paragraph( ss.ParagraphStyles.Normal )
    p.append( 'This document has different headers and footers for the first and then subsequent pages. '
              'If you insert a page break you should see a different header and footer.' )
    section.append( p )

    p = Paragraph( ss.ParagraphStyles.Normal, ParagraphPropertySet().SetPageBreakBefore( True ) )
    p.append( 'This should be page 2 '
              'with the subsequent headers and footers.' )
    section.append( p )

    section = Section( break_type=Section.PAGE, first_page_number=1 )
    doc.Sections.append( section )

    section.FirstHeader.append( 'This is the header for the first page of the second section.' )
    section.FirstFooter.append( 'This is the footer for the first page of the second section.' )

    section.Header.append( 'This is the header that will appear on subsequent pages for the second section.' )
    p = Paragraph( 'This is the footer that will appear on subsequent pages for the second section.', LINE )
    p.append( PAGE_NUMBER, ' of ', SECTION_PAGES )
    section.Footer.append( p )

    section.append( 'This is the first page' )

    p = Paragraph( ParagraphPropertySet().SetPageBreakBefore( True ), 'This is the second page' )
    section.append( p )

    return doc


