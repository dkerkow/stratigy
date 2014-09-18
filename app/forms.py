# Import Form module
from flask.ext.wtf import Form

# Import Form elements 
from wtforms import TextField

# Import Form validators
from wtforms.validators import Required

# Define the geodata input form (WTForms)

class GeodataForm(Form):
    site_name   = TextField('Site Name', [
                Required(message='Forgot your email address?')])
    geom        = TextField('Coordinates', [
                Required(message='You must provide coordinates.')])