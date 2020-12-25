#!/usr/bin/env python
# coding:utf-8
"""
# @Time     : 2020-08-12 17:49
# @Author   : Zhangyu
# @Email    : zhangycqupt@163.com
# @File     : setup1.py
# @Software : PyCharm
# @Desc     :
"""

from setuptools import setup, find_packages

setup(
    name='cfnlp',
    version='0.1',
    description=(
        'org nlp python lib'
    ),
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    author='zhangyu',
    author_email='976894176@qq.com',
    license='MIT',
    maintainer='cc&zhangyu&tanrui',
    maintainer_email='976894176@qq.com',
    packages=find_packages(),
    platforms=['all'],
    url='XX',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ], install_requires=['flask']

)
