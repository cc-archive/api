
import os

from tests.test_common import *

###########
## Tests ##
###########

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

if __name__ == '__main__':
    pass
