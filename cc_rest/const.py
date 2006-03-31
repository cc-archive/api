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
# *** we assume the layout is the same as a CVS checkout --
# *** that is, the XSL and XML files are in the parent directory
# *** of the cc_rest package (same directory as rest.cgi)

CC_REST_PATH = os.path.dirname(os.path.abspath(__file__))
XML_SOURCE = os.path.join(CC_REST_PATH, '..', XML_SOURCE)
XSLT_SOURCE = os.path.join(CC_REST_PATH, '..', XSLT_SOURCE)

VERSION="1.1.0"
