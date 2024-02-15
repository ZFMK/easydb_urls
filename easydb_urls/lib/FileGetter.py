#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from .ListGetter import ListGetter

log = logging.getLogger('easydb_urls')

class FileGetter(ListGetter):
	"""
	Run all steps needed for a search and return a list of URLs for the asset
	"""

	def __init__(self, sessionobj, request, paramsdict = None):
		ListGetter.__init__(self, sessionobj, request, paramsdict = paramsdict)

	def getFile(self, local:bool=False) -> list:
		"""Get all data for an asset: run query to easy db, format the ersult list, return list of urls to files
		"""
		self.runQuery(local)
		self.urls = self.getResultList()
		if len(self.urls)==0:
			return []
		return self.urls[0]['versions']
