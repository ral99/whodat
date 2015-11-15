import re

from whodat.http import *

class Handler:
    """Handle requests."""

    def __init__(self, url_pattern):
        """Set the regular expression for the URL pattern."""
        self._url_regex = re.compile(r'^%s$' % re.escape(url_pattern).replace('_', '([^/]+)'))

    def __call__(self, request, *args):
        """Call the appropriate method and return an HTTPResponse, or raise an HTTPMethodNotAllowed exception."""
        http_method = request.method.lower()
        if http_method == 'head':
            http_method = 'get'
        try:
            handler_method = getattr(self, http_method)
        except:
            raise HTTPMethodNotAllowed()
        response = handler_method(request, *args)
        if isinstance(response, str):
            response = HTTPResponse(response)
        if request.method.lower() == 'head':
            response = HTTPResponse('', response.status, response.content_type, response.charset, response.headerlist)
        return response

class url:
    """Decorator to transform a class into a Handler instance."""

    def __init__(self, url_pattern):
        """Set the URL pattern."""
        self._url_pattern = url_pattern

    def __call__(self, cls):
        """Return an instance of a new type inherited from Handler."""
        handler = type('handler', (Handler,), dict(cls.__dict__))
        return handler(self._url_pattern)

class ErrorHandler:
    """Handle HTTPErrors."""

    def error(self, http_error):
        """Return a general-purpose HTTPResponse."""
        return HTTPResponse(str(http_error), status=http_error.status)

    def __call__(self, http_error):
        """Handle an HTTPError with the appropriate method."""
        http_error_status = str(http_error.status)
        if hasattr(self, 'error%s' % http_error_status):
            handler_method = getattr(self, 'error%s' % http_error_status)
        elif hasattr(self, 'error%sxx' % http_error_status[0]):
            handler_method = getattr(self, 'error%sxx' % http_error_status[0])
        else:
            handler_method = self.error
        return handler_method(http_error)
