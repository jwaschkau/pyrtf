classifiers = """\
Development Status :: 4 - Beta
Topic :: Text Editors :: Text Processing
Topic :: Software Development :: Libraries :: Python Modules
Intended Audience :: Developers
Programming Language :: Python
License :: OSI Approved :: GNU General Public License (GPL)
"""

import sys
import os
import versioneer

from setuptools import setup, find_packages
from distutils.core import setup

doclines = open('README').readlines()

setup(
    name='PyRTF3',
    author='Mars Galactic',
    author_email='xoviat@noreply.users.github.com',
    url='https://github.com/xoviat/pyrtf',
    license='http://www.gnu.org/licenses/gpl.html',
    platforms=['Any'],
    install_requires=['PyParsing'],
    description=doclines[0],
    classifiers=[_f for _f in classifiers.split('\n') if _f],
    long_description='\n'.join(doclines[2:]),
    keywords=('RTF', 'Rich Text', 'Rich Text Format', 'documentation',
              'reports'),
    packages=find_packages(),
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass())
