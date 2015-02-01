# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

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

        record = Record(
            site_id=site_id,
            depth=depth,
            upper_boundary=upper_boundary,
            lower_boundary=lower_boundary
        )

        db.session.add(record)
        db.session.commit()

        flash('Record saved! ')
        return redirect(url_for('edit', form=form, site_id=site_id))

    # GET
    try:
        site = Site.query.get_or_404(site_id)
    except:
        return render_template('404.html'), 404
    else:
        records = Record.query.filter_by(site_id=site_id)
        return render_template('edit_site.html', form=form, site=site, records=records)
