import unittest
from pyramid import testing

class TestPyramidSession(unittest.TestCase):
	def setUp(self):
		from easydb_urls.lib.PyramidSession import SessionAuthentication
		self.config = testing.setUp()
		request = testing.DummyRequest()
		self.session_auth_instance = SessionAuthentication(request)

	def tearDown(self):
		testing.tearDown()

	def test_set_session_token(self):
		self.session_auth_instance.setSessionToken(sessiontoken='1234')
		self.assertEqual(self.session_auth_instance.request.session['eastoken'], '1234')

	def test_get_session_token(self):
		self.session_auth_instance.request.session['eastoken']='1234'
		self.assertEqual(self.session_auth_instance.getSessionToken(), '1234')


if __name__ == '__main__':
	unittest.main()
