# middleware.py
from django import shortcuts

class Redirect(Exception):
	def __init__(self, url):
		self.url = url
		# One-time configuration and initialization.

def redirect(url):
	raise Redirect(url)

class RedirectMiddleware(Exception):
	def __init__(self, url):
		self.url = url
		# One-time configuration and initialization.
	def __call__(self, request):
		# Code to be executed for each request before
		# the view (and later middleware) are called.

		response = self.url(request)

		# Code to be executed for each request/response after
		# the view is called.

		return response
	def process_exception(self, request, exception):
		if isinstance(exception, Redirect):
			return shortcuts.redirect(exception.url)