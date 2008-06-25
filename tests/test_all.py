
import cherrypy # this will go away eventually
import os
import webtest
import operator

from tests.test_common import *

####################
## Path constants ##
####################
RELAX_ERROR = os.path.join(RELAX_PATH, 'error.relax.xml')
RELAX_LICENSECLASS = os.path.join(RELAX_PATH, 'licenseclass.relax.xml')
RELAX_ISSUE = os.path.join(RELAX_PATH, 'issue.relax.xml')

##################
## Test fixture ##
##################
def setup():
    """Test fixture for nosetests: sets up the WSGI app server."""
    global app
    cherrypy.config.update({ 'global' : { 'log.screen' : False, } })
    cfgstr = 'config:%s' % (os.path.join(os.getcwd(), '..', 'server.cfg'))
    app = webtest.TestApp(cfgstr)
    global data
    data = TestData()

def teardown():
    """Test fixture for nosetests: tears down the WSGI app server."""
    cherrypy.engine.exit()

###########
## Tests ##
###########
def test_license_class_structure():
    """Test that each license class returns a valid XML chunk."""
    for lclass in data.license_classes():
        res = app.get('/license/%s' % lclass)
        assert relax_validate(RELAX_LICENSECLASS, res.body)
'''
def test_issue():
    """Test that every license class will be successfully issued via the /issue method."""
    for lclass in data.license_classes():
        for answers in data.xml_answers(lclass):
            res = app.get('/license/%s/issue?answers=%s' %
                          (lclass, answers))
            print "lclass: %s ; answers: %s" % (lclass, answers)
            assert relax_validate(RELAX_ISSUE, res.body)

def test_get():
    """Test that every license class will be successfully issued via the /get method."""
    for lclass in data.license_classes():
        for query_string in data.query_string_answers(lclass):
            res = app.get('/license/%s/get%s' % (lclass, query_string))
            assert relax_validate(RELAX_ISSUE, res.body)

def test_get_extra_args():
    """Test the /get method with extra nonsense arguments; extra arguments should be ignored."""
    for lclass in data.license_classes():
        for query_string in data.query_string_answers(lclass):
            res = app.get('/license/%s/get%s&foo=bar' % (lclass, query_string))
            assert relax_validate(RELAX_ISSUE, res.body)

def test_issue_error():
    """Issue with no answers or empty answers should return an error."""
    res = app.get('/license/blarf/issue?answers=<foo/>')
    assert relax_validate(RELAX_ERROR, res.body)
'''
def test_issue_invalid_class():
    """/issue should return an error with an invalid class."""
    res = app.get('/license/blarf/issue?answers=<foo/>')
    assert relax_validate(RELAX_ERROR, res.body)

def test_get_invalid_class():
    """/get should return an error with an invalid class."""
    res = app.get('/license/%s/get' % hash(app))
    assert relax_validate(RELAX_ERROR, res.body)

if __name__ == '__main__':
    pass
