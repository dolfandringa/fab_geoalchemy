from wtforms.fields import Field
from wtforms import widgets


class LocationField(Field):
    widget = widgets.TextInput()

    def __init__(self, *args, **kwargs):
        super(Field, self).__init__(*args, **kwargs)
