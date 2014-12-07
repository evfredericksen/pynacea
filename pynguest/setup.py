from setuptools import setup, find_packages
from codecs import open
from os import path
here = path.abspath(path.dirname(__file__))

setup(
	name='pynguest',
	version='0.0.14',
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
	packages=[],
	package_dir = {
		'pynguest': 'pynguest',
	},
	install_requires=[],
	scripts = ['scripts/pynacea.py'],
    data_files=[('Lib\site-packages', ['pynguest_config.ini'])],
	include_package_data = True,
	long_description = '''\
	'''
)
