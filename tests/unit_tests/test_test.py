import unittest

from whodat.handler import *
from whodat.http import *
from whodat.test import *
from whodat.wsgi import *

### Handlers ###

@url('/')
class RootHandler:
    def get(self, request):
        response = HTTPResponse('get, %s' % request.cookies.get('method', ''))
        response.set_cookie('method', 'get')
        return response

    def post(self, request):
        response = HTTPResponse('post, %s' % request.cookies.get('method', ''))
        response.set_cookie('method', 'post')
        return response

    def put(self, request):
        response = HTTPResponse('put, %s' % request.cookies.get('method', ''))
        response.set_cookie('method', 'put')
        return response

    def delete(self, request):
        response = HTTPResponse('delete, %s' % request.cookies.get('method', ''))
        response.set_cookie('method', 'delete')
        return response

### Tests ###

class ClientTest(unittest.TestCase):
    def setUp(self):
        app = WSGIApplication(True)
        app.add_handler(RootHandler)
        self.client = Client(app)

    def test_get(self):
        response = self.client.get('/')
        self.assertEqual(response.text, 'get, ')
        response = self.client.get('/')
        self.assertEqual(response.text, 'get, get')

    def test_post(self):
        response = self.client.post('/')
        self.assertEqual(response.text, 'post, ')
        response = self.client.get('/')
        self.assertEqual(response.text, 'get, post')

    def test_put(self):
        response = self.client.put('/')
        self.assertEqual(response.text, 'put, ')
        response = self.client.get('/')
        self.assertEqual(response.text, 'get, put')

    def test_delete(self):
        response = self.client.delete('/')
        self.assertEqual(response.text, 'delete, ')
        response = self.client.get('/')
        self.assertEqual(response.text, 'get, delete')

    def test_head(self):
        response = self.client.head('/')
        self.assertEqual(response.text, '')
        response = self.client.get('/')
        self.assertEqual(response.text, 'get, get')

if __name__ == '__main__':
    unittest.main()
