# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import the database object from the main app module
from app import db, app

# Import module forms
from app.mod_geodata.forms import GeodataForm

# Import module models (i.e. User)
from app.mod_geodata.models import Site

# Define the blueprint: 'geodata', set its url prefix: app.url/geodata
mod_geodata = Blueprint('geodata', __name__, url_prefix='/geodata')

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

# Return map
# (later this will be the place to search and place records)   
@app.route('/map/', methods=['GET', 'POST'])
def map():
    return render_template('geodata/map.html')