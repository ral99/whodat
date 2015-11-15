import unittest

from os.path import dirname, join, realpath
from whodat.extension import *
from whodat.handler import *
from whodat.http import *
from whodat.wsgi import *

### Extensions ###

class ExtensionA(Extension):
    def __call__(self, app):
        setattr(app, 'one', 1)

    def process_request(self, request):
        setattr(request, 'two', 2)

    def process_response(self, request, response):
        setattr(request, 'three', 3)

### Handlers ###

@url('/')
class RootHandler:
    def get(self, request):
        return HTTPResponse('get')

    def post(self, request):
        return HTTPResponse('post')

@url('/arg/_/')
class ArgHandler:
    def get(self, request, arg):
        return HTTPResponse('get %s' % arg)

    def post(self, request, arg):
        return HTTPResponse('post %s' % arg)

@url('/error/')
class DivisionByZeroHandler:
    def get(self, request):
        return HTTPResponse('%s' % 1 / 0)

class FirePolice(ErrorHandler):
    def error404(self, http_error):
        return HTTPResponse('404', status=http_error.status)

    def error5xx(self, http_error):
        return HTTPResponse('5xx', status=http_error.status)

### Tests ###

class WSGIApplicationTest(unittest.TestCase):
    def setUp(self):
        self.debug_app = WSGIApplication(True, error_handler=FirePolice, extensions=[ExtensionA()],
                                         static_url='/static/',
                                         static_dir=join(dirname(realpath(__file__)), 'resources', 'static'))
        self.debug_app.add_handler(RootHandler)
        self.debug_app.add_handler(ArgHandler)
        self.debug_app.add_handler(DivisionByZeroHandler)

        self.app = WSGIApplication(False, error_handler=FirePolice, extensions=[ExtensionA()])
        self.app.add_handler(RootHandler)
        self.app.add_handler(ArgHandler)
        self.app.add_handler(DivisionByZeroHandler)

    def test_extension(self):
        self.assertEqual(self.app.one, 1)
        request = HTTPRequest.get(path_info='/')
        response = self.app.handle_request(request)
        self.assertEqual(request.two, 2)
        self.assertEqual(request.three, 3)

    def test_get(self):
        request = HTTPRequest.get(path_info='/')
        response = self.app.handle_request(request)
        self.assertEqual(response.text, 'get')

        request = HTTPRequest.get(path_info='/arg/gold/')
        response = self.app.handle_request(request)
        self.assertEqual(response.text, 'get gold')

    def test_post(self):
        request = HTTPRequest.post(path_info='/')
        response = self.app.handle_request(request)
        self.assertEqual(response.text, 'post')

        request = HTTPRequest.post(path_info='/arg/gold/')
        response = self.app.handle_request(request)
        self.assertEqual(response.text, 'post gold')

    def test_redirect(self):
        request = HTTPRequest.get(path_info='')
        response = self.app.handle_request(request)
        self.assertEqual(response.status, '302 Found')

        request = HTTPRequest.get(path_info='/arg/gold')
        response = self.app.handle_request(request)
        self.assertEqual(response.status, '302 Found')

    def test_not_found(self):
        request = HTTPRequest.get(path_info='/gold/')
        response = self.app.handle_request(request)
        self.assertEqual(response.text, '404')
        self.assertEqual(response.status, '404 Not Found')

    def test_internal_server_error(self):
        request = HTTPRequest.get(path_info='/error/')
        response = self.app.handle_request(request)
        self.assertEqual(response.text, '5xx')
        self.assertEqual(response.status, '500 Internal Server Error')

    def test_method_not_allowed(self):
        request = HTTPRequest.put(path_info='/')
        response = self.app.handle_request(request)
        self.assertEqual(response.text, 'Error 405')
        self.assertEqual(response.status, '405 Method Not Allowed')

    def test_static_file(self):
        with open(join(dirname(realpath(__file__)), 'resources', 'static', 'pixel.png'), 'rb') as static_file:
            request = HTTPRequest.get(path_info='/static/pixel.png')
            response = self.debug_app.handle_request(request)
            self.assertEqual(response.status, '200 OK')
            self.assertEqual(response.body, static_file.read())
            self.assertEqual(response.content_type, 'image/png')
            self.assertEqual(response.charset, None)

            request = HTTPRequest.get(path_info='/static/pixel.jpg')
            response = self.debug_app.handle_request(request)
            self.assertEqual(response.text, '404')
            self.assertEqual(response.status, '404 Not Found')

            request = HTTPRequest.get(path_info='/static/pixel.png')
            response = self.app.handle_request(request)
            self.assertEqual(response.text, '404')
            self.assertEqual(response.status, '404 Not Found')

if __name__ == '__main__':
    unittest.main()
