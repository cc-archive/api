
import lxml
from StringIO import StringIO
import os

import cherrypy
import webtest # for the TestApi base class

##################
## Public names ##
##################
__all__ = (
           'RELAX_PATH',
           'relax_validate',
           'TestApi',
          )

####################
## Path constants ##
####################
RELAX_PATH = 'schemata'
if not os.path.exists(RELAX_PATH):
    RELAX_PATH = os.path.join('tests', 'schemata')

#######################
## Utility functions ##
#######################
def relax_validate(schema_filename, instance_buffer):
    """Validates xml string instance_buffer against RelaxNG schema 
    located in file schema_filename. By convention, schema_filename 
    is a constant defined in the test module. Schema files are 
    located in tests/schemata."""

    relaxng = lxml.etree.RelaxNG(lxml.etree.parse(schema_filename))
    instance = lxml.etree.parse(StringIO(instance_buffer))

    if not relaxng.validate(instance):
        print relaxng.error_log.last_error
        return False
    else:
        return True

############################
## Base classes for tests ##
############################

class TestApi:
    """Base class of test classes for the CC API. Defines test fixture
    behavior for creating and destroying webtest.TestApp instance of 
    the WSGI server."""

    def setUp(self):
        """Test fixture for nosetests: sets up the WSGI app server."""
        cherrypy.config.update({ 'global' : { 'log.screen' : False, } })
        cfgstr = 'config:%s' % (os.path.join(os.getcwd(), '..', 'server.cfg'))
        self.app = webtest.TestApp(cfgstr)

    def tearDown(self):
        """Test fixture for nosetests: tears down the WSGI app server."""
        cherrypy.engine.exit()
