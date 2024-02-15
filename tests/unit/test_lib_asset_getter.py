import unittest
from unittest.mock import patch
from pyramid import testing
import easydb_urls.lib.AssetGetter as ses


class TestAssetGetter_API(unittest.TestCase):
	"""API testing: all methods defined and parameters are as expected"""
	def setUp(self):
		self.config = testing.setUp()

	def tearDown(self):
		testing.tearDown()

	def test_is_class_AssetGetter(self):
		# see: https://medium.com/@george.shuklin/mocking-complicated-init-in-python-6ef9850dd202
		with patch.object(ses.AssetGetter, '__init__', lambda a, b, c, d: None) as p:
			inst = ses.AssetGetter(None, None, None)
			self.assertIsInstance(inst, ses.AssetGetter)

	def test_exists_Methods(self):
		"""Test method calls (without logic(!))"""
		with patch('easydb_urls.lib.AssetGetter.AssetGetter', autospec=True) as p:
			self.assertTrue(hasattr(p,'runQuery'))
			p.runQuery()
			self.assertTrue(hasattr(p,'getJSON'))
			p.getJSON()

			p.runQuery.assert_called_once()
			p.getJSON.assert_called_once()

if __name__ == '__main__':
	unittest.main()
