# package


from pyramid.config import Configurator


def main(global_config, **settings):
	config = Configurator(settings=settings)
	config.include('pyramid_chameleon')
	
	config.include('pyramid_beaker')

	config.add_route('help', '/')
	config.add_route('loginView', '/login')
	config.add_route('sessionLogin', '/sessionlogin')
	config.add_route('sessionLogout', '/sessionlogout')

	config.add_route('listAssets', '/assets')
	config.add_route('listAssetsJSON', '/json/assets')
	config.add_route('listAssetsCSV', '/csv/assets')
	config.add_route('searchPage', '/easyPage')
	config.add_route('searchPageJSON', '/json/easyObject')
	config.add_route('searchForm', '/search')
	config.add_route('searchDispatcher', '/searchDispatcher')

	config.add_route('getCollection', '/getCollection*collection_id')
	config.add_route('getCollectionJSON', '/json/getCollection*collection_id')
	config.add_route('getChildCollections', '/getChildCollections*parent_collection_id')
	config.add_route('getChildCollectionsJSON', '/json/getChildCollections*parent_collection_id')

	config.add_route('getFile', '/res/{filename}')

	config.add_route('resolveAsset', '/asset/{assettype}/{assetid}/{size}/{filename}')
	config.add_route('resolveImage', '/image/{assetid}/full/{size}/0/{filename}')
	config.add_route('resolveImageByID', '/image/{assetid}')
	
	config.add_route('showAsset', '/asset/{id}')
	config.add_route('showAssetJSON', '/json/asset/{id}')
	
	config.add_route('collectAssets', '/collectAssets')

	config.add_route('favicon', '/favicon.ico')
	config.add_static_view(name='static', path='easydb_urls:static')
	# ordering of the routes is important here
	
	config.scan()
	return config.make_wsgi_app()
