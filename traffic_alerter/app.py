# -*- coding: utf-8 -*-
'''
Created on 07/03/2013

@author: streaming.analistas@corp.terra.com.br
'''
# pep8: disable-msg=E501
# pylint: disable=C0301

from traffic_alerter import __version__
from traffic_alerter.submodule import module


def main():
    print "hello world v" + __version__
    module.main()
