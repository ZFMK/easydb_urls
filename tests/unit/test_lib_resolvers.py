import unittest
from unittest.mock import patch
from pyramid import testing
import easydb_urls.lib.Resolvers as res


class TestResolvers_API(unittest.TestCase):
	"""API testing: all methods defined and parameters are as expected"""
	def setUp(self):
		self.config = testing.setUp()

	def tearDown(self):
		testing.tearDown()

	def test_is_class_ImageResolver(self):
		# see: https://medium.com/@george.shuklin/mocking-complicated-init-in-python-6ef9850dd202
		with patch.object(res.ImageResolver, '__init__', lambda a, b, c, d, e, f: None) as p:
			inst = res.ImageResolver(None, None, None, None, None)
			self.assertIsInstance(inst, res.ImageResolver)

	def test_exists_Methods(self):
		"""Test method calls (without logic(!))"""
		with patch('easydb_urls.lib.Resolvers.ImageResolver', autospec=True) as p:
			self.assertTrue(hasattr(p,'runResolveQuery'))
			p.runResolveQuery()
			self.assertTrue(hasattr(p,'getAssetURL'))
			p.getAssetURL()
			self.assertTrue(hasattr(p,'is_diversity_workbench_request'))
			p.is_diversity_workbench_request()

			p.runResolveQuery.assert_called_once()
			p.getAssetURL.assert_called_once()
			p.is_diversity_workbench_request.assert_called_once()

class TestResolvers_Function(unittest.TestCase):
	"""API testing: all methods defined and parameters are as expected"""

	def setUp(self):
		import easydb_urls.lib.SessionEAS as ses
		self.config = testing.setUp()
		request = testing.DummyRequest()
		request.remote_addr = '10.0.2.23'
		sessionobj = ses.SessionEAS(request)
		self.instance = res.ImageResolver(sessionobj, request, 1234, 'small', [])

	def tearDown(self):
		testing.tearDown()

	def test_diversity_workbench_ip_true(self):
		self.instance.request.remote_addr = '10.0.2.23'
		self.assertTrue(self.instance.is_diversity_workbench_request())

	def test_diversity_workbench_ip_false(self):
		self.instance.request.remote_addr = '10.0.2.22'
		self.assertFalse(self.instance.is_diversity_workbench_request())

	def test_diversity_workbench_is_smallest(self):
		with patch('easydb_urls.lib.Resolvers.requests_cache.session.CachedSession.get') as mock_get:
			mock_get.return_value.status_code = 200
			mock_get.return_value.encoding = 'utf-8'
			mock_get.return_value.content = {}
			mock_get.return_value.text = '{}'
			self.instance.request.remote_addr = '10.0.2.23'
			self.instance.runResolveQuery()
			self.assertEqual(self.instance.preferredsize, ['small'], "Smallest possible image not returned")


if __name__ == '__main__':
	unittest.main()
