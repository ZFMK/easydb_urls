import unittest
from unittest.mock import patch
from pyramid import testing
import easydb_urls.lib.ParamsReader as ses


class TestParamsReader_API(unittest.TestCase):
	"""API testing: all methods defined and parameters are as expected"""
	def setUp(self):
		self.config = testing.setUp()

	def tearDown(self):
		testing.tearDown()

	def test_is_class_ParamsReader(self):
		# see: https://medium.com/@george.shuklin/mocking-complicated-init-in-python-6ef9850dd202
		with patch.object(ses.ParamsReader, '__init__', lambda a, b, c, d: None) as p:
			inst = ses.ParamsReader(None, None, None)
			self.assertIsInstance(inst, ses.ParamsReader)

	def test_exists_Params(self):
		with patch('easydb_urls.lib.ParamsReader.ParamsReader', autospec=True) as p:
			self.assertTrue(hasattr(p,'readParams'))
			p.readParams()
			self.assertTrue(hasattr(p,'separateParams'))
			p.separateParams(separator=";", params2lookup = ["search",])
			self.assertTrue(hasattr(p,'getRequestParamsList'))
			p.getRequestParamsList(params_to_skip=[])
			self.assertTrue(hasattr(p,'getRequestParamsString'))
			p.getRequestParamsString(params_to_skip=[])
			self.assertTrue(hasattr(p,'getParams'))
			p.getParams()

			p.readParams.assert_called_once()
			p.separateParams.assert_called_once_with(separator=";", params2lookup = ["search",])
			p.getRequestParamsList.assert_called_once_with(params_to_skip=[])
			p.getRequestParamsString.assert_called_once_with(params_to_skip=[])
			p.getParams.assert_called_once()

	def test_exists_Page(self):
		with patch('easydb_urls.lib.ParamsReader.ParamsReader', autospec=True) as p:
			self.assertTrue(hasattr(p, 'setPage'))
			p.setPage(page=1)
			self.assertTrue(hasattr(p, 'readPage'))
			p.readPage()
			self.assertTrue(hasattr(p, 'getPage'))
			p.getPage()
			self.assertTrue(hasattr(p, 'readPageSize'))
			p.readPageSize()
			self.assertTrue(hasattr(p, 'getPageSize'))
			p.getPageSize()
			self.assertTrue(hasattr(p, 'setPageSize'))
			p.setPageSize(pagesize=10)

			p.setPage.assert_called_once_with(page=1)
			p.readPage.assert_called_once()
			p.getPage.assert_called_once()
			p.readPageSize.assert_called_once()
			p.getPageSize.assert_called_once()
			p.setPageSize.assert_called_once_with(pagesize=10)

	def test_exists_Limit(self):
		with patch('easydb_urls.lib.ParamsReader.ParamsReader', autospec=True) as p:
			self.assertTrue(hasattr(p, 'setLimit'))
			p.setLimit(limit=10)
			self.assertTrue(hasattr(p, 'readLimit'))
			p.readLimit()
			self.assertTrue(hasattr(p, 'getLimit'))
			p.getLimit()

			p.setLimit.assert_called_once_with(limit=10)
			p.readLimit.assert_called_once()
			p.getLimit.assert_called_once()

	def test_exists_Offset(self):
		with patch('easydb_urls.lib.ParamsReader.ParamsReader', autospec=True) as p:
			self.assertTrue(hasattr(p, 'setOffset'))
			p.setOffset(offset=4)
			self.assertTrue(hasattr(p, 'readOffset'))
			p.readOffset()
			self.assertTrue(hasattr(p, 'getOffset'))
			p.getOffset()

			p.setOffset.assert_called_once_with(offset=4)
			p.readOffset.assert_called_once()
			p.getOffset.assert_called_once()

	def test_exists_Paging(self):
		with patch('easydb_urls.lib.ParamsReader.ParamsReader', autospec=True) as p:
			self.assertTrue(hasattr(p, 'readUsePaging'))
			p.readUsePaging()
			self.assertTrue(hasattr(p, 'usePaging'))
			p.usePaging()

			p.readUsePaging.assert_called_once()
			p.usePaging.assert_called_once()


if __name__ == '__main__':
	unittest.main()
