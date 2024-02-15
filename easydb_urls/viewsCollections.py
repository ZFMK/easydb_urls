import json
import logging

from pyramid.view import (view_config, view_defaults)
from configparser import ConfigParser

from .lib.CollectionGetter import CollectionGetter
from .lib.SessionEAS import SessionEAS

config = ConfigParser()
config.read('./easydb_urls/config.ini')
log = logging.getLogger(__name__)

# @view_defaults(route_name='specimens')
class eaCollectionViews(object):
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

	##############################################
	# content negotiation on /search/ path
	##############################################


	@view_config(route_name='getCollectionJSON', renderer="json")
	@view_config(route_name='getCollection', accept='application/json', renderer="json")
	def getCollection(self):
		"""Search for the file urls, i. e. easyDB url to a file
		"""
		colid = self.request.matchdict['collection_id']
		if len(colid) > 0:
			colid = colid[0]
		else:
			colid = None

		serviceurl = self.request.application_url + "/json"

		collectionsgetter = CollectionGetter(self.sessionobj, self.request)
		collectionsgetter.runCollectionQuery(collection_id = colid)
		collectionslist = collectionsgetter.getCollection(serviceurl = serviceurl)

		return collectionslist

	@view_config(route_name='getChildCollectionsJSON', renderer="json")
	@view_config(route_name='getChildCollections', accept='application/json', renderer="json")
	def getChildCollections(self):
		"""Search for the file urls, i. e. easyDB url to a file
		"""
		pcolid = self.request.matchdict['parent_collection_id']
		if len(pcolid) > 0:
			pcolid = pcolid[0]
		else:
			pcolid = None

		serviceurl = self.request.application_url + "/json"

		collectionsgetter = CollectionGetter(self.sessionobj, self.request)
		collectionsgetter.runCollectionListQuery(parent_collection_id = pcolid)
		collectionslist = collectionsgetter.getCollectionsList(serviceurl = serviceurl)

		collectionsgetter.appendTraversalList(collectionslist)
		collectionslist = self.traverseCollectionsTree(collectionsgetter, collectionslist, serviceurl)

		return collectionslist

	def traverseCollectionsTree(self, collectionsgetter, collectionslist, serviceurl):
		"""Start from top level collection and traverse to the leves
		"""
		for collection in collectionslist:
			if "collection id" in collection:
				collectionsgetter.runCollectionListQuery(parent_collection_id = collection['collection id'])
				collectionslist = collectionsgetter.getCollectionsList(serviceurl = serviceurl)
				if len(collectionslist) > 0:
					collectionsgetter.appendTraversalList(collectionslist)
					self.traverseCollectionsTree(collectionsgetter, collectionslist, serviceurl)
		collectionslist = collectionsgetter.getTraversalList()
		return collectionslist
