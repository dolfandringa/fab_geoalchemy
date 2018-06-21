from flask_appbuilder.models.sqla.interface import SQLAInterface, _is_sqla_type
from geoalchemy2 import Geometry


class GeoSQLAInterface(SQLAInterface):
    def is_point(self, col_name):
        try:
            return _is_sqla_type(self.list_columns[col_name].type,
                                 Geometry('POINT'))
        except:
            return False
