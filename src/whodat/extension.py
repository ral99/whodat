class Extension:
    """Plugin system for WSGIApplication."""

    def __call__(self, app):
        """It is called before any request is accepted by the server."""
        pass

    def process_request(self, request):
        """It is called before each request is processed by a handler."""
        pass

    def process_response(self, request, response):
        """It is called after each request is processed by a handler."""
        pass
