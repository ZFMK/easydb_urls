#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Docs: https://docs.easydb.de/en/technical/api/tutorial/python_tutorial/python_tutorial.html

import logging

from .Getter import Getter

log = logging.getLogger('easydb_urls')

class ObjectGetter(Getter):
	"""Return the URL of the first easydb result page that matches a search
	or return the found results as json object, then it contains all found results
	"""

	def __init__(self, sessionobj, request):
		Getter.__init__(self, sessionobj, request)

	def getJSONPage(self):
		return self.sessionobj.getResult_JSON()

	def getFirstPageURL(self):
		searchresult = self.sessionobj.getResultDict()

		if not 'objects' in searchresult:
			return None
		for json_object in searchresult['objects']:
			if not '_objecttype' in json_object or json_object['_objecttype']!='objekte':
				continue
			else:
				pageurl = "{0}/detail/{1}".format(self.baseurl, int(json_object['_system_object_id']))
			return pageurl
		return None
