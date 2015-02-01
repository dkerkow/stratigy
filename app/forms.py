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
    geom_x      = DecimalField('X Coordinate', [
                Required(message='You must provide coordinates.')])
    geom_y      = DecimalField('Y Coordinate', [
                Required(message='You must provide coordinates.')])

class NewRecordForm(Form):
    # 'site_id' is being injected in the controller
    depth           = DecimalField('depth of the record')
    upper_boundary  = DecimalField('upper bound of the record')
    lower_boundary  = DecimalField('lower bound of the record')
    attribute       = TextField('attribute name', [
                    Required(message='Please enter an attribute')])
    value           = TextField('value', [
                    Required(message='Please enter a value')])
