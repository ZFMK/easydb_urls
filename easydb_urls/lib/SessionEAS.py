#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Docs: https://docs.easydb.de/en/technical/api/tutorial/python_tutorial/python_tutorial.html

import requests
import json
import logging

from configparser import ConfigParser
from .PyramidSession import SessionAuthentication

log = logging.getLogger('easydb_urls')
config = ConfigParser()
config.read('./easydb_urls/config.ini')

class SessionError(Exception):
	def __init__(self, error_message:str=""):
		Exception.__init__(self, error_message)
		self.error_message = error_message

	def __str__(self):
		return "Session Error in {0}: {1}".format(__name__, self.error_message)

class SessionEAS:
	"""Class variables made private by setting and getting them with setters and getters and the property method?
	"""
	_session=""
	_token=""
	_header=""
	_content=""
	_plugins=""
	_password=""
	_login  = ""

	def __init__(self, request):
		self.request = request
		self.login = 'anonymous'
		self.password = None
		self.session = None
		self.token = None

		self.criteria = {}
		self.searchable = None
		self.searchtype = None
		self.queryparams = None
		self.criteria_template = {}
		self.searchresult = {}

		self.sslverify = config.getboolean('easydb_api', 'sslverify')
		self.setApiPaths()
		
		credentials = self.getCredentialsFromParams()
		
		self.sessionauth = SessionAuthentication(self.request)
		sessiontoken = self.sessionauth.getSessionToken()
		
		if credentials['user'] != 'anonymous' and credentials['password'] is not None:
			self.registerNewSession()
		
		elif 'token' in self.request.params:
			self.session = self.retrieve_session_by_token(self.request.params['token'])
		
		elif sessiontoken is not None:
			self.session = self.retrieve_session_by_token(sessiontoken)
		
		if self.session is None:
			self.registerNewSession()

	def setApiPaths(self):
		server = config.get('easydb_api', 'baseurl')
		self.new_session = server + "/api/v1/session"
		self.auth_session = server + "/api/v1/session/authenticate"
		self.deauth_session = server + "/api/v1/session/deauthenticate"
		self.search = server + "/api/v1/search"
		self.plugin = server + "/api/v1/plugin"
		self.server = server + "/api/v1/plugin/base/server/status"
		self.collectionlist = server + "/api/v1/collection/list"
		self.collection = server + "/api/v1/collection"
		self.objects = server + "/api/v1/objects"

	def getCredentialsFromParams(self):
		user = 'anonymous'
		password = None
		for requestparam in self.request.params:
		# fetch the user credentials if any
			if requestparam.lower() == 'user':
				user = self.request.params.getone(requestparam.lower())
			elif requestparam.lower() == 'password':
				password = self.request.params.getone(requestparam.lower())
		# use set credentials to set self.login and self.password only if both are in parameters
		return {'user': user, 'password': password}

	def setCredentialsFromParams(self):
		credentials = self.getCredentialsFromParams()
		self.setCredentials(credentials['user'], credentials['password'])

	def setCredentials(self, user, password):
		self.login = user
		self.password = password

	def getSessionAuthentication(self):
		return self.sessionauth

	def registerNewSession(self):
		# must it be called again, when registerNewSession is called after a change in credentials has happened?
		# is it possible?
		self.setCredentialsFromParams()
		self.start_session()

		try:
			self.authenticate_session()
		except ValueError:
			user = 'anonymous'
			password = None
			self.setCredentials(user, password)
			self.authenticate_session()
		self.sessionauth.setSessionToken(self.token)

	def start_session(self):
		"""Create new session using URL directed towards database
		"""
		sessionrequest = self.new_session
		r = None
		try:
			r = requests.get(sessionrequest, verify = self.sslverify)
		except requests.exceptions.ConnectionError as e:
			raise SessionError("A severe error occured during session start in SessionEAS: {}".format(e))
		if not r:
			log.error("A severe error occured during session start in SessionEAS")
			raise SessionError("A severe error occured during session start in SessionEAS")

		log.debug('%s.start_session for remote addr %s startet. Status code: %r' % (__name__, self.request.remote_addr, r.status_code))

		self.session = r
		self.header = r.headers
		self.token = self.getVal(r.json(), "token")
		self.content = r.json()


	def retrieve_session_by_token(self, token):
		"""Retrieve the same session using Token and plain url
			Compare instances to prove similarity
		"""
		payload = {"token": token}
		r = requests.get(self.new_session, params=payload, verify = self.sslverify)
		log.debug(r.status_code)
		
		if r.status_code == 200:
			if self.getVal(r.json(), "token") == token:
				self.session = r
				self.header = r.headers
				self.token = self.getVal(r.json(), "token")
				self.content = r.json()
				
				try:
					self.login = self.content['user']['user']['login']
				except KeyError:
					self.login = 'anonymous'
				
				self.sessionauth.setSessionToken(self.token)
				
				return self.session
		
		return None

	def getLogin(self):
		return self.login

	def authenticate_session(self):
		"""Authenticate Session using authenticate url
			login and password credentials required, or email instead of login
		"""
		log.debug('Authenticate %s' % self.login)
		if (self.login == 'anonymous') or (self.password is None):
			payload = {"token": self.token, "method": "anonymous"}
		else:
			payload = {"token": self.token, "login": self.login, "password": self.password, "method": ["easydb", "email"]}
		
		r = requests.post(self.auth_session, params=payload, verify = self.sslverify)
		
		log.debug('%s.authenticate_session status code: %r' % (__name__, r.status_code))
		if r.status_code==200:
			log.debug('Authentication successful')
			return self.login
		else:
			log.debug('Login failed!')
			raise ValueError

	def deauthenticate_session(self):
		"""Deauthenticate session using deauthenticate url
		"""
		payload = {"token": self.token}
		
		r = requests.post(self.deauth_session, params=payload, verify = self.sslverify)
		if r.status_code==200:
			log.debug('Logout successful')
			self.login = 'anonymous'
		else:
			log.debug('Logout failed!')
		
		self.sessionauth.setSessionToken(None)

	def isAuthenticated(self):
		if self.login is not None and self.login != 'anonymous':
			return True
		else:
			return False

	def setQueryParams(self, queryparams):
		#TODO: move query setting to Getter class
		self.searchable = queryparams['search']
		self.searchtype = queryparams['type'][0] # = 'search'
		# take all params
		self.queryparams = queryparams

	def set_criteria(self, local=False):
		"""Add the search strings from url parameters to the json that is used in request against easydb API
		"""
		self.criteria = {}
		search_type = self.searchtype
		self.criteria[self.searchtype] = []
		criteria_list = []

		for template in self.criteria_template[search_type]:
			# add the parameters set by request
			if len(self.searchable) > 0:
				for x in self.searchable:
					# add a complete search template for each string to search for
					tmp = dict(template)
					tmp['string'] = x
					criteria_list.append(tmp)
			else:
				tmp = dict(template)
				tmp['string'] = ''
				criteria_list.append(tmp)
			
		if self.login == 'anonymous':
			# anonymous login, respect inter/vs intranet access
			if local:
				pass  # -- nothing to do: the service is located in the intranet
			else:  # add search for tags "extern (Vorschau)" or "extern (Original) to query"
				tags = json.loads(config.get("DEFAULT", "tags_extern"))
				criteria_list.append({"type":"in","bool":"must","in":tags,"fields":["_tags._id"]})

		if "limit" in self.queryparams:
			self.criteria['limit'] = int(self.queryparams['limit'][0])
		if "offset" in self.queryparams:
			self.criteria['offset'] = int(self.queryparams['offset'][0])
		
		# add the object types to search for
		if self.searchtype !='filename':
			self.criteria['objecttypes'] = ["objekte"]
		
		# replace the searchtype (e.g. 'filename' or 'iiif') with 'search' as the others are not used in search
		# self.criteria[self.searchtype] = criteria_list
		if self.searchtype =='filename':
			del(self.criteria['filename'])
		self.criteria['search'] = criteria_list

	def getResult_JSON(self):
		if not 'objects' in self.searchresult:
			return {}
		else:
			return self.searchresult

	def getResultDict(self):
		"""Extra method if something changed in getResult_JSON()
		"""
		if not 'objects' in self.searchresult:
			return {}
		else:
			return self.searchresult

	def getResultCount(self):
		if 'count' in self.searchresult:
			return self.searchresult['count']
		else:
			return None

	def getResultLimit(self):
		if 'limit' in self.searchresult:
			return self.searchresult['limit']
		else:
			return None

	def getResultOffset(self):
		if 'offset' in self.searchresult:
			return self.searchresult['offset']
		else:
			return None

	def printRequest(self, req):
		command = "curl -X {method} -H {headers} -d '{data}' '{uri}'"
		method = req.method
		uri = req.url
		data = req.body
		headers = ['"{0}: {1}"'.format(k, v) for k, v in req.headers.items()]
		headers = " -H ".join(headers)
		return command.format(method=method, headers=headers, data=data, uri=uri)

	"""
		Helper Methods
	"""
	def getVal(self, data, lookupkey):
		if isinstance(data, dict):
			for key, value in data.items():
				if key == lookupkey:
					return value

	def write_json(self, data, name):
		with open(name, 'w') as outfile:
			json.dump(data, outfile, indent=2)

	def write_file(self, r, filename):
		with open(filename, 'wb') as fd:
			for chunk in r.iter_content(chunk_size=128):
				fd.write(chunk)

	def server_url_error_message(self, url, err):
		pass

	def _setSession(self, session=None):
		self._session = session

	def _getSession(self):
		return self._session

	def _setHeader(self, header):
		self._header = header

	def _getHeader(self):
		return self._header

	def _setToken(self, token):
		self._token = token

	def _getToken(self):
		return self._token

	def _setContent(self, content):
		self._content = content

	def _getContent(self):
		return self._content

	def _setPassword(self, password):
		self._password = password

	def _getPassword(self):
		return self._password

	def _setLogin(self, login):
		self._login = login

	def _getLogin(self):
		return self._login

	def _setPlugins(self, plugins):
		self._plugins = plugins

	def _getPlugins(self):
		return self._plugins

	"""
	class variables made private by setting and getting them with setters and getters and the property method?
	"""
	token = property(_getToken, _setToken)
	header = property(_getHeader, _setHeader)
	session = property(_getSession, _setSession)
	content = property(_getContent, _setContent)
	password = property(_getPassword, _setPassword)
	login = property(_getLogin, _setLogin)
	plugins= property(_getPlugins, _setPlugins)
	
