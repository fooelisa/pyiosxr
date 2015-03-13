from setuptools import setup, find_packages
from pip.req import parse_requirements
import uuid

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt', session=uuid.uuid1())

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

version = '0.1'

setup(
    name='pyIOSXR',
    version=version,
    py_modules=['pyIOSXR'],
    packages=find_packages(),
    install_requires=reqs,
    include_package_data=True,
    description = 'Python API to interact with network devices running IOS-XR',
    author = 'Elisa Jasinska',
    author_email = 'elisa@netflix.com',
    url = 'https://github.com/fooelisa/pyiosxr/', # use the URL to the github repo
    download_url = 'https://github.com/fooelisa/pyiosxr/tarball/%s' % version,
    keywords = ['IOS-XR', 'IOSXR', 'Cisco', 'networking'],
    classifiers = [],
)
