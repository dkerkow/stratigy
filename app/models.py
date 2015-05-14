from app import db
from geoalchemy2.types import Geometry
from geoalchemy2.elements import WKTElement
from sqlalchemy.dialects.postgresql import JSONB

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

class Site(Base):

    """represents location and metadata of a stratigraphic record"""

    __tablename__ = 'sites'
    __table_args__ = {"schema":"public"}

    # Name of the stratigraphic record:
    site_name       = db.Column(db.String(128), nullable=False)

    # Location of the stratigraphic record:
    geom            = db.Column(Geometry(geometry_type='POINT', srid=4326))

    records         = db.relationship(
                        'Record',
                        backref='site',
                        lazy='dynamic',
                        cascade="all, delete, delete-orphan"
                    )

    # New instance instantiation procedure:
    def __init__(self, site_name, geom_x, geom_y):

        geom = WKTElement('POINT({0} {1})'.format(geom_x, geom_y), srid=4326)

        self.site_name = site_name
        self.geom = geom

    def __repr__(self):
        return '<Site %r>' % self.site_name

class Record(Base):

    """represents single stratigraphic units"""

    __tablename__ = 'records'
    __table_args__ = {"schema":"public"}

    # ID of corresponding site:
    site_id         = db.Column(db.Integer, db.ForeignKey('public.sites.id'))

    # depth values:
    depth           = db.Column(db.Numeric, nullable=True)
    upper_boundary  = db.Column(db.Numeric, nullable=True)
    lower_boundary  = db.Column(db.Numeric, nullable=True)

    # stratigraphic properties, represented as key/value store
    properties      = db.Column(JSONB)

    def __init__(self, depth = None, upper_boundary = None,
            lower_boundary = None, site_id = None, properties = None):

        self.site_id = site_id
        self.depth = depth
        self.upper_boundary = upper_boundary
        self.lower_boundary = lower_boundary
        self.properties = properties
