import unittest
from unittest.mock import patch
from pyramid import testing
import easydb_urls.lib.dicts2csv as ses


class Testdicts2csv_API(unittest.TestCase):
	"""API testing: all methods defined and parameters are as expected"""
	def setUp(self):
		self.config = testing.setUp()

	def tearDown(self):
		testing.tearDown()

	def test_is_class_dicts2csv(self):
		# see: https://medium.com/@george.shuklin/mocking-complicated-init-in-python-6ef9850dd202
		with patch.object(ses.Dicts2CSV, '__init__', lambda a, b, c, d: None) as p:
			inst = ses.Dicts2CSV(None, None, None)
			self.assertIsInstance(inst, ses.Dicts2CSV)

	def test_exists_Methods(self):
		"""Test method calls (without logic(!))"""
		with patch('easydb_urls.lib.dicts2csv.Dicts2CSV', autospec=True) as p:
			self.assertTrue(hasattr(p,'addHeaderRow'))
			p.addHeaderRow()
			self.assertTrue(hasattr(p,'addDataRows'))
			p.addDataRows(resultdicts=[])
			self.assertTrue(hasattr(p,'setCSVString'))
			p.setCSVString()
			self.assertTrue(hasattr(p,'getCSVString'))
			p.getCSVString()

			p.addHeaderRow.assert_called_once()
			p.addDataRows.assert_called_once_with(resultdicts=[])
			p.setCSVString.assert_called_once()
			p.getCSVString.assert_called_once()

if __name__ == '__main__':
	unittest.main()
