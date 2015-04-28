from setuptools import setup, find_packages
from codecs import open
import os
here = os.path.abspath(os.path.dirname(__file__))
import sys

def get_windows_df_path():
	p = os.getenv('APPDATA')
	if p is None:
		p = os.path.join('c\\', 'pynacea')
	return p

df = {
	'linux': os.path.join(os.sep, 'usr', 'local', 'etc', 'pynacea'),
	'win32': get_windows_df_path(),
}

def get_data_files_dir():
	return df[sys.platform]

setup(
	name='pynhost',
	version='0.5.0',
	description='Linux Voice Recognition System',
	url='https://github.com/evfredericksen/pynacea',
	author='Evan Fredericksen',
	author_email='evfredericksen@gmail.com',
	license='MIT',
	classifiers=[
	'Development Status :: 3 - Alpha',
	'Intended Audience :: Developers',
	'Topic :: Software Development :: Build Tools',
	'License :: OSI Approved :: MIT License',
	'Programming Language :: Python :: 3',
	'Programming Language :: Python :: 3.2',
	'Programming Language :: Python :: 3.3',
	'Programming Language :: Python :: 3.4',
	],
	keywords='voice recognition grammar',
	packages=['pynhost'],
	package_dir = {
		'pynhost': 'pynhost',
	},
	install_requires=[],
	data_files=[(df[sys.platform], ['pynhost.ini'])],
	scripts = ['scripts/pynacea.py'],
	include_package_data = True,
	long_description = '''\
	'''
)