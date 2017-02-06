import os
from setuptools import find_packages, setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "really_good_products_api",
    version = "0.0.1",
    author = "Chris Lucas",
    author_email = "lucasc896@gmail.com",
    description = ("RESTful API for the best products ever."),
    long_description=read('README.md'),
    url="https://github.com/lucasc896/really_good_products_api",
    packages=find_packages(exclude=['tests', 'tests.*']),
    entry_points={
        "console_scripts": [
            "manage-db=goodproducts.db.manage:main",
        ]
    }
)