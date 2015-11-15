import controllers
import os

# bool that specifies wheter it is a development environment
DEBUG = True

# list of controller modules
CONTROLLERS = [controllers]

# error handler class
ERROR_HANDLER = None

# list of extensions
EXTENSIONS = []

# URL for static files in debug mode
STATIC_URL = '/static/'

# Directory for static files in debug mode
STATIC_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')
