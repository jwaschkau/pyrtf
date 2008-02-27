"""
An RTF file has the following syntax:
<File>:  '{' <header> <document>'}'

The header has the following syntax:

<header>: \rtf <charset> \deff? <fonttbl> <filetbl>? <colortbl>? <stylesheet>?  <listtables>? <revtbl>?

The document area has the following syntax.
<document>:  <info>? <docfmt>* <section>+

Each section in the RTF file has the following syntax:
<section>:   <secfmt>* <hdrftr>? <para>+ (\sect <section>)?
"""
from pyparsing import Optional, Literal, Word, Group, White
from pyparsing import Suppress, Combine, replaceWith
from pyparsing import alphas, nums, printables, alphanums
from pyparsing import restOfLine, oneOf, OneOrMore, ZeroOrMore
from pyparsing import ParseException

class RTFError(Exception):
    pass

class RTFParseError(RTFError):
   "Unable to parse RTF data."

class RTFGrammar(object):
    """
    # get the grammar
    >>> grammar = RTFGrammar().getGrammar()

    # let's check out parsing of the opening controls
    >>> doc = r'''{\\rtf1\\ansi\\ansicpg1252\cocoartf949\cocoasubrtf270
    ... {\\fonttbl\\f0\\froman\\fcharset0 Times-Roman;}
    ... }'''
    >>> tokens = grammar.parseString(doc)
    >>> tokens.version
    '1'
    >>> tokens.characterSet
    'ansi'
    >>> tokens.codePage
    '1252'

    # now the font table, RTF v1.0
    >>> doc = r'''{\\rtf1\\ansi\\ansicpg1252\cocoartf949\cocoasubrtf270
    ... {\\fonttbl\\f0\\froman\\fcharset0 Times-Roman;}
    ... }'''
    >>> tokens = grammar.parseString(doc)
    >>> tokens.fonts[0].fontNumber
    '0'
    >>> tokens.fonts[0].fontFamily
    'roman'
    >>> tokens.fonts[0].fontCharSet
    '0'
    >>> tokens.fonts[0].fontName
    'Times-Roman'

    # with more fonts
    >>> doc = r'''{\\rtf1\\ansi\\ansicpg1252\cocoartf949\cocoasubrtf270
    ... {\\fonttbl\\f0\\froman\\fcharset0 Times-Roman;\\f1\\fswiss\\fcharset0 ArialMT;}
    ... }'''
    >>> tokens = grammar.parseString(doc)
    >>> for font in tokens.fonts:
    ...   print font.fontNumber, font.fontFamily, font.fontName
    0 roman Times-Roman
    1 swiss ArialMT

    # font table, RTF v1.2+
    >>> doc = r'''{\\rtf1\\ansi\\ansicpg1252\uc1
    ...   {\\fonttbl{\\f0\\froman\\fcharset0\\fprq2{\*\panose 02020603050405020304}Times New Roman;}
    ...   {\\f1\\fmodern\\fcharset0\\fprq1{\*\panose 02070309020205020404}Courier New;}
    ...   {\\f2\\froman\\fcharset2\\fprq2{\*\panose 05050102010706020507}Symbol;}}
    ...   }'''
    >>> tokens = grammar.parseString(doc)
    >>> for font in tokens.fonts:
    ...   print font.fontNumber, font.fontFamily, font.fontName, font.panose
    0 roman Times New Roman 02020603050405020304
    1 modern Courier New 02070309020205020404
    2 roman Symbol 05050102010706020507

    # font table with panose optional
    >>> doc = r'''{\\rtf1\\ansi\\ansicpg1252\uc1
    ...   {\\fonttbl{\\f0\\froman\\fcharset0\\fprq2{\*\panose 02020603050405020304}Times New Roman;}
    ...   {\\f1\\fmodern\\fcharset0\\fprq1{\*\panose 02070309020205020404}Courier New;}
    ...   {\\f2\\froman\\fcharset2\\fprq2{\*\panose 05050102010706020507}Symbol;}
    ...   {\\f3\\froman\\fcharset3\\fprq2 Times New Roman (Hebrew);}}
    ...   }'''
    >>> tokens = grammar.parseString(doc)
    >>> for font in tokens.fonts:
    ...   print font.fontNumber, font.fontFamily, font.fontName, font.panose or 0
    0 roman Times New Roman 02020603050405020304
    1 modern Courier New 02070309020205020404
    2 roman Symbol 05050102010706020507
    3 roman Times New Roman (Hebrew) 0
    """
    separator = Literal(';')
    space = Literal(' ')
    white = White()
    leftBracket = Literal('{')
    rightBracket = Literal('}')
    bracket = leftBracket | rightBracket.setResultsName('bracket')

    # basic RTF control codes, ie. "\labelname3434"
    controlLabel = Combine(Word(alphas + "'") + Optional(Word(nums)))
    controlValue = Optional(space) + Optional(Word(alphanums + '-'))
    baseControl = Combine(Literal('\\') + controlLabel + controlValue
                          ).setResultsName('baseControl')

    # in some cases (color and font table declarations), control has ';'
    # suffix
    rtfControl = Combine(baseControl + Optional(separator)
                         ).setResultsName('control')

    rtfGroup = leftBracket + OneOrMore(rtfControl) + rightBracket

    # opening controls
    rtfVersionNumber = Word(nums).setResultsName('version')
    rtfVersion = Combine(Literal('\\') + 'rtf') + rtfVersionNumber
    charSet = Literal('\\') + Word(alphas).setResultsName('characterSet')
    codePage = Literal('\\ansicpg') + Word(nums).setResultsName('codePage')

    # default font
    # XXX

    # get font table
    fontTableControl = Combine(Literal('\\') + 'fonttbl')
    fontNumber = Literal('\\f') + Word(nums).setResultsName('fontNumber')
    fontFamily = Literal('\\f') + Word(alphanums
                         ).setResultsName('fontFamily')
    fontCharSet = Literal('\\f' + 'charset') + Word(alphanums
                          ).setResultsName('fontCharSet')
    fontPitch = Literal('\\f' + 'prq') + oneOf('0 1 2'
                        ).setResultsName('fontPitch')
    panose = (leftBracket + Combine(Literal('\\*\\' + 'panose') + space) +
        Word(nums).setResultsName('panose') + rightBracket)
    fontName = Word(alphanums + '()- ').setResultsName('fontName')
    # font table RTF v1.0
    fontGroupCombined = Group(
        fontNumber + fontFamily + fontCharSet + Optional(space) +
        fontName + Optional(separator)
        )
    # font table RTF v1.2+
    fontGroupSeparate = Group(
        leftBracket +
        fontNumber + fontFamily + fontCharSet +
        Optional(fontPitch) + Optional(space) + Optional(panose) + # | space +
        fontName + separator +
        rightBracket
        )
    font = fontGroupCombined | fontGroupSeparate
    fontTable = (leftBracket + fontTableControl +
        OneOrMore(font).setResultsName('fonts') +
        rightBracket)

    # file table
    # XXX

    # color table
    # XXX

    # stylesheet
    # XXX

    # list table
    # XXX

    # revision table
    # XXX

    # document info
    # XXX

    # document format
    # XXX

    # section format
    # XXX

    # header/footer
    # XXX

    # paragraph text
    
    # character text
    

    # assemble the grammar
    rtfDoc = (leftBracket + rtfVersion + charSet + codePage +
        OneOrMore(rtfControl) +
        fontTable +
        #OneOrMore(rtfGroup) +
        rightBracket
        )

    def getGrammar(self):
        return self.rtfDoc

class RTFParser(object):

    grammar = RTFGrammar().rtfDoc

    def __init__(self, rtfData=None):
        if rtfData:
            self.parse(rtfData)

    def parse(self, rtfData):
        """
        # setup the tests to read the test RTF files
        >>> import os.path
        >>> package, module = os.path.split(__file__)
        >>> trunk, package = os.path.split(package)
        >>> basedir = os.path.join(trunk, 'test', 'sources', 'macrtf')
        >>> def getFileData(filename):
        ...   fh = open(os.path.join(basedir, filename))
        ...   data = fh.read()
        ...   fh.close()
        ...   return data

        # simple, single-word content
        #>>> data = getFileData('simpleContent.rtf')
        #>>> try:
        #...   rp = RTFParser(data)
        #...   import pdb;pdb.set_trace()
        #... except Exception, e:
        #...   print e
        #...   print data.splitlines()
        #>>> rp.tokens
        #>>> dir(rp.tokens)
        #>>> rp.tokens.asDict()
        #>>> rp.tokens.items()
        """
        self.tokens = self.grammar.parseString(rtfData)

class RTFFile(object):
    """

    """
    def __init__(self, filename):
        self.filename = filename
        self._fonts = {}
        self.parsed = None
        self.parse()
        self.buildFontTable()

    def parse(self):
        if hasattr(self.filename, 'read'):
            fh = self.filename
        else:
            fh = open(self.filename)
        if hasattr(self.filename, 'getvalue'):
            data = fh.getvalue()
        else:
            data = fh.read()
        fh.close()
        # pass the string data into the parser
        try:
            parsed = RFTParser.parse(data)
        except ParseException, e:
            msg = "could not parse '%s'[...] : %s"
            raise RTFParseError(msg % (rtfstring[:30], e))
        self.parsed = protocol.validate(parsed)

    def setFonts(self, fontData):
        self._fonts = fontData

    def getFonts(self):
        return self._fonts

    fonts = property(getFonts, setFonts)

    def buildFontTable(self):
        """

        """

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()

