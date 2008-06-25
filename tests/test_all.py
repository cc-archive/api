
import cherrypy # this will go away eventually
import os
import webtest
import operator

from tests.test_common import RELAX_PATH, relax_validate

####################
## Path constants ##
####################
RELAX_LOCALES = os.path.join(RELAX_PATH, 'locales.relax.xml')
RELAX_ERROR = os.path.join(RELAX_PATH, 'error.relax.xml')
RELAX_CLASSES = os.path.join(RELAX_PATH, 'classes.relax.xml')
RELAX_LICENSECLASS = os.path.join(RELAX_PATH, 'licenseclass.relax.xml')
RELAX_ISSUE = os.path.join(RELAX_PATH, 'issue.relax.xml')
RELAX_ERROR = os.path.join(RELAX_PATH, 'error.relax.xml')

##################
## Test fixture ##
##################
def setup():
    """Test fixture for nosetests: sets up the WSGI app server."""
    global app
    cherrypy.config.update({ 'global' : { 'log.screen' : False, } })
    cfgstr = 'config:%s' % (os.path.join(os.getcwd(), '..', 'server.cfg'))
    app = webtest.TestApp(cfgstr)

def teardown():
    """Test fixture for nosetests: tears down the WSGI app server."""
    cherrypy.engine.exit()

#######################
## Utility functions ##
#######################
def _permute(lists): #TODO: document this function
    if lists:
        result = map(lambda i: (i,), lists[0])
        for list in lists[1:]:
            curr = []
            for item in list:
                new = map(operator.add, result, [(item,)]*len(result))
                curr[len(curr):] = new
            result = curr
    else:
        result = []
    return result

def _get_license_classes():
    return ['standard', 'publicdomain', 'recombo']

def _field_enums(lclass):
    """Retrieve the license information for this class, and generate a set of answers for use with testing."""
    return [
            ('commercial', ['y', 'n']),
            ('derivatives', ['y', 'sa', 'n']),
            ('jurisdiction', ['', 'us', 'de', 'uk'])
           ]

def _get_locales():
    """Return a list of supported locales."""
    locales = [
                'en', # English
                'de', # German
                # 'he', # Hebrew TODO: fix html <span dir="rtl"> formatting
                'el', # Greek
              ]
    return locales

def _test_answers_xml(lclass): # TODO: document what this function does
    all_answers = _field_enums(lclass)
    all_locales = _get_locales()
    for ans_combo in _permute([n[1] for n in all_answers]):
        for locale in all_locales:
            answers_xml = lxml.etree.Element('answers')
            locale_node = lxml.etree.SubElement(answers_xml, 'locale')
            locale_node.text = locale
            class_node = lxml.etree.SubElement(answers_xml, 'license-%s' % lclass)
            for a in zip([n[0] for n in all_answers], ans_combo):
                a_node = lxml.etree.SubElement(class_node, a[0])
                a_node.text = a[1]
            yield lxml.etree.tostring(answers_xml)

def _test_answer_query_strings(lclass): # TODO: document what this function does
    all_answers = _field_enums(lclass)
    all_locales = _get_locales()
    for ans_combo in _permute([n[1] for n in all_answers]):
        for locale in all_locales:
            params = zip([n[0] for n in all_answers], ans_combo)
            param_strs = ['='.join(n) for n in params]
            # append to each locale in turn
            param_strs.append('locale=%s' % locale)
            # generate the query string
            result = '?' + '&'.join(param_strs)
            # yield each
            yield result

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

def test_license_class_structure():
    """Test that each license class returns a valid XML chunk."""
    for lclass in _get_license_classes():
        res = app.get('/license/%s' % lclass)
        assert relax_validate(RELAX_LICENSECLASS, res.body)
'''
def test_issue():
    """Test that every license class will be successfully issued via the /issue method."""
    for lclass in _get_license_classes():
        for answers in _test_answers_xml(lclass):
            res = app.get('/license/%s/issue?answers=%s' %
                          (lclass, answers))
            print "lclass: %s ; answers: %s" % (lclass, answers)
            assert relax_validate(RELAX_ISSUE, res.body)

def test_get():
    """Test that every license class will be successfully issued via the /get method."""
    for lclass in _get_license_classes():
        for query_string in _test_answer_query_strings(lclass):
            res = app.get('/license/%s/get%s' % (lclass, query_string))
            assert relax_validate(RELAX_ISSUE, res.body)

def test_get_extra_args():
    """Test the /get method with extra nonsense arguments; extra arguments should be ignored."""
    for lclass in _get_license_classes():
        for query_string in _test_answer_query_strings(lclass):
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

def test_details_error():
    """A call to /details with no liecense-uri should return a missingparam error."""
    res = app.get('/details')
    assert relax_validate(RELAX_ERROR, res.body)

def test_license_details():
    """Test that the license details call responds appropriately."""
    for uri in ('http://creativecommons.org/licenses/by-nc-nd/2.5/',
                'http://creativecommons.org/licenses/by-nc-sa/2.5/',
                'http://creativecommons.org/licenses/by-sa/2.5/',
                'http://creativecommons.org/licenses/by/2.0/nl/',
               ):
        res = app.get('/details?license-uri=%s' % uri)
        assert relax_validate(RELAX_ISSUE, res.body)

def test_invalid_license_details():
    """Test that an invalid URI raises an error."""
    uri = "http://creativecommons.org/licenses/blarf"
    res = app.get('/details?license-uri=%s' % uri)
    assert relax_validate(RELAX_ERROR, res.body)

if __name__ == '__main__':
    pass
