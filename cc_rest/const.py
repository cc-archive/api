"""
$Id$

Constants and filenames for CC REST API implementation.

(c) 2004, Creative Commons, Nathan R. Yergler
Licensed under the GNU GPL 2 or later.
"""

import os

XML_SOURCE = "questions.xml"
XSLT_SOURCE = 'chooselicense.xsl'

# make absolute paths to the filenames
CC_REST_PATH = os.path.dirname(os.path.abspath(__file__))
XML_SOURCE = os.path.join(CC_REST_PATH, XML_SOURCE)
XSLT_SOURCE = os.path.join(CC_REST_PATH, XSLT_SOURCE)

VERSION="1.0.5"
