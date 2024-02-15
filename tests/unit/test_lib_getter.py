import unittest
from unittest.mock import patch
from pyramid import testing
import easydb_urls.lib.Getter as ses


class TestGetter_API(unittest.TestCase):
	"""API testing: all methods defined and parameters are as expected"""
	def setUp(self):
		self.config = testing.setUp()

	def tearDown(self):
		testing.tearDown()

	def test_is_class_Getter(self):
		# see: https://medium.com/@george.shuklin/mocking-complicated-init-in-python-6ef9850dd202
		with patch.object(ses.Getter, '__init__', lambda a, b, c, d, e: None) as p:
			inst = ses.Getter(None, None, None, None)
			self.assertIsInstance(inst, ses.Getter)

	def test_exists_Methods(self):
		"""Test method calls (without logic(!))"""
		with patch('easydb_urls.lib.Getter.Getter', autospec=True) as p:
			self.assertTrue(hasattr(p,'runQuery'))
			p.runQuery(local=False)
			self.assertTrue(hasattr(p,'getSearchParams'))
			p.getSearchParams()
			self.assertTrue(hasattr(p,'getResultCount'))
			p.getResultCount()
			self.assertTrue(hasattr(p,'getPageSize'))
			p.getPageSize()
			self.assertTrue(hasattr(p,'getMaxPage'))
			p.getMaxPage()
			self.assertTrue(hasattr(p,'getResultLimit'))
			p.getResultLimit()
			self.assertTrue(hasattr(p,'getResultOffset'))
			p.getResultOffset()
			self.assertTrue(hasattr(p,'setPage'))
			p.setPage(page=1)
			self.assertTrue(hasattr(p,'setPageSize'))
			p.setPageSize(pagesize=10)
			self.assertTrue(hasattr(p,'setLimit'))
			p.setLimit(limit=10)
			self.assertTrue(hasattr(p,'getCurrentPage'))
			p.getCurrentPage()
			self.assertTrue(hasattr(p,'getRequestParamsString'))
			p.getRequestParamsString(params_to_skip = [])

			p.runQuery.assert_called_once_with(local=False)
			p.getSearchParams.assert_called_once()
			p.getResultCount.assert_called_once()
			p.getPageSize.assert_called_once()
			p.getMaxPage.assert_called_once()
			p.getResultLimit.assert_called_once()
			p.getResultOffset.assert_called_once()
			p.setPage.assert_called_once_with(page=1)
			p.setPageSize.assert_called_once_with(pagesize=10)
			p.setLimit.assert_called_once_with(limit=10)
			p.getCurrentPage.assert_called_once()
			p.getRequestParamsString.assert_called_once_with(params_to_skip = [])




if __name__ == '__main__':
	unittest.main()
