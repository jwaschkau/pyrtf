from rtfng.Styles import TextStyle
from rtfng.PropertySets import TextPropertySet, ShadingPropertySet

class Text(object):
    def __init__(self, *params):
        self.Data = None
        self.Style = None
        self.Properties = None
        self.Shading = None

        for param in params:
            if isinstance(param, TextStyle):
                self.Style = param
            elif isinstance(param, TextPropertySet):
                self.Properties = param
            elif isinstance(param, ShadingPropertySet):
                self.Shading = param
            else:
                # otherwise let the rendering custom handler sort it out itself
                self.SetData(param)

    def SetData(self, value):
        self.Data = value

class Inline(Text):

    def SetData(self, value):
        self.append(value)

    def append(self, *params):
        # filter out any that are explicitly None
        values = [x for x in params if x is not None]
        self.extend(values)



def TEXT(*params, **kwargs):
    text_props = TextPropertySet()
    text_props.SetFont(kwargs.get('font', None ))
    text_props.SetSize(kwargs.get('size', None ))
    text_props.SetBold(kwargs.get('bold', False))
    text_props.SetItalic(kwargs.get('italic', False))
    text_props.SetUnderline(kwargs.get('underline', False))
    text_props.SetColour(kwargs.get('colour', None ))

    if len(params) == 1:
        return Text(params[0], text_props)

    result = Inline(text_props)
    apply(result.append, params)
    return result

def B(*params):
    text_props = TextPropertySet(bold=True)

    if len(params) == 1:
        return Text(params[0], text_props)

    result = Inline(text_props)
    apply(result.append, params)
    return result

def I(*params):
    text_props = TextPropertySet(italic=True)

    if len(params) == 1:
        return Text(params[0], text_props)

    result = Inline(text_props)
    apply(result.append, params)
    return result

def U(*params):
    text_props = TextPropertySet(underline=True)

    if len(params) == 1:
        return Text(params[0], text_props)

    result = Inline(text_props)
    apply(result.append, params)
    return result
