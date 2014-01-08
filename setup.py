import os
from setuptools import setup, find_packages

# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "bigcommerce-api",
    version = "0.9.3",
    
    packages=find_packages(),
    package_data = {'' : ['LICENSE', 'README.md']},
    install_requires = ['requests>=2.1.0',
                        'streql>=3.0.2'],
    author = "Bigcommerce Engineering",
    author_email = "vip@bigcommerce.com",
    description = "Connect Python applications with the Bigcommerce API",
    license = "MIT",
    keywords = "bigcommerce api client",
    url = "https://github.com/bc-jackiehuynh/bigcommerce-api-python/tree/alpha",
    
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
    ],
)