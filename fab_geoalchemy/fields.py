from wtforms.fields import Field
from .widgets import LatLonWidget


class PointField(Field):
    widget = LatLonWidget()

    def __init__(self, *args, **kwargs):
        super(PointField, self).__init__(*args, **kwargs)
