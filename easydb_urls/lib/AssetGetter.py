#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Docs: https://docs.easydb.de/en/technical/api/tutorial/python_tutorial/python_tutorial.html

import requests
import logging

from .Getter import Getter

log = logging.getLogger('easydb_urls')

class AssetGetter(Getter):
	"""Get the data for an asset with the given id
	"""

	def __init__(self, sessionobj, request, assetid):
		Getter.__init__(self, sessionobj, request)
		self.sessionobj = sessionobj
		self.assetid = assetid

	def runQuery(self):
		"""Overwrites runQuery from Getter class
		"""
		tokenpayload = {"token": self.sessionobj.token, 'pretty': '0'}

		objectpath = "/id/{0}".format(self.assetid)
		r = requests.get(self.sessionobj.objects + objectpath, params=tokenpayload, verify=self.sslverify)
		self.sessionobj.searchresult = r.json()

	def getJSON(self):
		return self.sessionobj.searchresult
