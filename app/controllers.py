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

@app.route('/submit_record/', methods=['GET', 'POST'])
def submit_record():
    form = GeodataForm()

    if form.validate_on_submit():

        site_name = request.form['site_name']
        geom_x, geom_y = (request.form['geom_x'], request.form['geom_y'])

        site = Site(site_name, geom_x, geom_y)
        db.session.add(site)
        db.session.commit()

        flash('Record successfully submitted: ')
        return redirect('/map')

    return render_template('submit_record.html', form=form)
