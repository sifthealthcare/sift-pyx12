######################################################################
# Copyright (c) 2001-2019
#   John Holland <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

"""
Interface to normalized Data Elements
"""

import os.path
import logging
import xml.etree.cElementTree as et
from pkg_resources import resource_stream

# Intrapackage imports
from sift_pyx12.errors import EngineError


class DataElementsError(Exception):
    """Class for data elements module errors."""


class DataElements(object):
    """
    Interface to normalized Data Elements
    """

    def __init__(self, base_path=None):
        """
        Initialize the list of data elements
        @param base_path: Override directory containing dataele.xml.  If None,
            uses package resource folder
        @type base_path: string

        @note: self.dataele - map to the data element
        {ele_num: {data_type, min_len, max_len, name}}
        """
        logger = logging.getLogger('sift_pyx12')
        self.dataele = {}
        dataele_file = 'dataele.xml'
        if base_path is not None:
            logger.debug("Looking for data element definition file '{}' in map_path '{}'".format(dataele_file, base_path))
            fd = open(os.path.join(base_path, dataele_file))
        else:
            logger.debug("Looking for data element definition file '{}' in pkg_resources".format(dataele_file))
            fd = resource_stream(__name__, os.path.join('map', dataele_file))
        parser = et.XMLParser(encoding="utf-8")
        for eElem in et.parse(fd, parser=parser).iter('data_ele'):
            ele_num = eElem.get('ele_num')
            data_type = eElem.get('data_type')
            min_len = int(eElem.get('min_len'))
            max_len = int(eElem.get('max_len'))
            name = eElem.get('name')
            self.dataele[ele_num] = {'data_type': data_type, 'min_len':
                                     min_len, 'max_len': max_len, 'name': name}
        fd.close()

    def get_by_elem_num(self, ele_num):
        """
        Get the element characteristics for the indexed element code
        @param ele_num: the data element code
        @type ele_num: string
        @return: {data_type, min_len, max_len, name}
        @rtype: dict
        """
        if not ele_num:
            raise EngineError('Bad data element %s' % (ele_num))
        if ele_num not in self.dataele:
            raise EngineError('Data Element "%s" is not defined' % (ele_num))
        return self.dataele[ele_num]

    def __repr__(self):
        print([v for k,v in self.dataele.items()])

    def debug_print(self):
        """
        Debug print data elements
        """
        self.__repr__()
