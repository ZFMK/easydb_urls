from pyramid.view import view_config
from configparser import ConfigParser

from .lib.AssetGetter import AssetGetter
from .lib.ParamsReader import ParamsReader
from .lib.SessionEAS import SessionEAS

config = ConfigParser()
config.read('./easydb_urls/config.ini')

class AssetViews(object):
	"""Get the data for an asset identified by the objectid as in https://media.leibniz-lib.de/detail/{id}
	"""
	def __init__(self, request):
		self.request = request
		self.baseurl = config.get('easydb_api', 'baseurl')
		self.sessionobj = SessionEAS(self.request)
		self.paramsreader = ParamsReader(self.request)
		self.queryparams = self.paramsreader.getParams()
		self.preferredsize = self.queryparams['preferredsize']

	@view_config(route_name='showAsset', renderer="json")
	@view_config(route_name='showAssetJSON', renderer="json")
	def assetByIDJSON(self):
		"""Get the json data for a given id
		"""
		assetid = self.request.matchdict['id']

		assetgetter = AssetGetter(self.sessionobj, self.request, assetid)
		assetgetter.runQuery()
		jsonobj = assetgetter.getJSON()

		return jsonobj
