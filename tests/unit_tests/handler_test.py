import unittest

from whodat.handler import *
from whodat.http import *

### Handlers ###

@url('/')
class RootHandler:
    def get(self, request):
        return HTTPResponse('get')

    def post(self, request):
        return HTTPResponse('post')

@url('/one/_/')
class OneArgHandler:
    def get(self, request, one):
        return HTTPResponse('%s' % one)

@url('/two/_/_/')
class TwoArgsHandler:
    def get(self, request, one, two):
        return HTTPResponse('%s, %s' % (one, two))

@url('/str/')
class StrHandler:
    def get(self, request):
        return 'get'

    def post(self, request):
        return 'post'

class FirePolice(ErrorHandler):
    def error404(self, http_error):
        return HTTPResponse('404', status=http_error.status)

    def error5xx(self, http_error):
        return HTTPResponse('5xx', status=http_error.status)

### Tests ###

class HandlerTest(unittest.TestCase):
    def test_url_regex(self):
        self.assertEqual(RootHandler._url_regex.pattern, r'^\/$')
        self.assertEqual(OneArgHandler._url_regex.pattern, r'^\/one\/([^/]+)\/$')
        self.assertEqual(TwoArgsHandler._url_regex.pattern, r'^\/two\/([^/]+)\/([^/]+)\/$')

    def test_get(self):
        response = RootHandler(HTTPRequest.get())
        self.assertEqual(response.text, 'get')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'text/html')
        self.assertEqual(response.charset, 'UTF-8')

        response = OneArgHandler(HTTPRequest.get(), 'one')
        self.assertEqual(response.text, 'one')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'text/html')
        self.assertEqual(response.charset, 'UTF-8')

        response = TwoArgsHandler(HTTPRequest.get(), 'one', 'two')
        self.assertEqual(response.text, 'one, two')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'text/html')
        self.assertEqual(response.charset, 'UTF-8')

        response = StrHandler(HTTPRequest.get())
        self.assertEqual(response.text, 'get')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'text/html')
        self.assertEqual(response.charset, 'UTF-8')

    def test_post(self):
        response = RootHandler(HTTPRequest.post())
        self.assertEqual(response.text, 'post')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'text/html')
        self.assertEqual(response.charset, 'UTF-8')

        response = StrHandler(HTTPRequest.post())
        self.assertEqual(response.text, 'post')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'text/html')
        self.assertEqual(response.charset, 'UTF-8')

    def test_head(self):
        response = RootHandler(HTTPRequest.head())
        self.assertEqual(response.text, '')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'text/html')
        self.assertEqual(response.charset, 'UTF-8')

        response = OneArgHandler(HTTPRequest.head(), 'one')
        self.assertEqual(response.text, '')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'text/html')
        self.assertEqual(response.charset, 'UTF-8')

        response = TwoArgsHandler(HTTPRequest.head(), 'one', 'two')
        self.assertEqual(response.text, '')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'text/html')
        self.assertEqual(response.charset, 'UTF-8')

        response = StrHandler(HTTPRequest.head())
        self.assertEqual(response.text, '')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'text/html')
        self.assertEqual(response.charset, 'UTF-8')

    def test_method_not_allowed(self):
        self.assertRaises(HTTPMethodNotAllowed, RootHandler, HTTPRequest.put())
        self.assertRaises(HTTPMethodNotAllowed, RootHandler, HTTPRequest.delete())

class urlTest(unittest.TestCase):
    def test_decorator(self):
        self.assertTrue(isinstance(RootHandler, Handler))

class ErrorHandlerTest(unittest.TestCase):
    def test_specific_error_handler(self):
        response = FirePolice()(HTTPNotFound())
        self.assertEqual(response.text, '404')
        self.assertEqual(response.status, '404 Not Found')

    def test_class_error_handler(self):
        response = FirePolice()(HTTPInternalServerError())
        self.assertEqual(response.text, '5xx')
        self.assertEqual(response.status, '500 Internal Server Error')

    def test_general_error_handler(self):
        response = FirePolice()(HTTPMethodNotAllowed())
        self.assertEqual(response.text, 'Error 405')
        self.assertEqual(response.status, '405 Method Not Allowed')

if __name__ == '__main__':
    unittest.main()
