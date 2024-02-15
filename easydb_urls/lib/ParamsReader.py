#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Docs: https://docs.easydb.de/en/technical/api/tutorial/python_tutorial/python_tutorial.html
import logging
from configparser import ConfigParser

log = logging.getLogger('easydb_urls')
config = ConfigParser()
config.read('./easydb_urls/config.ini')

class ParamsReader():
	"""Get arguments from request params"""
	def __init__(self, request, paramsdict = None, checkaccepted = True):
		log.debug('%s: search request: %r' % (__name__, request.params))

		if paramsdict is not None:
			self.requestparams = paramsdict
		else:
			self.requestparams = request.params
		self.separator = ';'
		self.acceptedparams = ['search', 'type', 'filename', 'page', 'pagesize', 'limit', 'offset', 'usepaging', 'preferredsize']
		self.checkaccepted = checkaccepted
		
		self.paramsdict = {}
		self.usepaging = True
		self.readParams()

	def readParams(self):
		# create an empty list for all acceptedparams
		for acceptedparam in self.acceptedparams:
			self.paramsdict[acceptedparam.lower()] = []
		self.paramsdict['type'] = ['search']  # -- default search type

		# set the params that are in requestparams
		for requestparam in self.requestparams:
			try:
				pvalues = self.requestparams.getall(requestparam)
			except AttributeError:  # -- not a multidict
				pvalues = [self.requestparams[requestparam]]
			if self.checkaccepted is True and requestparam.lower() not in self.paramsdict.keys():
				# check if the parameter is in acceptedparams
				# if not pass because the key have not been added before
				pass
			else:
				# default setting in easydb code is empty string for un-set parameter
				# now set it with a list
				self.paramsdict[requestparam.lower()] = pvalues

		self.readUsePaging()
		self.readPageSize()
		self.readPage()
		self.readOffset()
		self.readLimit()

	def separateParams(self, separator=";", params2lookup = ["search",]):
		"""Separate strings in parameters into a list by the choosen separator.
		params2lookup defines the parameters where the separation should apply to
		by default the search params are used
		"""
		self.separator = separator
		
		if len(params2lookup) <= 0:
			params2lookup = list(self.paramsdict.keys())
		paramstrings = []
		for param in params2lookup:
			try:
				for paramstring in self.paramsdict[param]:
					paramstrings.extend([element.strip() for element in paramstring.split(self.separator)])
				self.paramsdict[param] = paramstrings
			except KeyError:
				pass

	def getRequestParamsList(self, params_to_skip=[]):
		paramslist = []
		params_to_skip = [param.lower() for param in params_to_skip]
		
		for paramkey in self.paramsdict:
			if paramkey.lower() not in params_to_skip:
				for paramvalue in self.paramsdict[paramkey]:
					paramslist.append('{0}={1}'.format(paramkey.lower(), paramvalue))
		return paramslist

	def getRequestParamsString(self, params_to_skip=[]):
		requestparamslist = self.getRequestParamsList(params_to_skip = params_to_skip)
		return '&'.join(requestparamslist)

	def getParams(self):
		return self.paramsdict

	def setPage(self, page):
		self.paramsdict['page'] = []
		self.paramsdict['page'].append(int(page))
		offset = (int(self.getPage()) - 1) * int(self.getPageSize())
		self.setOffset(offset)

	def readPage(self):
		if len(self.paramsdict['page']) <= 0:
			self.paramsdict['page'].append(1)

	def getPage(self):
		return self.paramsdict['page'][0]
	
	def readPageSize(self):
		if len(self.paramsdict['pagesize']) <= 0:
			self.paramsdict['pagesize'].append(1000)

	def getPageSize(self):
		return self.paramsdict['pagesize'][0]

	def setPageSize(self, pagesize):
		self.setLimit(pagesize)

	def setLimit(self, limit):
		self.paramsdict['limit'] = []
		self.paramsdict['limit'].append(int(limit))
		self.paramsdict['pagesize'] = []
		self.paramsdict['pagesize'].append(int(limit))

	def readLimit(self):
		if len(self.paramsdict['limit']) <= 0:
			self.paramsdict['limit'].append(self.getPageSize())
		else:
			self.paramsdict['pagesize'] = []
			self.paramsdict['pagesize'].append(self.paramsdict['limit'][0])

	def getLimit(self):
		return self.paramsdict['limit'][0]

	def setOffset(self, offset):
		self.paramsdict['offset'] = []
		self.paramsdict['offset'].append(offset)

	def readOffset(self):
		if len(self.paramsdict['offset']) <= 0:
			offset = (int(self.getPage()) - 1) * int(self.getPageSize())
			self.paramsdict['offset'].append(offset)
		else:
			self.paramsdict['page'] = []
			page = int(int(self.paramsdict['offset'][0]) / int(self.paramsdict['pagesize'][0]) + 1)
			self.paramsdict['page'].append(page)

	def getOffset(self):
		return self.paramsdict['offset'][0]

	def readUsePaging(self):
		self.usepaging = True
		if len(self.paramsdict['usepaging']) > 0:
			if self.paramsdict['usepaging'][0].lower() in ['false', 'no', '0']:
				self.usepaging = False

	def usePaging(self):
		return self.usepaging
