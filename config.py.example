# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database  (Then psycopg2 will connect using a Unix socket in the same manner as psql. When you specify a HOST, psycopg2 will connect with TCP/IP, which requires a password.)
SQLALCHEMY_DATABASE_URI = "postgresql://stratigy:secret@localhost/stratigy_development"
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "s3cr3t"

# Secret key for signing cookies
SECRET_KEY = "s3cr3t"