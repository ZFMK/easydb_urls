import json
import logging

from pyramid.view import (view_config, view_defaults)
from configparser import ConfigParser

log = logging.getLogger(__name__)
config = ConfigParser()
config.read('./easydb_urls/config.ini')

from .lib.ListGetter import ListGetter
from .lib.ParamsReader import ParamsReader
from .lib.SessionEAS import SessionEAS

from .lib.dicts2csv import Dicts2CSV

# @view_defaults(route_name='specimens')
class Listview(object):
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
		r = remote_ip.split('.')[:3]
		for ip in config_ip_intern:
			l = ip.strip().split('.')[:3]
			if len(r)==3 and l[0]==r[0] and l[1]==r[1] and l[2]==r[2]:
				self.local = True
				break

	@view_config(route_name='listAssets', accept='text/html', renderer="templates/filelist.pt")
	def listAssetsHTML(self):
		"""Search for the file urls, i. e. easyDB url to a file
		"""
		pagetitle = 'Assets Result List'
		listgetter = ListGetter(self.sessionobj, self.request)
		listgetter.runQuery(self.local)
		resultdicts = listgetter.getResultList()
		resultcount = listgetter.getResultCount()
		currentpage = listgetter.getCurrentPage()
		pagesize = listgetter.getResultLimit()
		maxpage = listgetter.getMaxPage()
		requestparamsstring = listgetter.getRequestParamsString(params_to_skip = ['page', 'limit', 'offset'])
		
		# get the used search terms and prepare them for display in page
		searchterms = listgetter.getSearchParams()
		for searchkey in searchterms:
			if searchkey in ['search', 'filename']:
				searchterms[searchkey] = '; '.join(searchterms[searchkey])

		user = self.sessionobj.getLogin()
		authenticated = self.sessionobj.isAuthenticated()
		
		return {'pagetitle': pagetitle,
				'resultdicts': resultdicts,
				'resultcount': resultcount,
				'currentpage': currentpage,
				'pagesize': pagesize,
				'maxpage': maxpage,
				'request': self.request,
				'searchterms': searchterms,
				'requestparamsstring': requestparamsstring,
				'user': user,
				'baseurl': self.baseurl,
				'authenticated': authenticated}

	@view_config(route_name='listAssetsJSON', renderer="json")
	@view_config(route_name='listAssets', accept='application/json', renderer="json")
	def listAssetsJSON(self):
		"""Search for the file urls, i. e. easyDB url to a file
		"""
		paramsreader = ParamsReader(self.request)
		paramsreader.separateParams()
		paramsdict = paramsreader.getParams()
		
		if paramsreader.usePaging() is False:
			resultdicts = self.combineAssetPages(paramsdict)
		else:
			listgetter = ListGetter(self.sessionobj, self.request)
			listgetter.runQuery(self.local)
			resultdicts = listgetter.getResultList()
		
		resultlist = []
		for obj in resultdicts:
			newobject = {}
			newobject['Image links'] = []
			try:
				newobject['preview'] = obj['preview_url']
			except KeyError:
				pass
			try:
				images = obj['versions']
				for image in images:
					newobject['Image links'].append("{0}: {1}".format(image['size'], image['url']))
			except KeyError:
				pass
			try:
				newobject['EasyDB page'] = "https://media.zfmk.de/detail/{0}".format(obj['identifier'])
			except KeyError:
				pass
			try:
				newobject['CETAF Stable ID'] = "https://id.zfmk.de/collection_ZFMK/?AccessionNumber={0}".format(obj['accessionnumber'])
			except KeyError:
				pass
			try:
				newobject['Species'] = obj['speciesname'].replace("<em>", "").replace("</em>", "")
				newobject['Species html'] = obj['speciesname']
			except KeyError:
				pass
			try:
				newobject['Locality'] = obj['locality']
			except KeyError:
				pass
			resultlist.append(newobject)
		return resultlist

	@view_config(route_name='listAssetsCSV', renderer="string")
	@view_config(route_name='listAssets', accept='application/csv', renderer="string")
	def listAssetsCSV(self):
		"""Search for the file urls, i. e. easyDB url to a file
		"""
		paramsreader = ParamsReader(self.request)
		paramsreader.separateParams()
		paramsdict = paramsreader.getParams()
		
		response = self.request.response
		response.content_disposition = 'attachement; filename={0}'.format("assets.csv")
		
		if paramsreader.usePaging() is False:
			resultdicts = self.combineAssetPages(paramsdict)
		else:
			listgetter = ListGetter(self.sessionobj, self.request)
			listgetter.runQuery(self.local)
			resultdicts = listgetter.getResultList()
		
		dicts2csv = Dicts2CSV()
		dicts2csv.addDataRows(resultdicts)
		
		dicts2csv.addHeaderRow()
		csvstring = dicts2csv.getCSVString()
		
		return csvstring

	def combineAssetPages(self, paramsdict):
		"""This method collects all pages from a search result and puts them together
		used with url parameter usepaging=false
		"""
		querystring = ""
		querystrings = []
		for paramkey in paramsdict:
			if paramkey.lower() in ['page', 'pagesize', 'limit', 'offset']:
				continue
			for paramstring in paramsdict[paramkey]:
				querystrings.append("{0}={1}".format(paramkey, paramstring))
		querystring += '&'.join(querystrings)
		if querystring != "":
			querystring = "?" + querystring

		listgetter = ListGetter(self.sessionobj, self.request)
		
		resultdicts = []
		
		limit = 5000
		listgetter.setLimit(limit)
		listgetter.runQuery(self.local)
		resultdicts.extend(listgetter.getResultList())
		
		maxpage = listgetter.getMaxPage()
		if maxpage > 1:
			for page in range(2, maxpage + 1, 1):
				listgetter.setPage(page)
				listgetter.runQuery(self.local)
				resultdicts.extend(listgetter.getResultList())

		return resultdicts
