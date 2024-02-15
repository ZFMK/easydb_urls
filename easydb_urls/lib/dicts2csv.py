#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
log = logging.getLogger('easydb_urls')

class Dicts2CSV():
	def __init__(self):
		self.headers = ["Preview", "File / Image original", "Image full", "Image huge", "Image small", "EasyDB page", "CETAF Stable ID", "Species", "Locality"]
		self.resultlists = []
		self.csvstring = ""

	def addHeaderRow(self)->None:
		self.resultlists.insert(0, self.headers)

	def addDataRows(self, resultdicts:list)->None:
		for obj in resultdicts:
			result = []
			try:
				result.append("{0}".format(obj['preview_url']))
			except KeyError:
				result.append("")
			
			imagelinks = {
					"original": "",
					"full": "",
					"huge": "",
					"small": ""
				}
			try:
				images = obj['versions']
				for image in images:
					imagelinks[image['size']] = image['url']
			except KeyError:
				pass
			result.extend([imagelinks['original'], imagelinks['full'], imagelinks['huge'], imagelinks['small']])
			
			try:
				result.append("https://media.zfmk.de/detail/{0}".format(obj['identifier']))
			except KeyError:
				result.append("")
			try:
				result.append("https://id.zfmk.de/collection_ZFMK/?AccessionNumber={0}".format(obj['accessionnumber']))
			except KeyError:
				result.append("")
			try:
				result.append(obj['speciesname'].replace("<em>", "").replace("</em>", ""))
			except KeyError:
				result.append("")
			try:
				result.append(obj['locality'])
			except KeyError:
				result.append("")
			
			# replace None values with empty string
			# otherwise add it to the list as it is
			resultitems = []
			for element in result:
				if element is None:
					element = ""
				resultitems.append(element)
			
			self.resultlists.append(resultitems)

	def setCSVString(self)->None:
		resultstrings = []
		for resultlist in self.resultlists:
			resultstring = '"' + '", "'.join(resultlist) + '"'
			resultstrings.append(resultstring)
		
		self.csvstring = "\n".join(resultstrings)

	def getCSVString(self)->str:
		self.setCSVString()
		return self.csvstring
