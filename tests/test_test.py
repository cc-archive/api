# Copyright Frank Tobia, Creative Commons, whomever
# Released under MIT license whatever
# Standard boilerplate heading info

# TODO: a means of ensuring that these packages are installed as dependencies
import webtest
import cherrypy

import os
import sys

paths = []
paths.append(os.path.join(os.getcwd(), '..', 'src', 'cc', 'api'))
paths.append(os.path.join(os.getcwd(), '..', 'src', 'cc', 'licenses'))
print paths
for path in paths: # TODO: a better way
    sys.path.insert(0, path)

import rest_api # is my path configured correctly?
