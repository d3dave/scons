# MIT License
#
# Copyright The SCons Foundation
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
Helper functions for Microsoft Visual C/C++.
"""

import os
import re

from collections import (
    namedtuple,
)

def listdir_dirs(p):
    """
    Return a list of tuples for each subdirectory of the given directory path.
    Each tuple is comprised of the subdirectory name and the qualified subdirectory path.
    Assumes the given directory path exists and is a directory.

    Args:
        p: str
            directory path

    Returns:
        list[tuple[str,str]]: a list of tuples

    """
    dirs = []
    for dir_name in os.listdir(p):
        dir_path = os.path.join(p, dir_name)
        if os.path.isdir(dir_path):
            dirs.append((dir_name, dir_path))
    return dirs

def process_path(p):
    """
    Normalize a system path

    Args:
        p: str
            system path

    Returns:
        str: normalized system path

    """
    if p:
        p = os.path.normpath(p)
        p = os.path.realpath(p)
        p = os.path.normcase(p)
    return p

re_version_prefix = re.compile(r'^(?P<version>[0-9.]+).*$')

def get_version_prefix(version):
    """
    Get the version number prefix from a string.

    Args:
        version: str
            version specification

    Returns:
        str: the version number prefix

    """
    m = re_version_prefix.match(version)
    if m:
        rval = m.group('version')
    else:
        rval = ''
    return rval

re_msvc_version_prefix = re.compile(r'^(?P<version>[1-9][0-9]?[.][0-9]).*$')

def get_msvc_version_prefix(version):
    """
    Get the msvc version number prefix from a string.

    Args:
        version: str
            version specification

    Returns:
        str: the msvc version number prefix

    """
    m = re_msvc_version_prefix.match(version)
    if m:
        rval = m.group('version')
    else:
        rval = ''
    return rval

VERSION_ELEMENTS_DEFINITION = namedtuple('VersionElements', [
    'vc_version_numstr', # msvc version numeric string ('14.1')
    'vc_toolset_numstr', # toolset version numeric string ('14.16.27023')
    'vc_version_suffix', # component type ('Exp')
    'msvc_version',      # msvc version ('14.1Exp')
])

re_version_elements = re.compile(r'^(?P<version>(?P<msvc_version>[1-9][0-9]?[.][0-9])[0-9.]*)(?P<suffix>.*)$')

def get_version_elements(version):
    """
    Get the version elements from an msvc version or toolset version.

    Args:
        version: str
            version specification

    Returns:
        None or VersionElements namedtuple:
    """

    m = re_version_elements.match(version)
    if not m:
        return None

    vc_version_numstr = m.group('msvc_version')
    vc_toolset_numstr = m.group('version')
    vc_version_suffix = m.group('suffix')

    version_elements_def = VERSION_ELEMENTS_DEFINITION(
        vc_version_numstr = vc_version_numstr,
        vc_toolset_numstr = vc_toolset_numstr,
        vc_version_suffix = vc_version_suffix,
        msvc_version = vc_version_numstr + vc_version_suffix,
    )

    return version_elements_def

