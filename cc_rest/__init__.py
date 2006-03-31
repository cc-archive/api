"""
__init__.py
$Id$

Package initialization for CC REST API.

(c) 2004, Creative Commons, Nathan R. Yergler
Licensed under the GNU GPL 2 or later.
"""

import license
from license import classes
from license import details

import const

_q_exports = ['classes', 'details', 'license', 'version']
_q_index = classes 

def version(request):
    """Returns the CC Web Service version running on this instance."""
    return const.VERSION
    
