import json
import logging
import requests_cache
from configparser import ConfigParser

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPUnauthorized

from .lib.Resolvers import ImageResolver
from .lib.ParamsReader import ParamsReader
from .lib.SessionEAS import SessionEAS

log = logging.getLogger(__name__)
config = ConfigParser()
config.read('./easydb_urls/config.ini')


class ImageLoadError(Exception):
	def __init__(self, error_message:str=""):
		Exception.__init__(self, error_message)
		self.error_message = error_message

	def __str__(self):
		return "Image Load Error in {0}: {1}".format(__name__, self.error_message)

cache_session = requests_cache.CachedSession('http_cache', backend='filesystem', use_cache_dir=True, use_temp=True)

class eaResolverViews(object):
	"""Resolve the urls got from ListGetter to the real assets
	"""
	def __init__(self, request):
		self.request = request
		self.baseurl = config.get('easydb_api', 'baseurl')
		self.sessionobj = SessionEAS(self.request)
		self.paramsreader = ParamsReader(self.request)
		self.queryparams = self.paramsreader.getParams()
		self.preferredsize = self.queryparams['preferredsize']

	@view_config(route_name='resolveImage')
	@view_config(route_name='resolveAsset')
	@view_config(route_name='resolveImageByID')
	def resolveImage(self):
		"""Redirect to the url of an image asset
		"""
		#ToDo: ensure right URL format (/image/56367/full/small/0/ZFMK_207976.png)
		assetid = self.request.matchdict['assetid']
		if 'size' in self.request.matchdict:
			size = self.request.matchdict['size']
		else:
			size = None
		
		imageresolver = ImageResolver(self.sessionobj, self.request, assetid, size, self.preferredsize)
		imageresolver.runResolveQuery()
		if 'filename' in self.request.matchdict:
			requested_filename = '.'.join(self.request.matchdict['filename'].split('.')[:-1])
			if imageresolver.getAssetOriginalFilename()!=requested_filename:
				return HTTPNotFound()
		try:
			url = imageresolver.getAssetURL()
		except HTTPNotFound:
			return HTTPNotFound()
		except HTTPUnauthorized:
			return HTTPUnauthorized()
		return get_image(url=url)
		
def get_image(url:str):
	log.debug("get_image url: %s" % url)
	r = cache_session.get(url)
	if r.status_code != 200:
		raise ImageLoadError(json.loads(r.text))
	log.debug("Got image from cache: {}".format(True if r.from_cache else False))

	response = Response(content_type=r.headers.get('content-type'))
	response.body = r.content
	return response

