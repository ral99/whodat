from whodat.http import *

class Client:
    """HTTP client for WSGIApplication."""

    def __init__(self, app):
        """Set the client for testing the specified app."""
        self._app = app
        self._cookies = {}

    def set_cookies(self, response):
        """Set the cookies from an HTTPResponse to the client."""
        cookie_header = dict(response.headerlist).get('Set-Cookie', '')
        for cookie in cookie_header.split(';'):
            if cookie:
                key, value = cookie.strip().split('=')
                self._cookies[key] = value

    def http_cookies(self):
        """Return an string representation of the client cookies using the HTTP header format."""
        return ';'.join(['%s=%s' % (key, value) for key, value in self._cookies.items()])

    def get(self, path):
        """Handle a GET request."""
        request = HTTPRequest.get(path_info=path, headers={'HTTP_COOKIE': self.http_cookies()})
        response = self._app.handle_request(request)
        self.set_cookies(response)
        return response

    def post(self, path, params=None):
        """Handle a POST request."""
        request = HTTPRequest.post(path_info=path, params=params, headers={'HTTP_COOKIE': self.http_cookies()})
        response = self._app.handle_request(request)
        self.set_cookies(response)
        return response

    def put(self, path, params=None):
        """Handle a PUT request."""
        request = HTTPRequest.put(path_info=path, params=params, headers={'HTTP_COOKIE': self.http_cookies()})
        response = self._app.handle_request(request)
        self.set_cookies(response)
        return response

    def delete(self, path):
        """Handle a DELETE request."""
        request = HTTPRequest.delete(path_info=path, headers={'HTTP_COOKIE': self.http_cookies()})
        response = self._app.handle_request(request)
        self.set_cookies(response)
        return response

    def head(self, path):
        """Handle a HEAD request."""
        request = HTTPRequest.head(path_info=path, headers={'HTTP_COOKIE': self.http_cookies()})
        response = self._app.handle_request(request)
        self.set_cookies(response)
        return response
