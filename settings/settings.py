import os

DEBUG = False

APP_HOST = os.environ.get('APP_HOST', '')
APP_PORT = os.environ.get('APP_PORT', 80)

APP_SECRET = 'fhdfhaksjdf#sadfjklsdj@kjfdds'

INSTALLED_APPS = [
    'auth'
]

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASE_URL = os.environ.get('DATABASE_URL', '')


try:
    from .local_settings import *
except ImportError:
    pass