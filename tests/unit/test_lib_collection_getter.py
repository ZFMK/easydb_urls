import unittest
from unittest.mock import patch
from pyramid import testing
import easydb_urls.lib.CollectionGetter as ses


class TestCollectionGetter_API(unittest.TestCase):
	"""API testing: all methods defined and parameters are as expected"""
	def setUp(self):
		self.config = testing.setUp()

	def tearDown(self):
		testing.tearDown()

	def test_is_class_CollectionGetter(self):
		# see: https://medium.com/@george.shuklin/mocking-complicated-init-in-python-6ef9850dd202
		with patch.object(ses.CollectionGetter, '__init__', lambda a, b, c: None) as p:
			inst = ses.CollectionGetter(None, None)
			self.assertIsInstance(inst, ses.CollectionGetter)

	def test_exists_Methods(self):
		"""Test method calls (without logic(!))"""
		with patch('easydb_urls.lib.CollectionGetter.CollectionGetter', autospec=True) as p:
			self.assertTrue(hasattr(p,'runCollectionListQuery'))
			p.runCollectionListQuery(parent_collection_id = None)
			self.assertTrue(hasattr(p,'appendTraversalList'))
			p.appendTraversalList(collectionslist=[])
			self.assertTrue(hasattr(p,'getTraversalList'))
			p.getTraversalList()
			self.assertTrue(hasattr(p,'getCollectionsList'))
			p.getCollectionsList(serviceurl="")
			self.assertTrue(hasattr(p,'runCollectionQuery'))
			p.runCollectionQuery(collection_id=None)
			self.assertTrue(hasattr(p,'getCollection'))
			p.getCollection(serviceurl="")

			p.runCollectionListQuery.assert_called_once_with(parent_collection_id = None)
			p.appendTraversalList.assert_called_once_with(collectionslist=[])
			p.getTraversalList.assert_called_once()
			p.getCollectionsList.assert_called_once_with(serviceurl="")
			p.runCollectionQuery.assert_called_once_with(collection_id=None)
			p.getCollection.assert_called_once_with(serviceurl="")

if __name__ == '__main__':
	unittest.main()
