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


