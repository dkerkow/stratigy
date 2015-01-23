# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

from app import app, db
from app.forms import NewSiteForm
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
    try:
        site = Site.query.get_or_404(site_id)
    except:
        return render_template('404.html'), 404
    else:
        return render_template('edit_site.html', site=site)
