#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Docs: https://docs.easydb.de/en/technical/api/tutorial/python_tutorial/python_tutorial.html

import requests
import logging
log = logging.getLogger('easydb_urls')

from .Getter import Getter

class CollectionGetter(Getter):
	"""Get the data for the available collections (aka pools?)
	"""
	def __init__(self, sessionobj, request):
		Getter.__init__(self, sessionobj, request)
		self.sessionobj = sessionobj
		self.errormessage = ""
		self.token_payload = {"token": self.sessionobj.token, 'pretty': '0'}


	def runCollectionListQuery(self, parent_collection_id = None):
		"""Query the available collections.
		If parent_collection_id is None the top level collections are searched,
		otherwise all child collections of the collection with the given id are searched
		"""
		if parent_collection_id is not None:
			cidpath = "/" + str(parent_collection_id)
		else:
			cidpath = ""
		r = requests.get(self.sessionobj.collectionlist + cidpath, params=self.token_payload, verify=self.sslverify)
		self.sessionobj.searchresult = r.json()

	def appendTraversalList(self, collectionslist):
		try:
			self.traversallist.extend(collectionslist)
		except AttributeError:
			self.traversallist = []
			self.traversallist.extend(collectionslist)

	def getTraversalList(self):
		return self.traversallist

	def getCollectionsList(self, serviceurl):
		"""Return a list with properties of the found collections
		"""
		searchresult = self.sessionobj.searchresult

		self.collectionslist = []

		for collectionobj in searchresult:
			if isinstance(collectionobj, dict) and "collection" in collectionobj:
				try:
					collection_id = collectionobj['collection']['_id']
					collection_childs_url = "{0}{1}".format(serviceurl + "/getChildCollections/", collectionobj['collection']['_id'])
				except KeyError:
					continue
				try:
					collection_parent_id = "{0}{1}".format(serviceurl + "/getCollection/", collectionobj['collection']['_id_parent'])
				except KeyError:
					collection_parent_id = None
				try:
					collectionname_de = collectionobj['collection']['displayname']['de-DE']
				except KeyError:
					collectionname_de = ""
				try:
					collectionname_en = collectionobj['collection']['displayname']['en-US']
				except KeyError:
					collectionname_en = ""
				self.collectionslist.extend([{"Collection Name (de)": collectionname_de, "Collection name (en)": collectionname_en, "collection id": collection_id, "collection parent id": collection_parent_id, "child collections": collection_childs_url}])

		return self.collectionslist

	def runCollectionQuery(self, collection_id = None):
		"""Query the available collections.
		If collection_id is None the top level collections are searched,
		otherwise all child collections of the collection with the given id are searched
		"""
		if collection_id is not None:
			cidpath = "/" + str(collection_id)
		else:
			cidpath = ""
		r = requests.get(self.sessionobj.collection + cidpath, params=self.token_payload, verify=self.sslverify)
		self.sessionobj.searchresult = r.json()
		self.sessionobj.write_json(r.json(), "Collection.json")

	def getCollection(self, serviceurl):
		"""Return a list with properties of the found collections
		"""
		collectionobj = self.sessionobj.searchresult

		self.collection = {}
		if isinstance(collectionobj, dict) and "collection" in collectionobj:
			collection_id = collectionobj['collection']['_id']
			collection_childs_url = "{0}{1}".format(serviceurl + "/getChildCollections/", collectionobj['collection']['_id'])
			try:
				collection_parent_id = "{0}{1}".format(serviceurl + "/getCollection/", collectionobj['collection']['_id_parent'])
			except KeyError:
				collection_parent_id = None
			try:
				collectionname_de = collectionobj['collection']['displayname']['de-DE']
			except KeyError:
				collectionname_de = ""
			try:
				collectionname_en = collectionobj['collection']['displayname']['en-US']
			except KeyError:
				collectionname_en = ""
			self.collection = {"Collection Name (de)": collectionname_de,
								"Collection name (en)": collectionname_en,
								"collection id": collection_id,
								"collection parent id": collection_parent_id,
								"child collections": collection_childs_url}

		return self.collection
