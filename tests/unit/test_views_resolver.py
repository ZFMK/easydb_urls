import unittest
from unittest.mock import patch
from pyramid import testing
from easydb_urls.viewsResolver import eaResolverViews as View, get_image, ImageLoadError



class TestViewsResolver_API(unittest.TestCase):
	"""API testing: all methods defined and parameters are as expected"""
	def setUp(self):
		self.config = testing.setUp()

	def tearDown(self):
		testing.tearDown()

	def test_is_class_eaResolverViews(self):
		# see: https://medium.com/@george.shuklin/mocking-complicated-init-in-python-6ef9850dd202
		with patch.object(View, '__init__', lambda a, b: None) as p:
			inst = View(None)
			self.assertIsInstance(inst, View)

	@patch('easydb_urls.viewsResolver.get_image')
	def test_exists_resolveImage(self, mock_get_image):
		"""Test method calls (without logic(!))"""
		mock_get_image.return_value= {}
		with patch('easydb_urls.viewsResolver.eaResolverViews', autospec=True) as p:
			self.assertTrue(hasattr(p,'resolveImage'))
			p.resolveImage()

			p.resolveImage.assert_called_once()

	"""@patch('easydb_urls.viewsResolver.cache_session.get')
	def test_getImage_found(self, mock_get):
		mock_get.return_value.status_code = 200
		mock_get.return_value.headers = {'content-type': 'image/png'}
		response = get_image('https://example.com/test.png')
		self.assertEqual(response.status_code, 200)

	@patch('easydb_urls.viewsResolver.cache_session.get')
	def test_getImage_not_found(self, mock_get):
		mock_get.return_value.status_code = 404
		mock_get.return_value.text = "{'error': 'image not found'}"
		with self.assertRaises(ImageLoadError):
			response = get_image('https://example.com/test.png')"""

if __name__ == '__main__':
	unittest.main()
