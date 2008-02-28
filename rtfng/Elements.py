from types import IntType, FloatType, LongType, StringTypes
from copy import deepcopy
from binascii import hexlify

from Renderer import Renderer
from Constants import *
from Styles import *
from PropertySets import StandardColours, StandardFonts, StandardPaper

from rtfng.document.section import Section

class UnhandledParamError( Exception ) :
    def __init__( self, param ) :
        Exception.__init__( self, "Don't know what to do with param %s" % param )

#
#    Finally a StyleSheet in which all of this stuff is put together
#
class StyleSheet :
    def __init__( self, colours=None, fonts=None ) :

        self.Colours = colours or deepcopy( StandardColours )
        self.Fonts   = fonts   or deepcopy( StandardFonts   )

        self.TextStyles      = AttributedList()
        self.ParagraphStyles = AttributedList()

def MakeDefaultStyleSheet( ) :
    result = StyleSheet()

    NormalText = TextStyle( TextPropertySet( result.Fonts.Arial, 22 ) )

    ps = ParagraphStyle( 'Normal',
                         NormalText.Copy(),
                         ParagraphPropertySet( space_before = 60,
                                               space_after  = 60 ) )
    result.ParagraphStyles.append( ps )

    ps = ParagraphStyle( 'Normal Short',
                         NormalText.Copy() )
    result.ParagraphStyles.append( ps )

    NormalText.TextPropertySet.SetSize( 32 )
    ps = ParagraphStyle( 'Heading 1',
                         NormalText.Copy(),
                         ParagraphPropertySet( space_before = 240,
                                               space_after  = 60 ) )
    result.ParagraphStyles.append( ps )

    NormalText.TextPropertySet.SetSize( 24 ).SetBold( True )
    ps = ParagraphStyle( 'Heading 2',
                         NormalText.Copy(),
                         ParagraphPropertySet( space_before = 240,
                                               space_after  = 60 ) )
    result.ParagraphStyles.append( ps )

    #    Add some more in that are based on the normal template but that
    #    have some indenting set that makes them suitable for doing numbered
    normal_numbered = result.ParagraphStyles.Normal.Copy()
    normal_numbered.SetName( 'Normal Numbered' )
    normal_numbered.ParagraphPropertySet.SetFirstLineIndent( TabPropertySet.DEFAULT_WIDTH * -1 )
    normal_numbered.ParagraphPropertySet.SetLeftIndent     ( TabPropertySet.DEFAULT_WIDTH )

    result.ParagraphStyles.append( normal_numbered )

    normal_numbered2 = result.ParagraphStyles.Normal.Copy()
    normal_numbered2.SetName( 'Normal Numbered 2' )
    normal_numbered2.ParagraphPropertySet.SetFirstLineIndent( TabPropertySet.DEFAULT_WIDTH * -1 )
    normal_numbered2.ParagraphPropertySet.SetLeftIndent     ( TabPropertySet.DEFAULT_WIDTH *  2 )

    result.ParagraphStyles.append( normal_numbered2 )

    ## LIST STYLES
    for idx, indent in [ (1, TabPropertySet.DEFAULT_WIDTH    ),
                         (2, TabPropertySet.DEFAULT_WIDTH * 2),
                         (3, TabPropertySet.DEFAULT_WIDTH * 3) ] :
        indent = TabPropertySet.DEFAULT_WIDTH
        ps = ParagraphStyle( 'List %s' % idx,
                             TextStyle( TextPropertySet( result.Fonts.Arial, 22 ) ),
                             ParagraphPropertySet( space_before = 60,
                                                   space_after  = 60,
                                                   first_line_indent = -indent,
                                                   left_indent       = indent) )
        result.ParagraphStyles.append( ps )

    return result

class TAB  : pass
class LINE : pass

class RawCode :
    def __init__( self, data ) :
        self.Data = data

PAGE_NUMBER   = RawCode( r'{\field{\fldinst page}}'   )
TOTAL_PAGES   = RawCode( r'{\field{\fldinst numpages}}' )
SECTION_PAGES = RawCode( r'{\field{\fldinst sectionpages}}' )
ARIAL_BULLET  = RawCode( r'{\f2\'95}' )

def _get_jpg_dimensions( fin ):
    """
    converted from: http://dev.w3.org/cvsweb/Amaya/libjpeg/rdjpgcom.c?rev=1.2
    """

    M_SOF0   = chr( 0xC0 )    #    /* Start Of Frame N */
    M_SOF1   = chr( 0xC1 )    #    /* N indicates which compression process */
    M_SOF2   = chr( 0xC2 )    #    /* Only SOF0-SOF2 are now in common use */
    M_SOF3   = chr( 0xC3 )    #
    M_SOF5   = chr( 0xC5 )    #    /* NB: codes C4 and CC are NOT SOF markers */
    M_SOF6   = chr( 0xC6 )    #
    M_SOF7   = chr( 0xC7 )    #
    M_SOF9   = chr( 0xC9 )    #
    M_SOF10  = chr( 0xCA )    #
    M_SOF11  = chr( 0xCB )    #
    M_SOF13  = chr( 0xCD )    #
    M_SOF14  = chr( 0xCE )    #
    M_SOF15  = chr( 0xCF )    #
    M_SOI    = chr( 0xD8 )    #    /* Start Of Image (beginning of datastream) */
    M_EOI    = chr( 0xD9 )  #    /* End Of Image (end of datastream) */

    M_FF = chr( 0xFF )

    MARKERS = [ M_SOF0, M_SOF1,  M_SOF2,  M_SOF3,
                M_SOF5, M_SOF6,  M_SOF7,  M_SOF9,
                M_SOF10,M_SOF11, M_SOF13, M_SOF14,
                M_SOF15 ]

    def get_length() :
        b1 = fin.read( 1 )
        b2 = fin.read( 1 )
        return (ord(b1) << 8) + ord(b2)

    def next_marker() :
        #  markers come straight after an 0xFF so skip everything
        #  up to the first 0xFF that we find
        while fin.read(1) != M_FF :
            pass

        #  there can be more than one 0xFF as they can be used
        #  for padding so we are now looking for the first byte
        #  that isn't an 0xFF, this will be the marker
        while True :
            result = fin.read(1)
            if result != M_FF :
                return result

        raise Exception( 'Invalid JPEG' )

    #  BODY OF THE FUNCTION
    if not ((fin.read(1) == M_FF) and (fin.read(1) == M_SOI)) :
        raise Exception( 'Invalid Jpeg' )

    while True :
        marker = next_marker()

        #  the marker is always followed by two bytes representing the length of the data field
        length = get_length ()
        if length < 2 : raise Exception( "Erroneous JPEG marker length" )

        #  if it is a compression process marker then it will contain the dimension of the image
        if marker in MARKERS :
            #  the next byte is the data precision, just skip it
            fin.read(1)

            #  bingo
            image_height = get_length()
            image_width  = get_length()
            return image_width, image_height

        #  just skip whatever data it contains
        fin.read( length - 2 )

    raise Exception( 'Invalid JPEG, end of stream reached' )


_PNG_HEADER = '\x89\x50\x4e'
def _get_png_dimensions( data ) :
    if data[0:3] != _PNG_HEADER :
        raise Exception( 'Invalid PNG image' )

    width  = (ord(data[18]) * 256) + (ord(data[19]))
    height = (ord(data[22]) * 256) + (ord(data[23]))
    return width, height


class Image( RawCode ) :

    #  Need to add in the width and height in twips as it crashes
    #  word xp with these values.  Still working out the most
    #  efficient way of getting these values.
    # \picscalex100\picscaley100\piccropl0\piccropr0\piccropt0\piccropb0
    # picwgoal900\pichgoal281

    PNG_LIB = 'pngblip'
    JPG_LIB = 'jpegblip'
    PICT_TYPES = { 'png' : PNG_LIB,
                   'jpg' : JPG_LIB }

    def __init__( self, file_name, **kwargs ) :

        fin = file( file_name, 'rb' )

        pict_type = self.PICT_TYPES[ file_name[ -3 : ].lower() ]
        if pict_type == self.PNG_LIB :
            width, height = _get_png_dimensions( fin.read( 100 ) )
        else :
            width, height = _get_jpg_dimensions( fin )

        codes = [ pict_type,
                  'picwgoal%s' % (width  * 20),
                  'pichgoal%s' % (height * 20) ]
        for kwarg, code, default in [ ( 'scale_x',     'scalex', '100' ),
                                      ( 'scale_y',     'scaley', '100' ),
                                      ( 'crop_left',   'cropl',    '0' ),
                                      ( 'crop_right',  'cropr',    '0' ),
                                      ( 'crop_top',    'cropt',    '0' ),
                                      ( 'crop_bottom', 'cropb',    '0' ) ] :
            codes.append( 'pic%s%s' % ( code, kwargs.pop( kwarg, default ) ) )


        #  reset back to the start of the file to get all of it and now
        #  turn it into hex.
        fin.seek( 0, 0 )
        data = []
        image = hexlify( fin.read() )
        for i in range( 0, len( image ), 128 ) :
            data.append( image[ i : i + 128 ] )

        data = r'{\pict{\%s}%s}' % ( '\\'.join( codes ), '\n'.join( data ) )
        RawCode.__init__( self, data )

    def ToRawCode( self, var_name ) :
        return '%s = RawCode( """%s""" )' % ( var_name, self.Data )

class Text :
    def __init__( self, *params ) :
        self.Data       = None
        self.Style      = None
        self.Properties = None
        self.Shading    = None

        for param in params :
            if   isinstance( param, TextStyle  ) : self.Style      = param
            elif isinstance( param, TextPropertySet     ) : self.Properties = param
            elif isinstance( param, ShadingPropertySet  ) : self.Shading    = param
            else :
                #    otherwise let the rendering custom handler sort it out itself
                self.Data = param

    def SetData( self, value ) :
        self.Data = value

class Inline( list ) :
    def __init__( self, *params ) :
        super( Inline, self ).__init__()

        self.Style      = None
        self.Properties = None
        self.Shading    = None

        self._append = super( Inline, self ).append

        for param in params :
            if   isinstance( param, TextStyle  ) : self.Style      = param
            elif isinstance( param, TextPropertySet     ) : self.Properties = param
            elif isinstance( param, ShadingPropertySet  ) : self.Shading    = param
            else :
                #    otherwise we add to it to our list of elements and let
                #    the rendering custom handler sort it out itself.
                self.append( param )

    def append( self, *params ) :
        #    filter out any that are explicitly None
        [ self._append( param ) for param in params if param is not None ]

class Document :
    def __init__( self, style_sheet=None, default_language=None, view_kind=None, view_zoom_kind=None, view_scale=None ) :
        self.StyleSheet = style_sheet or MakeDefaultStyleSheet()
        self.Sections = AttributedList( Section )

        self.SetTitle( None )

        self.DefaultLanguage = default_language or Languages.DEFAULT
        self.ViewKind        = view_kind        or ViewKind.DEFAULT
        self.ViewZoomKind    = view_zoom_kind
        self.ViewScale       = view_scale

    def NewSection( self, *params, **kwargs ) :
        result = Section( *params, **kwargs )
        self.Sections.append( result )
        return result

    def SetTitle( self, value ) :
        self.Title = value
        return self

    def Copy( self ) :
        result = Document( style_sheet      = self.StyleSheet.Copy(),
                           default_language = self.DefaultLanguage,
                           view_kind        = self.ViewKind,
                           view_zoom_kind   = self.ViewZoomKind,
                           view_scale       = self.ViewScale )
        result.SetTitle( self.Title )
        result.Sections = self.Sections.Copy()

        return result

    # XXX this is a temporary fix until I figure out the best way to refactor
    # the renderer
    def write(self, fhOrFilename):
        if isinstance(fhOrFilename, str):
            fh = open(fhOrFilename, 'w+')
        else:
            fh = fhOrFilename
        r = Renderer()
        r.Write(self, fh)

def TEXT( *params, **kwargs ) :
    text_props = TextPropertySet()
    text_props.SetFont     ( kwargs.get( 'font',      None  ) )
    text_props.SetSize     ( kwargs.get( 'size',      None  ) )
    text_props.SetBold     ( kwargs.get( 'bold',      False ) )
    text_props.SetItalic   ( kwargs.get( 'italic',    False ) )
    text_props.SetUnderline( kwargs.get( 'underline', False ) )
    text_props.SetColour   ( kwargs.get( 'colour',    None  ) )

    if len( params ) == 1 :
        return Text( params[ 0 ], text_props )

    result = Inline( text_props )
    apply( result.append, params )
    return result

def B( *params ) :
    text_props = TextPropertySet( bold=True )

    if len( params ) == 1 :
        return Text( params[ 0 ], text_props )

    result = Inline( text_props )
    apply( result.append, params )
    return result

def I( *params ) :
    text_props = TextPropertySet( italic=True )

    if len( params ) == 1 :
        return Text( params[ 0 ], text_props )

    result = Inline( text_props )
    apply( result.append, params )
    return result

def U( *params ) :
    text_props = TextPropertySet( underline=True )

    if len( params ) == 1 :
        return Text( params[ 0 ], text_props )

    result = Inline( text_props )
    apply( result.append, params )
    return result
