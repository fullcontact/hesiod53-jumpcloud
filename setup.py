#!/usr/bin/env python

from setuptools import setup, find_packages

readme = open('README.rst').read()

install_requires = [
    "pyyaml==3.11",
    "python-ldap"
]

setup(
    name='hesiod53-jumpcloud',
    version='0.1.1',
    description='Create configuration file for hesiod53 using jumpcloud directory',
    long_description=readme,
    author='FullContact',
    author_email='ops+hesiod53@fullcontact.com',
    url='https://github.com/fullcontact/hesiod53-jumpcloud',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
        'Topic :: System :: Systems Administration :: Authentication/Directory :: LDAP',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='ssh jumpcloud',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'jumpcloud = jumpcloud.jumpcloud:main'
        ]
    },
)
