from wtforms.widgets import Input
from markupsafe import Markup


class LatLonWidget(Input):
    def __init__(self, *args, **kwargs):
        super(LatLonWidget, self).__init__(*args, **kwargs)

    def __call__(self, field, **kwargs):
        lat = Markup('<input type="text" %s>' %
                     self.html_params(name="%s_lat" % field.name, **kwargs))
        lon = Markup('<input type="text" %s>' %
                     self.html_params(name="%s_long" % field.name, **kwargs))
        return lat+lon
