from unittest import TestCase
from flask_appbuilder import SQLA, AppBuilder
from flask import Flask
from flask_appbuilder import Model
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from fab_geoalchemy import LocationField


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
    location = Column(Geometry('POINT'))

    def __repr__(self):
        if self.name:
            return self.name
        else:
            return 'Person Type %s' % self.id


class ObservationView(ModelView):
    datamodel = SQLAInterface(Observation)
    add_columns = ['name', 'location']


appbuilder.add_view(ObservationView, 'observations')


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

    def testGeoalchemyField(self):
        form = ObservationView().add_form()
        self.assertTrue(hasattr(form, 'location'))
        self.assertIsInstance(form.location, LocationField)

    def tearDown(self):
        db.drop_all()
