import os
from setuptools import setup

# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "bigcommerce",
    version = "0.9.0",
    author = "Bigcommerce Engineering",
    author_email = "vip@bigcommerce.com",
    description = ("Connect Python applications with the Bigcommerce API"),
    license = "MIT",
    keywords = "example documentation tutorial",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=['an_example_pypi_project', 'tests'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
    ],
)