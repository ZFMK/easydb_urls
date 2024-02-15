import os
import json
import logging
from configparser import ConfigParser
from ipaddress import IPv4Address, IPv4Network

from pyramid.response import FileResponse
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from .lib.ListGetter import ListGetter
from .lib.ObjectGetter import ObjectGetter
from .lib.FileGetter import FileGetter
from .lib.ParamsReader import ParamsReader
from .lib.SessionEAS import SessionEAS

log = logging.getLogger(__name__)
config = ConfigParser()
config.read('./easydb_urls/config.ini')


@view_config(route_name='favicon')
def favicon_view(request):
	here = os.path.dirname(__file__)
	icon = os.path.join(here, 'static', 'favicon.ico')
	return FileResponse(icon, request=request)

# @view_defaults(route_name='specimens')
class eaurlsViews(object):
	"""Routes for a webservice that queries easyDB
	The decorator decides wich method is used, depending on which HTTP-method is called and if the parameter id is given or not
	The decorator also does content negotiation by checking the Accept header of the http request
	Request parameters are handled within the views
	"""

	def __init__(self, request):
		self.request = request
		self.baseurl = config.get('easydb_api', 'baseurl')
		# get the session here and give it as parameter to the getter methods
		self.sessionobj = SessionEAS(self.request)
		self.local = False

		# distinguish between access from intranet (=local) and internet (extern).
		# this takes affect an anonymous session is requested
		if "X-Forwarded-For" not in self.request.headers:
			remote_ip = self.request.remote_addr
		else:
			remote_ip = self.request.headers["X-Forwarded-For"]
		log.debug('%s IP address/User Agent: %s/%s'%(__name__, remote_ip, self.request.user_agent))
		config_ip_intern = json.loads(config.get("DEFAULT", "ip_intern"))
		for ip in config_ip_intern:
			if IPv4Address(remote_ip) in IPv4Network(ip):
				self.local = True
				break

	@view_config(route_name='help', accept='text/html', renderer="templates/help.pt")
	def helpPage(self):
		pagecontent = {
			'pagetitle': 'Get easydb assets',
			'applicationurl': self.request.application_url
				
		}
		return pagecontent

	@view_config(route_name='searchPage', accept='text/html')
	def searchPageHTML(self):
		"""Search for the page urls, i. e. easyDB web page for an asset
		This redirects to the first search result. 
		It is not transparent to the user what happens here, but I have no idea how to implement a redirect to an easydb page that is transparent
		"""
		objectgetter = ObjectGetter(self.sessionobj, self.request)
		objectgetter.runQuery(self.local)
		resulturl = objectgetter.getFirstPageURL()
		if resulturl is None:
			return HTTPNotFound()
		else:
			# redirect
			return HTTPFound(location=resulturl)

	@view_config(route_name='searchPageJSON', renderer="json")
	@view_config(route_name='searchPage', accept='application/json', request_method='GET', renderer="json")
	def jsonPageJSON(self):
		"""The whole JSON object for the entry
		"""
		objectgetter = ObjectGetter(self.sessionobj, self.request)
		objectgetter.runQuery(self.local)
		result = objectgetter.getJSONPage()
		if result == {}:
			return HTTPNotFound()
		else:
			return result

	#####################################
	# this was used to test if subqueries can circumvent the server time out when the request takes more than 5 minutes.
	# Does not work because the parent request
	# is timed out
	@view_config(route_name='collectAssets', renderer="json")
	def collectAssets(self):
		listgetter = ListGetter(self.sessionobj, self.request)
		
		listgetter.runQuery(self.local)
		resultdicts = listgetter.getResultList()
		return {"resultdicts": resultdicts}
	####################################

	@view_config(route_name='searchForm', renderer="templates/searchform.pt")
	def searchForm(self):
		"""Display the search form
		"""
		user = self.sessionobj.getLogin()
		authenticated = self.sessionobj.isAuthenticated()

		pagetitle = 'Search EasyDB'
		return {'pagetitle': pagetitle, 'authenticated': authenticated, 'user': user}

	@view_config(route_name='getFile', accept='text/html')
	def getFile(self):
		"""Get a single object. Test: 841c7d2e-b317-41ad-83c0-bf8b17907dd3
		"""
		# ToDo: get file from cache

		filename = self.request.matchdict['filename']
		file_getter = FileGetter(self.sessionobj, self.request, paramsdict = {'search': filename, 'type': 'filename'})

		try:
			urldicts = file_getter.getFile(self.local)
		except NameError as e:
			log.error(e)
			return HTTPNotFound()

		log.debug("urldicts: %r" % urldicts)
		if len(urldicts)==0:
			return HTTPNotFound()

		return HTTPFound(location=urldicts[0]['download_url'])  # -- do a 302 redirect

	@view_config(route_name='searchDispatcher', accept='text/html')
	def searchDispatcher(self):
		"""Redirect search depending on parameter representation set in search form.
		"""
		paramsreader = ParamsReader(self.request, checkaccepted = False)
		paramsreader.separateParams()
		paramsdict = paramsreader.getParams()

		requestbody = ""
		requeststrings = []
		for paramkey in paramsdict:
			for paramstring in paramsdict[paramkey]:
				requeststrings.append("{0}={1}".format(paramkey, paramstring))
		requestbody += '&'.join(requeststrings)
		if requestbody != "":
			requestbody = "?" + requestbody

		if self.request.params.getone('representation') == "json":
			return HTTPFound(location='{0}/json/assets{1}'.format(self.request.application_url, requestbody))
		else:
			return HTTPFound(location='{0}/assets{1}'.format(self.request.application_url, requestbody))
