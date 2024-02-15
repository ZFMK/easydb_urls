import unittest
from unittest.mock import patch
from pyramid import testing
import easydb_urls.lib.ListGetter as ses


class TestListGetter_API(unittest.TestCase):
	"""API testing: all methods defined and parameters are as expected"""
	def setUp(self):
		self.config = testing.setUp()

	def tearDown(self):
		testing.tearDown()

	def test_is_class_ListGetter(self):
		# see: https://medium.com/@george.shuklin/mocking-complicated-init-in-python-6ef9850dd202
		with patch.object(ses.ListGetter, '__init__', lambda a, b, c, d: None) as p:
			inst = ses.ListGetter(None, None, None)
			self.assertIsInstance(inst, ses.ListGetter)

	def test_exists_Methods(self):
		"""Test method calls (without logic(!))"""
		with patch('easydb_urls.lib.ListGetter.ListGetter', autospec=True) as p:
			self.assertTrue(hasattr(p,'getResultList'))
			p.getResultList()
			self.assertTrue(hasattr(p,'setImages'))
			p.setImages(json_object={}, resultdict={})
			self.assertTrue(hasattr(p,'setPreviewImages'))
			p.setPreviewImages(json_object={}, resultdict={})
			self.assertTrue(hasattr(p,'setSpeciesName'))
			p.setSpeciesName(json_object={}, resultdict={})
			self.assertTrue(hasattr(p,'setAccessionNumber'))
			p.setAccessionNumber(json_object={}, resultdict={})
			self.assertTrue(hasattr(p,'setEasyDBIdentifier'))
			p.setEasyDBIdentifier(json_object={}, resultdict={})
			self.assertTrue(hasattr(p,'setTitle'))
			p.setTitle(json_object={}, resultdict={})

			p.getResultList.assert_called_once()
			p.setImages.assert_called_once_with(json_object={}, resultdict={})
			p.setPreviewImages.assert_called_once_with(json_object={}, resultdict={})
			p.setSpeciesName.assert_called_once_with(json_object={}, resultdict={})
			p.setAccessionNumber.assert_called_once_with(json_object={}, resultdict={})
			p.setEasyDBIdentifier.assert_called_once_with(json_object={}, resultdict={})
			p.setTitle.assert_called_once_with(json_object={}, resultdict={})

if __name__ == '__main__':
	unittest.main()
