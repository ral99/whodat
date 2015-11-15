import cgi
import unittest

from whodat.http import *

class HTTPRequestTest(unittest.TestCase):
    def test_method(self):
        request = HTTPRequest.get()
        self.assertEqual(request.method, 'GET')

        request = HTTPRequest.head()
        self.assertEqual(request.method, 'HEAD')

        request = HTTPRequest.post()
        self.assertEqual(request.method, 'POST')

        request = HTTPRequest.put()
        self.assertEqual(request.method, 'PUT')

        request = HTTPRequest.delete()
        self.assertEqual(request.method, 'DELETE')

    def test_http_version(self):
        request = HTTPRequest.get()
        self.assertEqual(request.http_version, 'HTTP/1.1')

        request = HTTPRequest.get(http_version='HTTP/1.0')
        self.assertEqual(request.http_version, 'HTTP/1.0')

    def test_charset(self):
        request = HTTPRequest.get()
        self.assertEqual(request.charset, 'UTF-8')

    def test_host_name(self):
        request = HTTPRequest.get(server_name='localhost', server_port=8000)
        self.assertEqual(request.host_name, 'http://localhost:8000')

        request = HTTPRequest.get(server_name='google.com', server_port=80)
        self.assertEqual(request.host_name, 'http://google.com')

    def test_host_port(self):
        request = HTTPRequest.get(server_port=8000)
        self.assertEqual(request.host_port, 8000)

    def test_host(self):
        request = HTTPRequest.get(server_name='localhost', server_port=8000)
        self.assertEqual(request.host, 'localhost:8000')

        request = HTTPRequest.get(server_name='google.com', server_port=80)
        self.assertEqual(request.host, 'google.com:80')

    def test_path(self):
        request = HTTPRequest.get(script_name='', path_info='/post/delete')
        self.assertEqual(request.path, '/post/delete')

        request = HTTPRequest.get(script_name='/post/delete', path_info='')
        self.assertEqual(request.path, '/post/delete')

        request = HTTPRequest.get(script_name='/wiki', path_info='/post/delete')
        self.assertEqual(request.path, '/wiki/post/delete')

    def test_query_string(self):
        request = HTTPRequest.get(query_string='abc=def&123=456')
        self.assertEqual(request.query_string, 'abc=def&123=456')

    def test_url(self):
        request = HTTPRequest.get(server_name='google.com', server_port=80, script_name='/wiki',
                                  path_info='/post/delete', query_string='abc=def', url_scheme='https')
        self.assertEqual(request.url, 'https://google.com:80/wiki/post/delete?abc=def')

    def test_body(self):
        request = HTTPRequest.post()
        self.assertEqual(request.body, b'')

        request = HTTPRequest.post(params={'abc': 'def'})
        self.assertEqual(request.body, b'abc=def')

        request = HTTPRequest.post(params={'abc': 'def', '123': '456'})
        self.assertIn(b'123=456', request.body)
        self.assertIn(b'abc=def', request.body)

    def test_text(self):
        request = HTTPRequest.post()
        self.assertEqual(request.text, '')

        request = HTTPRequest.post(params={'abc': 'def'})
        self.assertEqual(request.text, 'abc=def')

        request = HTTPRequest.post(params={'abc': 'def', '123': '456'})
        self.assertIn('123=456', request.text)
        self.assertIn('abc=def', request.text)

    def test_GET(self):
        request = HTTPRequest.get(query_string='abc=def&123=456')
        self.assertEqual(request.GET['abc'], 'def')
        self.assertEqual(request.GET['123'], '456')

    def test_POST(self):
        request = HTTPRequest.post(params={'abc': 'def', '123': '456'})
        self.assertEqual(request.POST['abc'], 'def')
        self.assertEqual(request.POST['123'], '456')

        request = HTTPRequest.post(params={'file': ('filename', b'content')})
        self.assertTrue(isinstance(request.POST['file'], cgi.FieldStorage))

    def test_headers(self):
        request = HTTPRequest.get(headers={'HTTP_CONNECTION': 'keep-alive',
                                           'HTTP_USER_AGENT': 'Mozilla/5.0',
                                           'HTTP_ACCEPT': 'text/html,text/xhtml;q=0.9',
                                           'HTTP_ACCEPT_ENCODING': 'gzip,deflate,sdch',
                                           'HTTP_ACCEPT_LANGUAGE': 'en-US,en;q=0.8,de;q=0.6'})
        self.assertEqual(request.headers['Connection'], 'keep-alive')
        self.assertEqual(request.headers['User-Agent'], 'Mozilla/5.0')
        self.assertEqual(request.headers['Accept'], 'text/html,text/xhtml;q=0.9')
        self.assertEqual(request.headers['Accept-Encoding'], 'gzip,deflate,sdch')
        self.assertEqual(request.headers['Accept-Language'], 'en-US,en;q=0.8,de;q=0.6')

        request = HTTPRequest.post()
        self.assertEqual(request.headers['Content-Type'], 'application/x-www-form-urlencoded')

        request = HTTPRequest.post(params={'file': ('filename', b'content')})
        self.assertIn('multipart/form-data; boundary=', request.headers['Content-Type'])

    def test_cookies(self):
        request = HTTPRequest.get(headers={'HTTP_COOKIE': 'abc=def; 123=456'})
        self.assertEqual(request.cookies['abc'], 'def')
        self.assertEqual(request.cookies['123'], '456')

    def test_accept(self):
        request = HTTPRequest.get(headers={'HTTP_ACCEPT': 'text/html,text/xhtml;q=0.9'})
        self.assertEqual(request.accept, ['text/html', 'text/xhtml'])

    def test_accept_charset(self):
        request = HTTPRequest.get(headers={'HTTP_ACCEPT_CHARSET': 'iso-8859-5,unicode-1-1;q=0.8'})
        self.assertEqual(request.accept_charset, ['iso-8859-5', 'iso-8859-1', 'unicode-1-1'])

    def test_accept_encoding(self):
        request = HTTPRequest.get(headers={'HTTP_ACCEPT_ENCODING': 'gzip,deflate,sdch'})
        self.assertEqual(request.accept_encoding, ['gzip', 'deflate', 'sdch'])

    def test_accept_language(self):
        request = HTTPRequest.get(headers={'HTTP_ACCEPT_LANGUAGE': 'en-US,en;q=0.8,de;q=0.6'})
        self.assertEqual(request.accept_language, ['en-US', 'en', 'de'])

class HTTPResponseTest(unittest.TestCase):
    def test_body(self):
        response = HTTPResponse(body='abc123')
        self.assertEqual(response.body, b'abc123')

        response = HTTPResponse(body=b'abc123')
        self.assertEqual(response.body, b'abc123')

    def test_text(self):
        response = HTTPResponse(body='abc123')
        self.assertEqual(response.text, 'abc123')

        response = HTTPResponse(body=b'abc123')
        self.assertEqual(response.text, 'abc123')

    def test_content_type(self):
        response = HTTPResponse(content_type='text/plain')
        self.assertEqual(response.content_type, 'text/plain')

        response = HTTPResponse(content_type='image/jpeg')
        self.assertEqual(response.content_type, 'image/jpeg')

    def test_status(self):
        response = HTTPResponse(status=200)
        self.assertEqual(response.status, '200 OK')

        response = HTTPResponse(status=404)
        self.assertEqual(response.status, '404 Not Found')

    def test_charset(self):
        response = HTTPResponse(charset='utf-8')
        self.assertEqual(response.charset, 'utf-8')

        response = HTTPResponse(charset='latin-1')
        self.assertEqual(response.charset, 'latin-1')

    def test_headerlist(self):
        response = HTTPResponse(headerlist=[('Set-Cookie', 'abc=def'), ('Cache-Control', 'max-age=60')])
        self.assertEqual(response.headerlist, [('Set-Cookie', 'abc=def'), ('Cache-Control', 'max-age=60'),
                                               ('Content-Length', '0')])

    def test_cache_expires(self):
        response = HTTPResponse()
        response.cache_expires(5)
        self.assertIn(('Cache-Control', 'max-age=5'), response.headerlist)

    def test_set_cookie(self):
        response = HTTPResponse()
        response.set_cookie('abc', 'def')
        self.assertIn(('Set-Cookie', 'abc=def; Path=/'), response.headerlist)

    def test_unset_cookie(self):
        response = HTTPResponse()
        response.set_cookie('abc', 'def')
        response.set_cookie('123', '456')
        response.unset_cookie('abc')
        self.assertIn(('Set-Cookie', '123=456; Path=/'), response.headerlist)
        self.assertNotIn(('Set-Cookie', 'abc=def; Path=/'), response.headerlist)

    def test_delete_cookie(self):
        response = HTTPResponse()
        response.delete_cookie('a')
        self.assertTrue(dict(response.headerlist)['Set-Cookie'].startswith('a=; Max-Age=0; Path=/'))

class HTTPRedirectTest(unittest.TestCase):
    def test(self):
        response = HTTPRedirect('http://www.google.com')
        self.assertEqual(response.status, '302 Found')
        self.assertIn(('Location', 'http://www.google.com'), response.headerlist)

        response = HTTPRedirect('http://www.google.com', True)
        self.assertEqual(response.status, '301 Moved Permanently')
        self.assertIn(('Location', 'http://www.google.com'), response.headerlist)

class HTTPErrorTest(unittest.TestCase):
    def test(self):
        error = HTTPError(404)
        self.assertEqual(error.status, 404)
        self.assertEqual(str(error), 'Error 404')

class HTTPNotFoundTest(unittest.TestCase):
    def test(self):
        error = HTTPNotFound()
        self.assertEqual(error.status, 404)
        self.assertEqual(str(error), 'Error 404')

class HTTPMethodNotAllowedTest(unittest.TestCase):
    def test(self):
        error = HTTPMethodNotAllowed()
        self.assertEqual(error.status, 405)
        self.assertEqual(str(error), 'Error 405')

class HTTPInternalServerErrorTest(unittest.TestCase):
    def test(self):
        error = HTTPInternalServerError()
        self.assertEqual(error.status, 500)
        self.assertEqual(str(error), 'Error 500')

if __name__ == '__main__':
    unittest.main()
