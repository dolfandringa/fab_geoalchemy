from wtforms.widgets import Input
from markupsafe import Markup
import logging
from copy import deepcopy
from wtforms.utils import unset_value

log = logging.getLogger(__name__)


class LatLonWidget(Input):

    def __call__(self, field, **kwargs):
        log.debug("Instantiating LatLonWidget")
        lonname = "{}_lon".format(field.name)
        latname = "{}_lat".format(field.name)
        kwargs.setdefault("id", field.id)
        lonkwargs = deepcopy(kwargs)
        latkwargs = deepcopy(kwargs)
        lonkwargs["id"] = lonname
        latkwargs["id"] = latname
        log.debug("Field.data: {}".format(field.data))
        log.debug("kwargs: {}".format(kwargs))
        if "value" not in kwargs and field.data is not None \
                and field.data != unset_value:
            lonkwargs["value"] = field.data[lonname]
            latkwargs["value"] = field.data[latname]
        if "required" not in kwargs and "required" in getattr(field,
                                                              "flags", []):
            kwargs["required"] = True
        log.debug("Widget kwargs: {}".format(kwargs))
        lat = Markup('Latitude: <input type="text" %s>' %
                     self.html_params(name="%s_lat" % field.name, **latkwargs))
        lon = Markup(' Longitude: <input type="text" %s>' %
                     self.html_params(name="%s_lon" % field.name, **lonkwargs))
        return lat+lon
