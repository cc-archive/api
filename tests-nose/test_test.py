
import cherrypy # this will go away eventually
import os
import webtest
from StringIO import StringIO # TODO: decide if this is necessary
import lxml

####################
## Path constants ##
####################
RELAX_PATH = os.path.join(os.pardir, 'relax')
RELAX_LOCALES = os.path.join(RELAX_PATH, 'locales.relax.xml')
# more to come, when I clean them up

##################
## Test fixture ##
##################
def setup():
    """Test fixture for nosetests: sets up the WSGI app server
    """
    global app
    cfgstr = 'config:%s' % (os.path.join(os.getcwd(), '..', 'server.cfg'))
    app = webtest.TestApp(cfgstr)

###############################
## Testing utility functions ##
###############################
def relax_validate(schema_filename, instance_buffer):
    relaxng = lxml.etree.RelaxNG(lxml.etree.parse(schema_filename))
    instance = lxml.etree.parse(StringIO(instance_buffer))

    if not relaxng.validate(instance):
        print relaxng.error_log.last_error
        return False
    else:
        return True

###########
## Tests ##
###########
def test_locales():
    """Test that /locales returns a list of supported languages."""
    res = app.get('/locales')
    assert relax_validate(RELAX_LOCALES, res.body)

def test_locales_extra_args():
    """Test the /locales method with extra non-sense arguments;
    extra arguments should be ignored."""
    res = app.get('/locales?foo=bar')
    assert relax_validate(RELAX_LOCALES, res.body)
    res = app.get('/locales?lang=en_US&blarf=%s' % hash(res))
    assert relax_validate(RELAX_LOCALES, res.body)

if __name__ == '__main__':
    pass
