
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
RELAX_ERROR = os.path.join(RELAX_PATH, 'error.relax.xml')
RELAX_CLASSES = os.path.join(RELAX_PATH, 'classes.relax.xml')
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

def test_classes():
    """Test that /classes and / are synonyms."""
    root = app.get('/').body
    classes = app.get('/').body
    assert root == classes

def test_invalid_class():
    """An invalid license class name should return an explicit error."""
    res = app.get('/license/noclass')
    assert relax_validate(RELAX_ERROR, res.body)

def test_classes_structure():
    """Test the return values of /classes to ensure it fits with our
    claims."""
    res = app.get('/classes')
    assert relax_validate(RELAX_CLASSES, res.body)

if __name__ == '__main__':
    pass
