from setuptools import setup, find_packages
import sys
import os

# check for python version and define the right requirements
if sys.version_info < (3, 0):
	raise Exception ('python version must be >= 3.0')
else:
	pass

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
	README = f.read()

requires = [
	'configparser>=5.2.0',
	'coverage>=6.2',
	'mock>=4.0.3',
	'pyramid==2.0',
	'pyramid_beaker==0.8',
	'pyramid_chameleon==0.3',
	'pytest>=5.4.2',
	'pytest-cov>=3.0',
	'requests_cache==0.9.1',
	'requests>=2.27.1',
	'setuptools>=57.0.0',
	'waitress>=2.0',
]

tests_require = [
	'coverage',
	'pytest>=5.4.2',
	'pytest-cov',
]

setup(name='easydb_urls',
	author='Börn Quast',
	author_email='bquast@zfmk.de',
	license='CC-By 4.0',
	version='1.0.1',
	url='https://gitlab.leibniz-lib.de/easydb/easydb_urls.git',
	extras_require={
		'testing': tests_require,
	},
	packages=find_packages(exclude=['tests']),
	include_package_data=True,
	zip_safe=False,
	tests_require=tests_require,
	test_suite="tests",
	install_requires=requires,
	entry_points="""\
	[paste.app_factory]
	main = easydb_urls:main
	""",
)
