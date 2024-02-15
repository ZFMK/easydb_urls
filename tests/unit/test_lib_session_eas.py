import unittest
from unittest.mock import patch
from pyramid import testing
import easydb_urls.lib.SessionEAS as ses


class TestSessionEAS_API(unittest.TestCase):
	"""API testing: all methods defined and parameters are as expected"""
	def setUp(self):
		self.config = testing.setUp()

	def tearDown(self):
		testing.tearDown()

	def test_is_class_SessionEAS(self):
		# see: https://medium.com/@george.shuklin/mocking-complicated-init-in-python-6ef9850dd202
		with patch.object(ses.SessionEAS, '__init__', lambda x, y: None) as p:
			session_auth_instance = ses.SessionEAS(None)
			self.assertIsInstance(session_auth_instance, ses.SessionEAS)

	def test_exists_setApiPaths(self):
		with patch('easydb_urls.lib.SessionEAS.SessionEAS', autospec=True) as p:
			self.assertTrue(hasattr(p,'setApiPaths'))
			p.setApiPaths()
		p.setApiPaths.assert_called_once()

	def test_exists_getCredentialsFromParams(self):
		with patch('easydb_urls.lib.SessionEAS.SessionEAS', autospec=True) as p:
			self.assertTrue(hasattr(p,'getCredentialsFromParams'))
			p.getCredentialsFromParams()
		p.getCredentialsFromParams.assert_called_once()

	def test_exists_setCredentialsFromParams(self):
		with patch('easydb_urls.lib.SessionEAS.SessionEAS', autospec=True) as p:
			self.assertTrue(hasattr(p,'setCredentialsFromParams'))
			p.setCredentialsFromParams()
		p.setCredentialsFromParams.assert_called_once()

	def test_exists_setCredentials(self):
		with patch('easydb_urls.lib.SessionEAS.SessionEAS', autospec=True) as p:
			self.assertTrue(hasattr(p, 'setCredentials'))
			p.setCredentials(user='username', password='password')
		p.setCredentials.assert_called_once_with(user='username', password='password')

	def test_exists_getSessionAuthentication(self):
		with patch('easydb_urls.lib.SessionEAS.SessionEAS', autospec=True) as p:
			self.assertTrue(hasattr(p, 'getSessionAuthentication'))
			p.getSessionAuthentication()
		p.getSessionAuthentication.assert_called_once()

	def test_exists_registerNewSession(self):
		with patch('easydb_urls.lib.SessionEAS.SessionEAS', autospec=True) as p:
			self.assertTrue(hasattr(p, 'registerNewSession'))
			p.registerNewSession()
		p.registerNewSession.assert_called_once()

	def test_exists_start_session(self):
		with patch('easydb_urls.lib.SessionEAS.SessionEAS', autospec=True) as p:
			self.assertTrue(hasattr(p, 'start_session'))
			p.start_session()
		p.start_session.assert_called_once()

	"""def test_exists_start_session_works(self):
		request = testing.DummyRequest()
		initialized_session = ses.SessionEAS(request)
		with patch('easydb_urls.lib.SessionEAS.SessionEAS.start_session', autospec=True) as p:
			p.content = {'frontend_language': 'de-DE'}
			p.header = {'Content-Type': 'application/json; charset=utf-8'}
			initialized_session.start_session()
			self.assertEqual(initialized_session.content['frontend_language'], p.content['frontend_language'])
			self.assertEqual(initialized_session.header['Content-Type'], p.header['Content-Type'])"""

	def test_exists_retrieve_session_by_token(self):
		with patch('easydb_urls.lib.SessionEAS.SessionEAS', autospec=True) as p:
			self.assertTrue(hasattr(p, 'retrieve_session_by_token'))
			p.retrieve_session_by_token(token='token')
		p.retrieve_session_by_token.assert_called_once_with(token='token')

	def test_exists_getLogin(self):
		with patch('easydb_urls.lib.SessionEAS.SessionEAS', autospec=True) as p:
			self.assertTrue(hasattr(p, 'getLogin'))
			p.getLogin()
		p.getLogin.assert_called_once()

	def test_exists_authenticate_session(self):
		with patch('easydb_urls.lib.SessionEAS.SessionEAS', autospec=True) as p:
			self.assertTrue(hasattr(p, 'authenticate_session'))
			p.authenticate_session()
			self.assertTrue(hasattr(p, 'deauthenticate_session'))
			p.deauthenticate_session()
			self.assertTrue(hasattr(p, 'isAuthenticated'))
			p.isAuthenticated()

			p.authenticate_session.assert_called_once()
			p.deauthenticate_session.assert_called_once()
			p.isAuthenticated.assert_called_once()

	def test_exists_setQueryParams(self):
		with patch('easydb_urls.lib.SessionEAS.SessionEAS', autospec=True) as p:
			self.assertTrue(hasattr(p, 'setQueryParams'))
			p.setQueryParams(queryparams={})
		p.setQueryParams.assert_called_once_with(queryparams={})

	def test_exists_set_criteria(self):
		with patch('easydb_urls.lib.SessionEAS.SessionEAS', autospec=True) as p:
			self.assertTrue(hasattr(p, 'set_criteria'))
			p.set_criteria(local=False)
		p.set_criteria.assert_called_once_with(local=False)

	def test_exists_Result(self):
		with patch('easydb_urls.lib.SessionEAS.SessionEAS', autospec=True) as p:
			self.assertTrue(hasattr(p, 'getResult_JSON'))
			p.getResult_JSON()
			self.assertTrue(hasattr(p, 'getResultDict'))
			p.getResultDict()
			self.assertTrue(hasattr(p, 'getResultCount'))
			p.getResultCount()
			self.assertTrue(hasattr(p, 'getResultLimit'))
			p.getResultLimit()
			self.assertTrue(hasattr(p, 'getResultOffset'))
			p.getResultOffset()

			p.getResult_JSON.assert_called_once()
			p.getResultDict.assert_called_once()
			p.getResultCount.assert_called_once()
			p.getResultLimit.assert_called_once()
			p.getResultOffset.assert_called_once()

	def test_exists_printRequest(self):
		request = testing.DummyRequest()
		with patch('easydb_urls.lib.SessionEAS.SessionEAS', autospec=True) as p:
			self.assertTrue(hasattr(p, 'printRequest'))
			p.printRequest(req=request)
		p.printRequest.assert_called_once_with(req=request)

	def test_exists_getVal(self):
		with patch('easydb_urls.lib.SessionEAS.SessionEAS', autospec=True) as p:
			self.assertTrue(hasattr(p, 'getVal'))
			p.getVal(data={}, lookupkey='key')
		p.getVal.assert_called_once_with(data={}, lookupkey='key')

	def test_exists_write_json(self):
		with patch('easydb_urls.lib.SessionEAS.SessionEAS', autospec=True) as p:
			self.assertTrue(hasattr(p, 'write_json'))
			p.write_json(data={'Some data': 'json'}, name='file name')
		p.write_json.assert_called_once_with(data={'Some data': 'json'}, name='file name')

	def test_exists_write_file(self):
		with patch('easydb_urls.lib.SessionEAS.SessionEAS', autospec=True) as p:
			self.assertTrue(hasattr(p, 'write_file'))
			p.write_file(r='Some data', filename='file name')
		p.write_file.assert_called_once_with(r='Some data', filename='file name')

	def test_exists_server_url_error_message(self):
		with patch('easydb_urls.lib.SessionEAS.SessionEAS', autospec=True) as p:
			self.assertTrue(hasattr(p, 'server_url_error_message'))
			p.server_url_error_message(url='url', err='error')
		p.server_url_error_message.assert_called_once_with(url='url', err='error')

	def test_exists_server_url_Getter_and_Setter(self):
		with patch('easydb_urls.lib.SessionEAS.SessionEAS', autospec=True) as p:
			self.assertTrue(hasattr(p, '_setSession'))
			p._setSession(session=None)
			self.assertTrue(hasattr(p, '_getSession'))
			p._getSession()
			self.assertTrue(hasattr(p, '_setHeader'))
			p._setHeader(header=None)
			self.assertTrue(hasattr(p, '_getHeader'))
			p._getHeader()
			self.assertTrue(hasattr(p, '_setToken'))
			p._setToken(token=None)
			self.assertTrue(hasattr(p, '_getToken'))
			p._getToken()
			self.assertTrue(hasattr(p, '_setContent'))
			p._setContent(content=None)
			self.assertTrue(hasattr(p, '_getContent'))
			p._getContent()
			self.assertTrue(hasattr(p, '_setPassword'))
			p._setPassword(password=None)
			self.assertTrue(hasattr(p, '_getPassword'))
			p._getPassword()
			self.assertTrue(hasattr(p, '_setLogin'))
			p._setLogin(login=None)
			self.assertTrue(hasattr(p, '_getLogin'))
			p._getLogin()
			self.assertTrue(hasattr(p, '_setPlugins'))
			p._setPlugins(plugins=None)
			self.assertTrue(hasattr(p, '_getPlugins'))
			p._getPlugins()

			p._setSession.assert_called_once_with(session=None)
			p._getSession.assert_called_once()
			p._setHeader.assert_called_once_with(header=None)
			p._getHeader.assert_called_once()
			p._setToken.assert_called_once_with(token=None)
			p._getToken.assert_called_once()
			p._setContent.assert_called_once_with(content=None)
			p._getContent.assert_called_once()
			p._setPassword.assert_called_once_with(password=None)
			p._getPassword.assert_called_once()
			p._setLogin.assert_called_once_with(login=None)
			p._getLogin.assert_called_once()
			p._setPlugins.assert_called_once_with(plugins=None)
			p._getPlugins.assert_called_once()


if __name__ == '__main__':
	unittest.main()
