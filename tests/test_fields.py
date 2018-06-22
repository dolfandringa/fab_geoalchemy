import logging
from unittest import TestCase
from flask_appbuilder import SQLA, AppBuilder
from flask import Flask
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from geoalchemy2.elements import WKBElement
from werkzeug.datastructures import MultiDict

codelog = logging.getLogger('fab_geoalchemy')
codelog.setLevel(logging.DEBUG)

from fab_geoalchemy.views import GeoModelView
from fab_geoalchemy.interface import GeoSQLAInterface
from fab_geoalchemy import PointField, LatLonWidget

cfg = {'SQLALCHEMY_DATABASE_URI': 'postgresql:///test',
       'CSRF_ENABLED': False,
       'WTF_CSRF_ENABLED': False,
       'SECRET_KEY': 'bla'}

app = Flask('wtforms_jsonschema2_testing')
app.config.update(cfg)
db = SQLA(app)
appbuilder = AppBuilder(app, db.session)


class Observation(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(Geometry(geometry_type='POINT', srid=4326))
    location2 = Column(Geometry(geometry_type='POINT', srid=3857))

    def __repr__(self):
        if self.name:
            return self.name
        else:
            return 'Person Type %s' % self.id


class ObservationView(GeoModelView):
    datamodel = GeoSQLAInterface(Observation)
    add_columns = ['name', 'location', 'location2']


appbuilder.add_view(ObservationView, 'observations')
NL = 'SRID=4326;POLYGON((4.40108047690016 53.3586997019374,2.8607023099851' +\
     '51.4002188897169,6.9247420162497 50.6194989118665,7.67988543219077 ' +\
     '54.0188617734724,4.40108047690016 53.3586997019374))'


class TestFields(TestCase):
    def setUp(self):
        self.maxDiff = None
        app.testing = True
        self.app = app.test_client()
        ctx = app.app_context()
        ctx.push()
        db.create_all()
        db.session.add(Observation(name='something'))
        db.session.commit()
        db.session.flush()

    def testFieldConversion(self):
        form = ObservationView().add_form()
        self.assertTrue(hasattr(form, 'location'))
        self.assertIsInstance(form.location, PointField)
        self.assertIsInstance(form.location.widget, LatLonWidget)
        correct_html = 'Latitude: <input type="text" name="location_lat">' +\
            'Longitude: <input type="text" name="location_lon">'
        self.assertEqual(form.location(), correct_html)

    def testDataProcessing(self):
        form = ObservationView().add_form()
        data = MultiDict({'name': 'test',
                          'location_lat': '52.34812',
                          'location_lon': '5.98193',
                          'location2_lat': '52.34812',
                          'location2_lon': '5.98193'})
        form.process(formdata=data)
        self.assertEqual(form.location.data,
                         'SRID=4326;POINT(5.98193 52.34812)')
        self.assertEqual(form.location2.data,
                         'SRID=3857;POINT(5.98193 52.34812)')
        row = Observation()
        form.populate_obj(row)
        db.session.add(row)
        print(row.location)
        db.session.commit()
        db.session.flush()
        print("Location: {}".format(row.location))
        print("Checking intersection")
        print(db.session.scalar(row.location.ST_Intersects(NL)))
        self.assertTrue(db.session.scalar(row.location.ST_Intersects(NL)))
        print("Finished checking intersection")
        db.session.commit()

    def tearDown(self):
        db.drop_all()
