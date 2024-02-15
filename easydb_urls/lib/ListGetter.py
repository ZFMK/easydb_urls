#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
iterate over found json results an create a list of result entries with some data on each entry
"""

import re
import logging

from .Getter import Getter

log = logging.getLogger('easydb_urls')


class ListGetter(Getter):
	"""Run all steps needed for a search and return a list of file entries as python dictionaries
	"""
	def __init__(self, sessionobj, request, paramsdict = None):
		Getter.__init__(self, sessionobj, request, paramsdict = paramsdict)
		self.application_url = request.application_url
		self.resultdicts = []

	def getResultList(self) -> list:
		"""Get list of avaliables image versions from session obj or from json object
			Always set the resultlist to the currenty fetched data,
			in case listegetter was called repeately, e. g. with new page number set

			:returns: list
		"""
		self.resultdicts = []

		# try to get results from session object
		searchresult = self.sessionobj.getResultDict()
		if not 'objects' in searchresult:
			return self.resultdicts

		log.info('%s.setResultList: number of objects found: %r' % (__name__, len(searchresult['objects'])))
		for json_object in searchresult['objects']:
			resultdict = {}
			if not '_objecttype' in json_object or json_object['_objecttype']!='objekte':
				continue
			else:
				try:
					resultdict['locality'] = json_object['objekte']['aufnahmeort_lokalitaet']
				except KeyError:
					resultdict['locality'] = None
				
				#look if there are images and get them, otherwise skip the entry
				resultdict = self.setImages(json_object, resultdict)
				# look if there is a preview image
				resultdict = self.setPreviewImages(json_object, resultdict)
				# look for species name
				resultdict = self.setSpeciesName(json_object, resultdict)
				# look for accession number
				resultdict = self.setAccessionNumber(json_object, resultdict)
				# look for easydb's _system_object_id
				resultdict = self.setEasyDBIdentifier(json_object, resultdict)
				# look for the title if there is any
				resultdict = self.setTitle(json_object, resultdict)

			self.resultdicts.append(resultdict)
			#print(resultdict)
		return self.resultdicts

	def setImages(self, json_object, resultdict):
		"""For each possible asset view create urls that resolve to the files in easydb
		"""
		filesizes = ['original', 'full', 'huge', 'small']
		versions = []
		try:
			json_datei = json_object['objekte']['datei'][0] # -- only the image version set as default for viewer in easydb
		except KeyError:
			#log.debug('No file in %s' % json_object['_global_object_id'])
			resultdict['versions'] = []
			return resultdict
		
		for filesize in filesizes:
			if not filesize in json_datei['versions']:
				continue
			if ('status' in json_datei['versions'][filesize] and
						json_datei['versions'][filesize]['status'] == 'done' and
					json_datei['versions'][filesize]['_download_allowed'] and
						json_datei['versions'][filesize]['_download_allowed'] is True):
				entry = json_datei['versions'][filesize]
				try:
					entry.update({'filename_base': json_datei['original_filename_basename']})
				except KeyError:
					entry.update({'filename_base': json_datei['name']})
				entry.update({
					'identifier': json_object['_system_object_id'],
					'size': filesize,
					'class': json_datei['class']
				})
				if json_datei['class']=='image':
					entry['url'] = '{0}/{class}/{identifier}/full/{size}/0/{filename_base}.{extension}'.format(self.application_url, **entry)
				else:
					entry['url'] = '{0}/asset/{class}/{identifier}/{size}/{filename_base}.{extension}'.format(self.application_url, **entry)
				versions.append(entry)
		resultdict['versions'] = versions
		return resultdict

	@staticmethod
	def setPreviewImages(json_object, resultdict):
		"""Get preview from asset for display in result list
		"""
		try:
			resultdict['preview_url'] = json_object['objekte']['datei'][0]['versions']['preview']['url']
		except KeyError:
			if 'preview' in json_object['objekte'] and len(json_object['objekte']['preview'])>0:
				# -- for e.g. archives
				try:
					resultdict['preview_url'] = json_object['objekte']['preview'][0]['versions']['preview']['url']
				except KeyError:
					resultdict['preview_url'] = None
			else:
				resultdict['preview_url'] = None
		if resultdict['preview_url'] is None:
			try:
				# use index -1 to get the smallest available version
				if resultdict['versions'][-1]['class'] == 'image':
					try:
						resultdict['preview_url'] = resultdict['versions'][-1]['url']
					except KeyError:
						pass
			except KeyError:
				pass
			except IndexError:
				pass
		return resultdict

	def setSpeciesName(self, json_object, resultdict):
		"""Get species name from asset (in objekte__organismen->lk_taxonnames_id)
		"""
		try:
			resultdict['identification'] = json_object['objekte']['_nested:objekte__organismen'][0]['lk_taxonnames_id']['_standard']['1']['text']['de-DE']
			resultdict['speciesname'] = self.__get_formatted_species_name(resultdict['identification'])
		except KeyError:
			pass
		except IndexError:
			pass
		return resultdict

	@staticmethod
	def __get_formatted_species_name(species_name:str) -> str:
		"""Return species name string with html markup for italics
		"""
		pattern = re.compile(r'\s*([A-Z]\w+)(\s+((spec|sp|cf)\.))?(\s+([a-z]+))?')
		# not working in python 3.4
		#replacement = r'<em>\1</em> \3 <em>\6</em>'
		#speciesname = pattern.sub(replacement, identification, 1)
		
		# workarround for python 3.4
		sp = pattern.match(species_name)
		if sp is not None:
			replacement = '<em>{0}</em>{1}<em>{2}</em>'.format(sp.group(1), sp.group(2), sp.group(5))
			replacement = replacement.replace('None', '')
			species_name = pattern.sub(replacement, species_name, 1)
		else:
			pass
		return species_name

	@staticmethod
	def setAccessionNumber(json_object, resultdict):
		"""Get Accession nmuber(s) name from asset (in objekte__organismen->sammlungsnummer)
		"""
		try:
			resultdict['accessionnumber'] = json_object['objekte']['_nested:objekte__organismen'][0]['sammlungsnummer']
		except KeyError:
			pass
		except IndexError:
			pass
		return resultdict

	@staticmethod
	def setEasyDBIdentifier(json_object, resultdict):
		"""Get (unique) system object id for asset)
		"""
		try:
			resultdict['identifier'] = json_object['_system_object_id']
		except KeyError:
			pass
		return resultdict

	@staticmethod
	def setTitle(json_object, resultdict):
		"""Get asset title
		"""
		try:
			resultdict['title'] = json_object['objekte']['title']
		except KeyError:
			pass
		return resultdict
