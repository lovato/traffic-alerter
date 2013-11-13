# -*- coding: utf-8 -*-
"""
    Setup package
    ~~~~~~~~~~~~~~~~~~~~

    Setuptools/distutils commands to package installation.

    :author: Marco Lovato/Eng. Streaming
    :contact: streaming.analistas@corp.terra.com.br
    :copyright: Copyright 2007-2013 by the Sphinx team, see AUTHORS.
    :license: Other/Proprietary, see LICENSE for details.
"""
# pylint: HOOK-IGNORED

import os
from setuptools import Command, setup, find_packages
import httplib
import base64
import string
import re
from distutils.version import StrictVersion
from subprocess import Popen, PIPE, STDOUT, call
import subprocess

# Hack to silence atexit traceback in newer python versions
try:
    import multiprocessing
except ImportError:
    pass

project_name = 'traffic_alerter'
__version__ = __import__(project_name).__version__
__author__ = __import__(project_name).__author__
__description__ = __import__(project_name).__description__

if os.getenv('BUILD_NUMBER') is not None:
    __version__ = __version__ + '.' + os.getenv('BUILD_NUMBER')


class deploy(Command):

    """Audits source code using PyFlakes for following issues:
        - Names which are used but not defined or used before they are defined.
        - Names which are redefined without having been used.
    """
    description = "Audit source code with PyFlakes"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if _is_already_installed():
            print "ERROR: Version is lower or equal"
            exit(1)
        else:
            response = cmd_output(
                "python setup.py sdist upload -r prod".split())
            response = response.split('\n')
            print response[-2]
            exit(0)


class is_already_installed(Command):

    """Audits source code using PyFlakes for following issues:
        - Names which are used but not defined or used before they are defined.
        - Names which are redefined without having been used.
    """
    description = "Audit source code with PyFlakes"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if _is_already_installed():
            print "Version is lower or equal"
            exit(1)
        else:
            print "Version is higher"
            exit(0)


def _is_already_installed():
    host = "pypi.tpn.terra.com"
    url = "/simple/" + project_name + "/"
    username = 'marco.lovato'
    password = 'marco.lovato'

    # base64 encode the username and password
    auth = base64.encodestring(
        '%s:%s' % (username, password)).replace('\n', '')

    webservice = httplib.HTTP(host)
    # write your headers
    webservice.putrequest("GET", url)
    webservice.putheader("Host", host)
    webservice.putheader("User-Agent", "Python http auth")
    webservice.putheader("Content-type", "text/html; charset=\"UTF-8\"")
    # write the Authorization header like: 'Basic base64encode(username + ':'
    # + password)
    webservice.putheader("Authorization", "Basic %s" % auth)

    webservice.endheaders()
    # get the response
    statuscode, statusmessage, header = webservice.getreply()
    response = webservice.getfile().readlines()
    version_list = []
    for line in response:
        if 'tar' in line:
            line = re.sub(r"<.*-([\d\.]+)tar.gz</a>", r"\1", line)[:-2]
            version_list.append(line)
    version_list.sort(key=lambda s: map(int, s.split('.')))
    if version_tuple(__version__) > version_tuple(version_list[-1]):
        return False
    else:
        return True


def cmd_output(args, **kwds):
    kwds.setdefault("stdout", subprocess.PIPE)
    kwds.setdefault("stderr", subprocess.STDOUT)
    p = subprocess.Popen(args, **kwds)
    return p.communicate()[0]


def get_requirements(file_name='requirements.txt'):
    lines = []
    try:
        filename = open(file_name)
        lines = [i.strip() for i in filename.readlines()]
        filename.close()
    except:
        pass
    return lines


def version_tuple(version):
    return tuple([int(num) for num in version.split('.')])


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except:
        pass
    return ''


CLASSIFIERS = [
    'Environment :: Library',
    'Intended Audience :: Developers',
    'Programming Language :: Python',
    'Operating System :: OS Independent',
    'Topic :: Internet :: WWW/HTTP',
]

setup(
    author=__author__,
    author_email='streaming.analistas@corp.terra.com.br',
    classifiers=CLASSIFIERS,
    description=__description__,
    entry_points={
        'console_scripts': [
            project_name + '_app = ' + project_name + '.app:main'
        ]
    },
    include_package_data=True,
    install_requires=get_requirements(),
    license=read('LICENSE'),
    long_description=read('README.rst'),
    name=project_name,
    packages=find_packages(),
    platforms=['any'],
    scripts=[],
    test_suite='nose.collector',
    tests_require=get_requirements('requirements-dev.txt'),
    url='http://pypi.tpn.terra.com/packages/' + project_name,
    version=__version__,
    cmdclass={
        'is_already_installed': is_already_installed,
        'deploy': deploy
    },
    zip_safe=True
)
