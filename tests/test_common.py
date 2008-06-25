
from unittest import TestCase
import lxml
from StringIO import StringIO
import os

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

class TestApi(TestCase):

    def __init__(self, *args, **kwargs):
        # each class can have its own local copy
        # TODO: see if things explode if it's module-level
        TestCase.__init__(self, *args, **kwargs)
        self.cherrypy = __import__('cherrypy')
        self.webtest = __import__('webtest')


    def setUp(self):
        """Test fixture for nosetests: sets up the WSGI app server."""
        self.cherrypy.config.update({ 'global' : { 'log.screen' : False, } })
        cfgstr = 'config:%s' % (os.path.join(os.getcwd(), '..', 'server.cfg'))
        self.app = self.webtest.TestApp(cfgstr)

    def tearDown(self):
        """Test fixture for nosetests: tears down the WSGI app server."""
        self.cherrypy.engine.exit()
