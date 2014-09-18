# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

from app import app, db
from app.forms import GeodataForm
from app.models import Site

### Controllers ###

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map/', methods=['GET', 'POST'])
def map():
    return render_template('map.html')

