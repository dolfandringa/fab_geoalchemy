from flask_appbuilder.views import ModelView
from flask_appbuilder.forms import GeneralModelConverter, FieldConverter
from .widgets import LatLonWidget
from .fields import PointField
from wtforms import validators
from flask_appbuilder.validators import Unique


class GeoFieldConverter(FieldConverter):
    conversion_table = tuple(
        [('is_point', PointField, LatLonWidget)] +
        list(FieldConverter.conversion_table))


class GeoModelConverter(GeneralModelConverter):
    def _convert_simple(self, col_name, label, description, lst_validators,
                        form_props):
        # Add Validator size
        max = self.datamodel.get_max_length(col_name)
        min = self.datamodel.get_min_length(col_name)
        if max != -1 or min != -1:
            lst_validators.append(validators.Length(max=max, min=min))
        # Add Validator is null
        if not self.datamodel.is_nullable(col_name):
            lst_validators.append(validators.InputRequired())
        else:
            lst_validators.append(validators.Optional())
        # Add Validator is unique
        if self.datamodel.is_unique(col_name):
            lst_validators.append(Unique(self.datamodel, col_name))
        default_value = self.datamodel.get_col_default(col_name)
        fc = GeoFieldConverter(self.datamodel, col_name, label, description,
                               lst_validators, default=default_value)
        form_props[col_name] = fc.convert()
        return form_props


class GeoModelView(ModelView):

    def _init_forms(self):
        super(GeoModelView, self)._init_forms()
        conv = GeoModelConverter(self.datamodel)
        if not self.search_form:
            self.search_form = conv.create_form(
                self.label_columns,
                self.search_columns,
                extra_fields=self.search_form_extra_fields,
                filter_rel_fields=self.search_form_query_rel_fields)
        if not self.add_form:
            self.add_form = conv.create_form(
                self.label_columns,
                self.add_columns,
                self.description_columns,
                self.validators_columns,
                self.add_form_extra_fields,
                self.add_form_query_rel_fields)
        if not self.edit_form:
            self.edit_form = conv.create_form(self.label_columns,
                                              self.edit_columns,
                                              self.description_columns,
                                              self.validators_columns,
                                              self.edit_form_extra_fields,
                                              self.edit_form_query_rel_fields)
