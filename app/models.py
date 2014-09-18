from app import db
from geoalchemy2.types import Geometry
from sqlalchemy.dialects.postgresql import JSON

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())


# Database model that holds the basic element of stratigraphic records, inherited from model 'Base':
class Site(Base):

    """represents an x/y coordinate location."""

    __tablename__ = 'geodata_sites'
    __table_args__ = {"schema":"public"}
    
    # Name of the stratigraphic record:
    site_name       = db.Column(db.String(128), nullable=False)

    # Location of the stratigraphic record:
    geom            = db.Column(Geometry(geometry_type='POINT', srid=4326))
    
    # JSON field containing stratigraphic record
    stratigraphy    = db.Column(JSON)

    # New instance instantiation procedure:
    def __init__(self, site_name, geom):
    
        self.site_name = site_name
        self.geom = geom
        self.stratigraphy = stratigraphy

    def __repr__(self):
        return '<Site %r>' % self.site_name
