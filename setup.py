from __future__ import print_function

import io
import os.path
import re
from distutils.text_file import TextFile

from setuptools import find_packages, setup

home = os.path.abspath(os.path.dirname(__file__))
missing = object()


def read_description(*files, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = [io.open(name, encoding=encoding).read() for name in files]
    return sep.join(buf)


def read_dependencies(requirements=missing):
    if requirements is None:
        return []
    if requirements is missing:
        requirements = 'requirements.txt'
    if not os.path.isfile(requirements):
        return []
    text = TextFile(requirements, lstrip_ws=True)
    try:
        return text.readlines()
    finally:
        text.close()


def read_version(module_name):
    with open(os.path.join(module_name, '__init__.py'), 'r') as fd:
        result = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                           fd.read(), re.MULTILINE)
        return result.group(1) if result else '0.0.1'


setup(
    name='flask_kits',
    version=read_version('flask_kits'),
    license='The MIT License',
    description='demo',
    author='recipe',
    author_email='ycs_ctbu_2010@126.com',
    install_requires=read_dependencies(),
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Software Distribution',
        'Topic :: System :: Systems Administration',
    ]
)
