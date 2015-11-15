import unittest

from os.path import dirname, join, realpath
from urllib import request

class IntegrationTest(unittest.TestCase):
    def test_get(self):
        response = request.urlopen('http://localhost:8000/golden/corn/')
        text = response.read()
        self.assertEqual(text.decode('utf-8'), 'Lets get the golden corn!')

        response = request.urlopen('http://localhost:8000/metal/silver/food/apple/')
        text = response.read()
        self.assertEqual(text.decode('utf-8'), 'Lets get the silver apple!')

    def test_post(self):
        response = request.urlopen('http://localhost:8000/golden/corn/', data=b"")
        text = response.read()
        self.assertEqual(text.decode('utf-8'), 'Lets post the golden corn!')

        response = request.urlopen('http://localhost:8000/metal/silver/food/apple/', data=b"")
        text = response.read()
        self.assertEqual(text.decode('utf-8'), 'Lets post the silver apple!')

    def test_redirect(self):
        response = request.urlopen('http://localhost:8000/golden/corn')
        text = response.read()
        self.assertEqual(text.decode('utf-8'), 'Lets get the golden corn!')

        response = request.urlopen('http://localhost:8000/metal/silver/food/apple')
        text = response.read()
        self.assertEqual(text.decode('utf-8'), 'Lets get the silver apple!')

    def test_not_found(self):
        self.assertRaises(request.HTTPError, request.urlopen, 'http://localhost:8000/')

    def test_static_files(self):
        with open(join(dirname(realpath(__file__)), 'src', 'static', 'pixel.png'), 'rb') as static_file:
            response = request.urlopen('http://localhost:8000/static/pixel.png')
            self.assertEqual(response.read(), static_file.read())

if __name__ == '__main__':
    unittest.main()
