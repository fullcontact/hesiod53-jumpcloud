#!/usr/bin/env python

from setuptools import setup, find_packages

readme = open('README.md').read()

install_requires = [
    "pyyaml==3.11",
    "python-ldap"
]

setup(
    name='hesiod53-jumpcloud',
    version='0.1.0',
    description='Create configuration file for hesiod53 using jumpcloud directory',
    long_description=readme,
    author='FullContact',
    author_email='ops+hesiod53@fullcontact.com',
    url='https://github.com/fullcontact/hesiod53-jumpcloud',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'jumpcloud = jumpcloud.jumpcloud:main'
        ]
    },
)
