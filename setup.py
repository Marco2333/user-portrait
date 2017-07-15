#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

#!/usr/bin/env python
from setuptools import setup

setup(
    name='TwitterProject',
    version='1.0.0.dev1',
    description='A twitter users analytics python project',
    url='https://github.com/duncanzhou/Twitter-Project',
    author='DuncanZhou',
    author_email='zhouyimingww@163.com',
    license='Soochow University',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='twitter python',
    packages=['nltk','MySQLdb','pymongo','neo4j.v1'],
)
