#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Docs: https://docs.easydb.de/en/technical/api/tutorial/python_tutorial/python_tutorial.html


import logging
import requests_cache
from pyramid.httpexceptions import HTTPNotFound, HTTPUnauthorized
from configparser import ConfigParser

from .Getter import Getter

log = logging.getLogger('easydb_urls')
config = ConfigParser()
config.read('./easydb_urls/config.ini')

urls_expire_after = {
    'media.leibniz-lib.de/api/v1/objects/id/*': 3600
}
cache_session = requests_cache.CachedSession('http_cache',
											 backend='filesystem',
											 use_cache_dir=True,
											 use_temp=True,
											 ignored_parameters=['params'],
											 urls_expire_after=urls_expire_after)


class BadRequest(Exception):
	def __init__(self, error_message:str="", url:str="", detail:str=None):
		Exception.__init__(self, error_message)
		self.error_message = error_message
		self.url = url
		self.detail = detail

	def __str__(self):
		if self.detail is not None:
			return "{0} in {1} for requesting {2}: {3}".format(self.error_message, __name__, self.url, self.detail)
		else:
			return "{0} in {1} for requesting {2}".format(self.error_message, __name__, self.url)

class ImageResolver(Getter):
	"""Get a URL for a given asset id
	"""
	def __init__(self, sessionobj, request, assetid, size = None, preferredsize = []):
		Getter.__init__(self, sessionobj, request)
		self.assetid = assetid
		self.size = size
		if self.size is None:
			self.size = 'original'
		self.errormessage = ""
		self.preferredsize = preferredsize
		self.url = None

	def runResolveQuery(self) -> None:
		"""Get the metadata for a given asset id"""
		if self.is_diversity_workbench_request():
			log.debug("Serve smallest image for DiversityWorkbench")
			self.preferredsize = ['small']
		url = "{0}/id/{1}".format(self.sessionobj.objects, self.assetid)
		log.debug("runResolveQuery url: %s" % url)
		r = cache_session.get(url, params=self.token_payload, verify=self.sslverify)
		if r.status_code != 200:
			raise BadRequest(r.reason, url, r.text)
		log.debug("Got json metadata for image from cache: {}".format(True if r.from_cache else False))
		self.sessionobj.searchresult = r.json()

	def is_diversity_workbench_request(self) -> bool:
		"""If referring IP matches one of the configured IPs for Diversity Workbench, return True"""
		diversity_workbench_host_ip = config.get('easydb_api', 'diversity_workbench_host_ip')
		try:
			log.debug("Remote Addr: {0}, HTTP_USER_AGENT: {1}".format(self.request.remote_addr, (self.request.environ['HTTP_USER_AGENT'])))
		except KeyError:
			log.debug("Remote Addr: {0}, HTTP_USER_AGENT: None".format(self.request.remote_addr))
		if self.request.remote_addr in diversity_workbench_host_ip.split(';'):
			return True
		return False

	def getAssetURL(self):
		"""Return a URL for the first version in found object"""
		searchresult = self.sessionobj.searchresult

		try:
			json_versions = self.sessionobj.searchresult['objekte']['datei'][-1]['versions']
		except KeyError:
			raise HTTPNotFound()
		sizes = ['original', 'full', 'huge', 'preview', 'small']
		if len(self.preferredsize) > 0:
			if self.preferredsize[0].lower() in ['small', 'smallest']:
				sizes = list(reversed(sizes))
		elif self.size in json_versions.keys() and self.size in sizes:
			sizes = sizes[sizes.index(self.size):]  # reduce list equal or less than requested size
		else:
			raise HTTPNotFound()
		for size in sizes:
			if '_not_allowed' in json_versions[size]:
				continue
			try:
				self.url = json_versions[size]['url']
				return self.url
			except KeyError:
				pass
		raise HTTPUnauthorized()

	def getAssetOriginalFilename(self):
		"""Return a URL for the first version in found object"""
		try:
			return self.sessionobj.searchresult['objekte']['datei'][-1]['original_filename_basename']
		except KeyError:
			return ''
