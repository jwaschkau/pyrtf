#!/usr/bin/env python

import sys
sys.path.append( '../' )

from rtfng import *

SAMPLE_PARA = """The play opens one year after the death of Richard II, and
King Henry is making plans for a crusade to the Holy Land to cleanse himself
of the guilt he feels over the usurpation of Richard's crown. But the crusade
must be postponed when Henry learns that Welsh rebels, led by Owen Glendower,
have defeated and captured Mortimer. Although the brave Henry Percy, nicknamed
Hotspur, has quashed much of the uprising, there is still much trouble in
Scotland. King Henry has a deep admiration for Hotspur and he longs for his
own son, Prince Hal, to display some of Hotspur's noble qualities. Hal is more
comfortable in a tavern than on the battlefield, and he spends his days
carousing with riff-raff in London. But King Henry also has his problems with
the headstrong Hotspur, who refuses to turn over his prisoners to the state as
he has been so ordered. Westmoreland tells King Henry that Hotspur has many of
the traits of his uncle, Thomas Percy, the Earl of Worcester, and defying
authority runs in the family."""

def MakeExample2() :
    doc     = Document()
    ss      = doc.StyleSheet
    section = Section()
    doc.Sections.append( section )

    #    things really only get interesting after you
    #    start to use styles to spice things up
    p = Paragraph( ss.ParagraphStyles.Heading1 )
    p.append( 'Example 2' )
    section.append( p )

    p = Paragraph( ss.ParagraphStyles.Normal )
    p.append( 'In this case we have used a two styles. '
              'The first paragraph is marked with the Heading1 style so that it '
              'will appear differently to the user. ')
    section.append( p )

    p = Paragraph()
    p.append( 'Notice that after I have changed the style of the paragraph '
              'all subsequent paragraphs have that style automatically. '
              'This saves typing and is the default behaviour for RTF documents.' )
    section.append( p )

    p = Paragraph()
    p.append( 'I also happen to like Arial so our base style is Arial not Times New Roman.' )
    section.append( p )

    p = Paragraph()
    p.append( 'It is also possible to provide overrides for element of a style. ',
              'For example I can change just the font ',
              TEXT( 'size', size=48 ),
              ' or ',
              TEXT( 'typeface', font=ss.Fonts.Impact ) ,
              '.' )
    section.append( p )

    p = Paragraph()
    p.append( 'The paragraph itself can also be overridden in lots of ways, tabs, '
              'borders, alignment, etc can all be modified either in the style or as an '
              'override during the creation of the paragraph. '
              'The next paragraph demonstrates custom tab widths and embedded '
              'carriage returns, ie new line markers that do not cause a paragraph break.' )
    section.append( p )

    #    ParagraphPS is an alias for ParagraphPropertySet
    para_props = ParagraphPS( tabs = [ TabPS( width=TabPS.DEFAULT_WIDTH     ),
                                       TabPS( width=TabPS.DEFAULT_WIDTH * 2 ),
                                       TabPS( width=TabPS.DEFAULT_WIDTH     ) ] )
    p = Paragraph( ss.ParagraphStyles.Normal, para_props )
    p.append( 'Left Word', TAB, 'Middle Word', TAB, 'Right Word', LINE,
              'Left Word', TAB, 'Middle Word', TAB, 'Right Word' )
    section.append( p )

    section.append( 'The alignment of tabs and style can also be controlled. '
                    'The following paragraph demonstrates how to use flush right tabs'
                    'and leader dots.' )

    para_props = ParagraphPS( tabs = [ TabPS( section.TwipsToRightMargin(),
                                              alignment = TabPS.RIGHT,
                                              leader    = TabPS.DOTS  ) ] )
    p = Paragraph( ss.ParagraphStyles.Normal, para_props )
    p.append( 'Before Dots', TAB, 'After Dots' )
    section.append( p )

    section.append( 'Paragraphs can also be indented, the following is all at the '
                    'same indent level and the one after it has the first line '
                    'at a different indent to the rest.  The third has the '
                    'first line going in the other direction and is also separated '
                    'by a page break.  Note that the '
                    'FirstLineIndent is defined as being the difference from the LeftIndent.' )

    section.append( 'The following text was copied from http://www.shakespeare-online.com/plots/1kh4ps.html.' )

    para_props = ParagraphPS()
    para_props.SetLeftIndent( TabPropertySet.DEFAULT_WIDTH *  3 )
    p = Paragraph( ss.ParagraphStyles.Normal, para_props )
    p.append( SAMPLE_PARA )
    section.append( p )

    para_props = ParagraphPS()
    para_props.SetFirstLineIndent( TabPropertySet.DEFAULT_WIDTH * -2 )
    para_props.SetLeftIndent( TabPropertySet.DEFAULT_WIDTH *  3 )
    p = Paragraph( ss.ParagraphStyles.Normal, para_props )
    p.append( SAMPLE_PARA )
    section.append( p )

    #    do a page
    para_props = ParagraphPS()
    para_props.SetPageBreakBefore( True )
    para_props.SetFirstLineIndent( TabPropertySet.DEFAULT_WIDTH )
    para_props.SetLeftIndent( TabPropertySet.DEFAULT_WIDTH )
    p = Paragraph( ss.ParagraphStyles.Normal, para_props )
    p.append( SAMPLE_PARA )
    section.append( p )

    return doc


def OpenFile( name ) :
    return file( '%s.rtf' % name, 'w' )

if __name__ == '__main__' :
    DR = Renderer()

    doc2 = MakeExample2()

    DR.Write( doc2, OpenFile( '2' ) )

    print "Finished"
