#!/usr/bin/env python
from paste.servers.cgi_wsgi import run_with_cgi
from cherrypy._cpwsgi import wsgiApp

from rest_api import cherrypy as rest_api

rest_api.server.start(initOnly=True)

run_with_cgi(wsgiApp)
