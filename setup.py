import os
from setuptools import setup, find_packages

# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

VERSION = '0.17.1'

setup(
    name = 'bigcommerce',
    version = VERSION,

    packages = find_packages(),
    install_requires = ['requests>=2.1.0', 'streql>=3.0.2', 'pyjwt>=1.4.0'],
    
    
    url = 'https://github.com/bigcommerce/bigcommerce-api-python',
    download_url = 'https://pypi.python.org/packages/source/b/bigcommerce/bigcommerce-{}.tar.gz'.format(VERSION),

    author = 'Bigcommerce Engineering',
    author_email = 'api@bigcommerce.com',

    description = 'Connect Python applications with the Bigcommerce API',
    long_description = read('README.rst'),
    license = 'MIT',

    keywords = ['bigcommerce', 'api', 'v2', 'client'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Office/Business',
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4'
    ],
)
