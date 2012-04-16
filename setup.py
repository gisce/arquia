#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup file for arquia client.
"""

from distutils.core import setup

PACKAGES = ['arquiapgw', ]
PACKAGES_DATA = {}

setup(name='arquiapgw',
      description = """A client to submit payment orders to the Arquia
      service.""",
      author='GISCE Enginyeria',
      author_email='devel@gisce.net',
      url='http://www.gisce.net',
      version='0.2.3',
      license='General Public Licence 2',
      long_description='''Long description''',
      provides=['arquiapgw'],
      install_requires=['PyDES'],
      packages=PACKAGES,
      package_data=PACKAGES_DATA,
      scripts=[],
)
