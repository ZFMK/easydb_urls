import unittest
from unittest.mock import patch
from pyramid import testing
import easydb_urls.lib.ObjectGetter as ses


class TestObjectGetter_API(unittest.TestCase):
	"""API testing: all methods defined and parameters are as expected"""
	def setUp(self):
		self.config = testing.setUp()

	def tearDown(self):
		testing.tearDown()

	def test_is_class_ObjectGetter(self):
		# see: https://medium.com/@george.shuklin/mocking-complicated-init-in-python-6ef9850dd202
		with patch.object(ses.ObjectGetter, '__init__', lambda a, b, c: None) as p:
			inst = ses.ObjectGetter(None, None)
			self.assertIsInstance(inst, ses.ObjectGetter)

	def test_exists_Methods(self):
		"""Test method calls (without logic(!))"""
		with patch('easydb_urls.lib.ObjectGetter.ObjectGetter', autospec=True) as p:
			self.assertTrue(hasattr(p,'getJSONPage'))
			p.getJSONPage()
			self.assertTrue(hasattr(p,'getFirstPageURL'))
			p.getFirstPageURL()

			p.getJSONPage.assert_called_once()
			p.getFirstPageURL.assert_called_once()

if __name__ == '__main__':
	unittest.main()
