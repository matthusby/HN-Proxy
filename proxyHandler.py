from google.appengine.api import urlfetch
from google.appengine.ext import webapp

class AssestHandler(webapp.RequestHandler):
	def get(self):
		url = "http://news.ycombinator.com" + self.request.path
		if self.request.query_string is not None:
			url = url + '?' + self.request.query_string

		if 'user' in self.request.cookies:
			fetch_headers = {'Cookie':'user=' + self.request.cookies['user']}
			result = urlfetch.fetch(url, headers=fetch_headers, follow_redirects=False)
		else:
			result = urlfetch.fetch(url, follow_redirects=False)

		if 'set-cookie' in result.headers:
			self.response.headers.add_header('set-cookie', result.headers.get('set-cookie'))

		if 'location' in result.headers:
			self.redirect('/' + result.headers.get('location'))
		else:
			self.response.headers.add_header('content-type', result.headers['content-type'])
			self.response.out.write(result.content)

	def post(self):
		url = "http://news.ycombinator.com" + self.request.path
		post_data = ''
		for arg in self.request.arguments():
			post_data += arg + '=' + self.request.get(arg) + '&'
		post_data = post_data[:-1]
		if 'user' in self.request.cookies:
			fetch_headers = {'Cookie':'user=' + self.request.cookies['user']}
			result = urlfetch.fetch(url, method=urlfetch.POST, headers=fetch_headers, payload=post_data, follow_redirects=False)
		else:
			result = urlfetch.fetch(url, method=urlfetch.POST, payload=post_data, follow_redirects=False)

		if 'set-cookie' in result.headers:
			self.response.headers.add_header('set-cookie', result.headers.get('set-cookie'))

		if 'location' in result.headers:
			self.redirect('/' + result.headers.get('location'))
		else:
			self.response.out.write(result.content)