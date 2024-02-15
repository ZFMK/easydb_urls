import json
import logging
import re
from configparser import ConfigParser

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from .lib.SessionEAS import SessionEAS

log = logging.getLogger(__name__)
config = ConfigParser()
config.read('./easydb_urls/config.ini')

class LoginViews(object):
	"""View for managing user authentication
	"""

	def __init__(self, request):
		self.request = request
		self.baseurl = config.get('easydb_api', 'baseurl')

	@view_config(route_name='loginView', renderer="templates/login.pt")
	def loginView(self):
		"""Extra view for login, will always create a new session even if the user is logged in
		"""
		user = None
		return {'user': user}

	@view_config(route_name='sessionLogin')
	def sessionLogin(self):
		"""Try login, redirect to search form (=start page) on failure"""
		sessionobj = SessionEAS(self.request)
		referrer = self.request.referrer
		try:
			return HTTPFound(referrer)
		except ValueError:
			return HTTPFound(self.request.route_url('searchForm'))

	@view_config(route_name='sessionLogout')
	def sessionLogout(self):
		"""Do logout"""
		sessionobj = SessionEAS(self.request)
		if sessionobj.isAuthenticated() is not False:
			sessionobj.deauthenticate_session()

		referer = self.request.referer

		# delete credentials if given in referer string
		if isinstance(referer, str):
			referer = re.sub(r'\&user\=[^&]*(\&)?', r'\1', referer)
			referer = re.sub(r'\&password\=[^&]*(\&)?', r'\1', referer)

		try:
			return HTTPFound(referer)
		except ValueError:
			return HTTPFound(self.request.route_url('searchForm'))
