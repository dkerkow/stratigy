# -*- coding: utf-8 -*-

# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, Response

import simplejson as json

from app import app, db
from app.forms import NewSiteForm
from app.forms import NewRecordForm
from app.models import Site, Record

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

@app.route('/new_site/', methods=['GET', 'POST'])
def new_site():
    form = NewSiteForm()

    if form.validate_on_submit():

        site_name = request.form['site_name']
        geom_x, geom_y = (request.form['geom_x'], request.form['geom_y'])

        site = Site(site_name, geom_x, geom_y)
        db.session.add(site)
        db.session.commit()

        flash('Record successfully submitted: ')
        return redirect('/map')

    return render_template('new_site.html', form=form)

@app.route('/sites/', methods=['GET'])
def sites():
    sites = Site.query.all()
    return render_template('sites.html', sites=sites)

@app.route('/edit/<int:site_id>', methods=['GET', 'POST'])
def edit(site_id=None):

    # POST
    form = NewRecordForm()
    if form.validate_on_submit():

        depth           = request.form['depth']
        upper_boundary  = request.form['upper_boundary']
        lower_boundary  = request.form['lower_boundary']

        attribute       = request.form['attribute']
        value           = request.form['value']

        # try if value can be cast to integer or float:
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                value = value

        properties = { attribute : value }

        record = Record(
            site_id=site_id,
            depth=depth,
            upper_boundary=upper_boundary,
            lower_boundary=lower_boundary,
            properties=properties
        )

        db.session.add(record)
        db.session.commit()

        flash('Record saved! ')
        return redirect(url_for('edit', site_id=site_id))

    # GET
    try:
        site = Site.query.get_or_404(site_id)
    except:
        return render_template('404.html'), 404
    else:
        records = Record.query.filter_by(site_id=site_id)

        return render_template(
            'edit_site.html',
            site_id=site_id,
            form=form,
            site=site,
            records=records
        )


@app.route('/data/<int:site_id>', methods=['GET'])
def data(site_id=None):
    try:
        site = Site.query.get_or_404(site_id)

    except:
        resp = Response(status=404)
        return resp

    else:
        geom = db.session.scalar(site.geom.ST_AsGeoJSON())

        records = Record.query.filter_by(site_id=site_id)

        record_dict = {}

        for record in records:
            properties_dict = json.loads(record.properties)
            record_dict[record.id] = {
                'depth': record.depth,
                'upper_boundary': record.upper_boundary,
                'lower_boundary': record.lower_boundary,
                'properties': properties_dict
            }

        geojson_data = {
            u'type': u'Feature',
            u'geometry': json.loads(geom),
            u'properties': {
                u'title': u'Site Name',
                u'description': u'Description Placeholder',
                u'marker-size': u'large',
                u'strat_units': record_dict,
            }
        }

        geojson = json.dumps(geojson_data)
        resp = Response(geojson, status=200, mimetype='application/json')
        return resp
