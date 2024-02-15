#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Docs: https://docs.easydb.de/en/technical/api/tutorial/python_tutorial/python_tutorial.html

import requests
import json
import logging
from configparser import ConfigParser

from .ParamsReader import ParamsReader
from criteria_template import json_template

log = logging.getLogger('easydb_urls')
config = ConfigParser()
config.read('./easydb_urls/config.ini')


class Getter:
	"""Run all steps needed for a search
	parent class, with child methods in ListGetter and ObjectGetter
	"""
	def __init__(self, sessionobj, request, paramsdict = None, checkaccepted = True):
		self.baseurl = config.get('easydb_api', 'baseurl')
		self.sessionobj = sessionobj
		self.request = request
		
		self.sslverify = config.getboolean('easydb_api', 'sslverify')
		self.token_payload = {"token": self.sessionobj.token, "pretty": "0"}

		# list for the resulting urls
		self.urls = []

		# get the request params filtered by accepted params as dict with param name as key and
		# a list as values
		self.paramsreader = ParamsReader(self.request, paramsdict = paramsdict, checkaccepted = checkaccepted)
		self.paramsreader.separateParams()
		self.queryparams = self.paramsreader.getParams()

	def runQuery(self, local=False):
		"""Search database using search url and search criteria from search.json
			Store response in session object and cache results for subsequent use
		"""

		self.sessionobj.setQueryParams(self.queryparams)

		self.sessionobj.criteria_template = json_template # loaded from criteria_template.py
		self.sessionobj.set_criteria(local=local)

		_search_data = json.dumps(self.sessionobj.criteria)
		log.info('%s.runQuery: Search criteria: %r' % (__name__, _search_data))
		r = requests.post(self.sessionobj.search, params=self.token_payload, data=_search_data, verify=self.sslverify)

		res = r.json()

		if 'code' in res and res['code'][:5]=='error':
			# some error occured, e.g:
			# {'realm': 'api', 'description': 'Value original_filename_basename is not valid for field', 'code': 'error.api.invalid_value', 'parameters': {}}
			raise NameError(res)

		self.sessionobj.searchresult = res

	def getSearchParams(self):
		return self.queryparams

	def getResultCount(self):
		return self.sessionobj.getResultCount()
	
	def getPageSize(self):
		return self.sessionobj.getResultLimit()
	
	def getMaxPage(self):
		return int(self.getResultCount() / self.getResultLimit() + 1)
	
	def getResultLimit(self):
		# same as pagesize
		return self.sessionobj.getResultLimit()
	
	def getResultOffset(self):
		return self.sessionobj.getResultOffset()
	
	def setPage(self, page):
		self.paramsreader.setPage(page)
		self.queryparams = self.paramsreader.getParams()
	
	def setPageSize(self, pagesize):
		self.paramsreader.setPageSize(pagesize)
		self.queryparams = self.paramsreader.getParams()
	
	def setLimit(self, limit):
		self.paramsreader.setLimit(limit)
		self.queryparams = self.paramsreader.getParams()
	
	def getCurrentPage(self):
		count = self.getResultCount()
		offset = self.getResultOffset()
		limit = self.getResultLimit()
		currentpage = 1
		if (count is not None) and (offset is not None) and limit != 0:
			if offset <= count:
				currentpage = int(offset / limit + 1)
		return currentpage

	# redirect to paramsreader
	def getRequestParamsString(self, params_to_skip = []):
		return self.paramsreader.getRequestParamsString(params_to_skip = params_to_skip)
