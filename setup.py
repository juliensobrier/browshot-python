# -*- coding: utf-8 -*-
import os

from setuptools import setup

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8') as file:
        return file.read()

requirements = ['requests']

setup(
    name='Browshot',
    version='1.32.0',
    py_modules=['browshot'],
    description='Client to interact with Browshot',
    long_description=read('README'),
    url='https://github.com/juliensobrier/browshot-python',
    license='Apache-2.0',
    author='Julien Sobrier',
    author_email='julien@sobrier.net',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],
    python_requires='>=3.9',
    install_requires=requirements,
)
