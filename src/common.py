# -*- coding: utf-8 -*-

import wx

import os, sys


debugging = ('WINGDB_ACTIVE' in os.environ)  # if True, at many places exceptions will be raised instead of handled

app_title = 'English-Myanmar Dictionary'

working_dir = os.path.dirname(os.path.realpath(__file__))
assets_path = os.path.join(working_dir, 'assets')   # Application data like file history and database

credits_file = 'CREDITS'                            # Path of the credits file "CREDITS.txt"
license_file = 'LICENSE'                            # Path of the license file "LICENSE.txt"
database_file = 'EMDictionary.db'                   # Database file name of distionary data
picture_zip_file = 'pics.zip'                       # Pictures zip file name
data_size = 50                                      # Size limit for data query

platform = 'not_set'                 # Current platform string (mostly wx.Platform)
version = 'not_set'                  # application version string; see: get_version()
py_version = sys.version.split()[0]  # Python version string
wx_version = 'not_set'               # wxPython version string

if len(wx.VERSION)==5:
    def SetToolTip(c, s):
        c.SetToolTipString(s)
else:
    def SetToolTip(c, s):
        c.SetToolTip(s)

def color_to_string(color):
    "returns the hexadecimal string representation of the given colour '#RRGGBB'"
    if color is None: return None
    return '#%.2x%.2x%.2x'%(color.Red(), color.Green(), color.Blue())

def read_version_file():
    """Read the version information from file "RELEASE-VERSION".
    see: write_version_file() and get_version()"""
    try:
        import version
        return version.__version__.strip()
    except ImportError:
        return None

def write_version_file(release):
    """Write the given version string into file "version.py".

    release: version string to write

    see: read_version_file(), get_version()"""
    fh = open('version.py', 'w')
    fh.write("""\
#
# This is an automatically generated file. Manual changes will be
# overwritten without warning.
#

__version__ = "%s"
""" % release)
    fh.close()

def get_version(suffix=True):
    """Return the release string.

    The release will determinate in three steps:
     1. read from release file (see read_version_file() )
     2. Set to "not found"

    The release string contains a suffix if wxGlade runs as standalone edition.

    suffix: Append suffix for standalone edition (bool)

    see: read_version_file()"""
    release = read_version_file()
    if not release:
        release = 'not found'

    if suffix and hasattr(sys, 'frozen'):
        release = '%s (standalone edition)' % release

    return release