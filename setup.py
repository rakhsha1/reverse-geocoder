# setup.py
import os
from distutils.core import setup, Extension

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(name='pg_reverse_geocoder',
	version='1.0',
      author='Ali Rakhshanfar',
      author_email='ali@personagraph.com',
      url='https://github.com/rakhsha1/reverse-geocoder',
      packages=['reverse_geocoder'],
      package_dir={'reverse_geocoder': './reverse_geocoder'},
      package_data={'reverse_geocoder': ['all_countries_with_postal_code.csv']},
      requires=['numpy', 'scipy'],
      description='Fast, offline reverse geocoder.',
)