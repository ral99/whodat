#!/usr/bin/env python

from settings import DEBUG, CONTROLLERS, ERROR_HANDLER, EXTENSIONS, STATIC_URL, STATIC_DIR
from whodat.wsgi import *

application = WSGIApplication(DEBUG, CONTROLLERS, ERROR_HANDLER, EXTENSIONS, STATIC_URL, STATIC_DIR)
