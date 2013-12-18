import os
from setuptools import setup

# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "Bigcommerce API Python Client",
    version = "0.9.0",
    
    packages=['bigcommerce'],
    package_data = {'' : ['LICENSE', 'README.md']},
    install_requires = ['requests>=2.0.1',
                        'simplejson>=3.3.1'],
    author = "Bigcommerce Engineering",
    author_email = "vip@bigcommerce.com",
    description = ("Connect Python applications with the Bigcommerce API"),
    license = "MIT",
    keywords = "bigcommerce api client",
    url = "https://github.com/maetl/bigcommerce-api-python/",
    
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
    ],
)