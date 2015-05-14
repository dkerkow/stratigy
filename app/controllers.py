# -*- coding: utf-8 -*-

# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, Response

import simplejson as json

from app import app, db
from app.forms import NewSiteForm, NewRecordForm, SearchSitesForm, \
                      AddRecordProperty

from app.models import Site, Record

### Controllers ###

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

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
            properties = json.loads(record.properties)
            record_dict[record.id] = properties
            record_dict[record.id].update(
                    depth=record.depth,
                    upper_boundary=record.upper_boundary,
                    lower_boundary=record.lower_boundary
            )

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


@app.route('/search/', methods=['GET', 'POST'])
def search():
    form = SearchSitesForm()
    sites = []
    if form.validate_on_submit():

        site_name = request.form['site_name']
        key_name = request.form['key_name']

        sites = Site.query.filter_by(site_name=site_name).all()

    return render_template(
        'search.html',
        form=form,
        sites=sites
    )


@app.route('/record/<int:record_id>', methods=['GET', 'POST'])
def edit_record(record_id=None):
    # POST
    form = AddRecordProperty()

    if form.validate_on_submit():
        attribute = request.form['attribute']
        value     = request.form['value']

        record = Record.query.filter_by(id=record_id).one()
        properties = json.loads(record.properties)

        # check if new attribute already exists:
        if attribute in properties:
            # gib Fehler aus
            flash('Error: Attribute {} already exists!'.format(attribute))
        else:
            # append new property
            properties[attribute] = value

            # write to DB
            record.properties = properties
            db.session.commit()
            flash('Successfully saved!')

        return redirect(url_for('edit_record', record_id=record_id))

    # GET
    try:
        record = Record.query.get_or_404(record_id)
    except:
        return render_template('404.html'), 404
    else:
        record = Record.query.filter_by(id=record_id).one()
        site = Site.query.filter_by(id=record.site_id).one()
        properties = json.loads(record.properties)

        return render_template(
            'edit_record.html',
            form=form,
            id=record.id,
            depth=record.depth,
            upper_boundary=record.upper_boundary,
            lower_boundary=record.lower_boundary,
            properties=properties,
            site_name=site.site_name
        )


@app.route('/record/delete/<int:record_id>', methods=['GET'])
def delete_record(record_id=None):
    try:
        record = Record.query.filter_by(id=record_id).one()
    except:
        return render_template('404.html'), 404
    else:
        site_id = record.site_id
        db.session.delete(record)
        db.session.commit()
        flash('Record successfully deleted!')
        return redirect(url_for('edit', site_id=site_id))

@app.route('/site/delete/<int:site_id>', methods=['GET'])
def delete_site(site_id=None):
    try:
        site = Site.query.filter_by(id=site_id).one()
    except:
        return render_template('404.html'), 404
    else:
        # delete the site, cascades to related records
        db.session.delete(site)
        db.session.commit()
        flash('Site and Records successfully deleted!')
        return redirect(url_for('sites'))
