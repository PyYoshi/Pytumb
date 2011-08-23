#!/usr/bin/env python
#from distutils.core import setup
from setuptools import setup, find_packages
import Pytumb

setup(name="Pytumb",
      version=Pytumb.__vesion__,
      description="Tumblr library for python",
      license=Pytumb.__license__,
      author=Pytumb.__author__,
      url=Pytumb.__url__,
      packages = find_packages(),
      keywords= "tumblr library",
      zip_safe = True,
      install_require=[
      'httplib2'
      ]
      )