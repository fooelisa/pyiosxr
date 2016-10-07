#!/usr/bin/env python
# coding=utf-8
"""A module to interact with Cisco devices running IOS-XR."""

# Copyright 2015 Netflix. All rights reserved.
# Copyright 2016 BigWaveIT. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

from setuptools import setup, find_packages
from pip.req import parse_requirements
import uuid

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt', session=uuid.uuid1())

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

version = '0.25'

setup(
    name='pyIOSXR',
    version=version,
    py_modules=['pyIOSXR'],
    packages=find_packages(),
    install_requires=reqs,
    include_package_data=True,
    description='Python API to interact with network devices running IOS-XR',
    author='Elisa Jasinska, Mircea Ulinic',
    author_email='elisa@bigwaveit.org, mircea@cloudflare.com',
    url='https://github.com/fooelisa/pyiosxr/',
    download_url='https://github.com/fooelisa/pyiosxr/tarball/%s' % version,
    keywords=['IOS-XR', 'IOSXR', 'Cisco', 'networking'],
    classifiers=[],
)
