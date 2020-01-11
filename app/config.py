"""
config.py
- settings for the flask application object
"""
import os 
import logging 
from tempfile import gettempdir

class BaseConfig(object):
    DEBUG = True
    BASE_DIR = os.getcwd()
    logging.basicConfig(format='[%(name)s %(levelname)s %(asctime)s]  %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
    SQL_ALCH_DATABASE = None 
    
    SQL_ALCH_DATABASE = None 
    #
    #   ===================================
    #   DATABASE_DIALECT: postgresql+pg8000
    #   DATABASE_USER: username
    #   DATABASE_PASS: password
    #   DATABASE_IP: ip(:port)
    #   DATABASE_NAME: database
    #   ===================================
    #
    if os.environ.get('DATABASE_DIALECT') and os.environ.get('DATABASE_USER') and os.environ.get('DATABASE_PASS') and os.environ.get('DATABASE_IP') and os.environ.get('DATABASE_NAME'):
        SQL_ALCH_DATABASE = f"{os.environ.get('DATABASE_DIALECT')}://{os.environ.get('DATABASE_USER')}:{os.environ.get('DATABASE_PASS')}@{os.environ.get('DATABASE_IP')}/{os.environ.get('DATABASE_NAME')}"
        logging.debug(f"[DATABASE] Using external database with dialect {os.environ.get('DATABASE_DIALECT')}")
    else:
        logging.debug('[DATABASE] Either DATABASE_DIALECT, DATABASE_USER, DATABASE_PASS, DATABASE_URL or DATABASE_NAME is missing')
        logging.debug('[DATABASE] Using default sqlite database')
        pass
    SQLALCHEMY_DATABASE_URI = SQL_ALCH_DATABASE or 'sqlite:///' + os.path.join(BASE_DIR, 'zit.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # used for encryption and session management
    SECRET_KEY = 'SO_SECRET_KEY_MAYBE_RANDOM?123AWD$%!@awd'

    MAX_CONTENT_LENGTH = 6 * 1024 * 1024
    THREADS_PER_PAGE = 2
    CSRF_ENABLED = True
    TEMP_PATH = gettempdir()

