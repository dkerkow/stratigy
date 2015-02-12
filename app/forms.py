# Import Form module
from flask.ext.wtf import Form

# Import Form elements
from wtforms import TextField, DecimalField

# Import Form validators
from wtforms.validators import Required

# Define the geodata input form (WTForms)

class NewSiteForm(Form):
    site_name   = TextField('Site Name', [
                Required(message='Forgot your email address?')])
    geom_x      = DecimalField('Longitude', [
                Required(message='You must provide coordinates.')])
    geom_y      = DecimalField('Latitude', [
                Required(message='You must provide coordinates.')])

class NewRecordForm(Form):
    # 'site_id' is being injected in the controller
    depth           = DecimalField('Depth of the record')
    upper_boundary  = DecimalField('Upper bound of the record')
    lower_boundary  = DecimalField('Lower bound of the record')
    attribute       = TextField('Attribute name', [
                    Required(message='Please enter an attribute')])
    value           = TextField('Value', [
                    Required(message='Please enter a value')])
