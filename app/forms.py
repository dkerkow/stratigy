# Import Form module
from flask.ext.wtf import Form

# Import Form elements 
from wtforms import TextField, DecimalField

# Import Form validators
from wtforms.validators import Required

# Define the geodata input form (WTForms)

class GeodataForm(Form):
    site_name   = TextField('Site Name', [
                Required(message='Forgot your email address?')])
    geom_x      = DecimalField('X Coordinate', [
                Required(message='You must provide coordinates.')])
    geom_y      = DecimalField('Y Coordinate', [
                Required(message='You must provide coordinates.')])
    strat_json  = TextField('Stratigraphy in JSON format.')
