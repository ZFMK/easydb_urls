import unittest
from unittest.mock import patch
from pyramid import testing
import easydb_urls.lib.FileGetter as ses


class TestFileGetter_API(unittest.TestCase):
	"""API testing: all methods defined and parameters are as expected"""
	def setUp(self):
		self.config = testing.setUp()

	def tearDown(self):
		testing.tearDown()

	def test_is_class_FileGetter(self):
		# see: https://medium.com/@george.shuklin/mocking-complicated-init-in-python-6ef9850dd202
		with patch.object(ses.FileGetter, '__init__', lambda a, b, c, d: None) as p:
			inst = ses.FileGetter(None, None, None)
			self.assertIsInstance(inst, ses.FileGetter)

	def test_exists_Methods(self):
		"""Test method calls (without logic(!))"""
		with patch('easydb_urls.lib.FileGetter.FileGetter', autospec=True) as p:
			self.assertTrue(hasattr(p,'getFile'))
			p.getFile(local=False)

			p.getFile.assert_called_once_with(local=False)

if __name__ == '__main__':
	unittest.main()
