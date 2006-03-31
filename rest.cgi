#!/usr/local/python233/bin/python

"""
rest.cgi
$Id$

Creative Commons REST API Quixote CGI driver script.

(c) 2004, Nathan R. Yergler, Creative Commons
Licensed under the GNU GPL 2 or later.
"""

import quixote

# enable page templates
quixote.enable_ptl()

# create the publisher and dispatch the request
rest = quixote.Publisher("cc_rest")
rest.setup_logs()
rest.publish_cgi()
