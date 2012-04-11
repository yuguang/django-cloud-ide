# -*- coding: utf-8 -*-
"""Setup file for easy installation"""
from setuptools import setup

setup(name='cloud_ide',
    version='1.0.0',
    author='Yuguang Zhang',
    author_email='zh.yuguang.cn@gmail.com',
    description='Django social authentication made simple.',
    license='GPL',
    keywords='django, openid, oauth, social auth, application',
    url='https://github.com/yuguang/cloud_ide',
    packages=['cloud_ide','cloud_ide.fiddle','cloud_ide.login','cloud_ide.shared','cloud_ide.snippet'],
    long_description='Cloud IDE provides storage, authentication, and generic templates for fiddles.',
    install_requires=['django>=1.2.5',],
    classifiers=['Framework :: Django',
                 'Development Status :: 4 - Beta',
                 'Topic :: Internet',
                 'License :: OSI Approved :: GPL License',
                 'Intended Audience :: Developers',
                 'Environment :: Web Environment',
                 'Programming Language :: Python :: 2.5',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7'])