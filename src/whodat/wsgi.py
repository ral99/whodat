import inspect
import mimetypes
import os
import traceback

from whodat.handler import *
from whodat.http import *

class WSGIApplication:
    """WSGI application interface."""

    def __init__(self, debug, controllers=None, error_handler=None, extensions=None, static_url=None, static_dir=None):
        """Set attributes, inspect controllers to find Handlers and initialize extensions."""
        self._debug = debug
        self._error_handler = error_handler() if error_handler else ErrorHandler()
        self._extensions = extensions or []
        self._static_url = static_url
        self._static_dir = static_dir
        self._routes = {}
        for controller in controllers or []:
            for name, obj in inspect.getmembers(controller):
                if isinstance(obj, Handler):
                    self.add_handler(obj)
        for extension in self._extensions:
            extension(self)

    def add_handler(self, handler):
        """Add a Handler to this application."""
        self._routes[handler._url_regex] = handler

    def handle_request(self, request):
        """Return an HTTPResponse or redirect the request by appending a slash to its path."""
        try:
            for (url_regex, handler) in self._routes.items():
                match = url_regex.match(request.path)
                if match is not None:
                    for extension in self._extensions:
                        extension.process_request(request)
                    response = handler(request, *match.groups())
                    for extension in self._extensions:
                        extension.process_response(request, response)
                    return response
            for (url_regex, handler) in self._routes.items():
                match = url_regex.match(request.path + '/')
                if match is not None:
                    return HTTPRedirect(request.path + '/')
            if self._debug and self._static_url and self._static_dir and request.path.startswith(self._static_url):
                static_filename = os.path.join(self._static_dir, request.path[len(self._static_url):])
                try:
                    with open(static_filename, 'rb') as static_file:
                        content_type, charset = mimetypes.guess_type(static_filename)
                        return HTTPResponse(static_file.read(), content_type=content_type, charset=charset)
                except:
                    pass
            raise HTTPNotFound()
        except Exception as error:
            if not isinstance(error, HTTPError):
                if self._debug:
                    traceback.print_exc()
                error = HTTPInternalServerError()
            return self._error_handler(error)

    def __call__(self, environ, start_response):
        """WSGI interface."""
        return self.handle_request(HTTPRequest(environ))(environ, start_response)
