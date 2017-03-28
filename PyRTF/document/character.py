from PyRTF.Styles import TextStyle
from PyRTF.PropertySets import TextPropertySet, ShadingPropertySet


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


class Inline(list):
    ''' A Text object but with a list of data. Perhaps unify Text and Inline classes? '''

    def __init__(self, *params):  # Method copied from above
        super(Inline, self).__init__()

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
                self.append(param)

    def append(self, *params):
        # filter out any that are explicitly None
        values = [x for x in params if x is not None]
        self.extend(values)


def TEXT(*params, **kwargs):
    textProps = TextPropertySet()
    textProps.font = kwargs.get('font', None)
    textProps.size = kwargs.get('size', None)
    textProps.bold = kwargs.get('bold', False)
    textProps.italic = kwargs.get('italic', False)
    textProps.underline = kwargs.get('underline', False)
    textProps.colour = kwargs.get('colour', None)

    if len(params) == 1:
        return Text(params[0], textProps)

    result = Inline(textProps)
    apply(result.append, params)
    return result


def B(*params):
    textProps = TextPropertySet(bold=True)

    if len(params) == 1:
        return Text(params[0], textProps)

    result = Inline(textProps)
    apply(result.append, params)
    return result


def I(*params):
    textProps = TextPropertySet(italic=True)

    if len(params) == 1:
        return Text(params[0], textProps)

    result = Inline(textProps)
    apply(result.append, params)
    return result


def U(*params):
    textProps = TextPropertySet(underline=True)

    if len(params) == 1:
        return Text(params[0], textProps)

    result = Inline(textProps)
    apply(result.append, params)
    return result
