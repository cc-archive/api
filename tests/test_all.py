
import cherrypy # this will go away eventually
import os
import webtest
from StringIO import StringIO # TODO: decide if this is necessary
import lxml
import operator

####################
## Path constants ##
####################
RELAX_PATH = os.path.join(os.pardir, 'relax')
RELAX_LOCALES = os.path.join(RELAX_PATH, 'locales.relax.xml')
RELAX_ERROR = os.path.join(RELAX_PATH, 'error.relax.xml')
RELAX_CLASSES = os.path.join(RELAX_PATH, 'classes.relax.xml')
RELAX_LICENSECLASS = os.path.join(RELAX_PATH, 'licenseclass.relax.xml')
RELAX_ISSUE = os.path.join(RELAX_PATH, 'issue.relax.xml')
RELAX_ERROR = os.path.join(RELAX_PATH, 'error.relax.xml')
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
    res = app.get('/classes')
    classes = []
    classdoc = lxml.etree.parse(StringIO(res.body))
    for license in classdoc.xpath('//license/@id'):
        classes.append(license)
    return classes

def _field_enums(lclass):
    """Retrieve the license information for this class, and generate a set of answers for use with testing."""
    res = app.get('/license/%s' % lclass)
    all_answers = []
    classdoc = lxml.etree.parse(StringIO(res.body))
    for field in classdoc.xpath('//field'):
        field_id = field.get('id')
        answer_values = []
        for e in field.xpath('./enum'):
            answer_values.append(e.get('id'))
        all_answers.append((field_id, answer_values))
    return all_answers

def _get_locales():
    """Return a list of supported locales."""
    res = app.get('/locales')
    locale_doc = lxml.etree.parse(StringIO(res.body))
    return [n for n in locale_doc.xpath('//locale/@id') if n not in ('he',)]

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

def test_issue(): #TODO: FIX THIS FAILING TEST
    """Test that every license class will be successfully issued via the /issue method."""
    for lclass in _get_license_classes():
        for answers in _test_answers_xml(lclass):
            res = app.get('/license/%s/issue?answers=%s' %
                          (lclass, answers))
            assert relax_validate(RELAX_ISSUE, res.body)

def test_get(): #TODO: FIX THIS FAILING TEST
    """Test that every license class will be successfully issued via the /get method."""
    for lclass in _get_license_classes():
        for query_string in _test_answer_query_strings(lclass):
            res = app.get('/license/%s/get%s' % (lclass, query_string))
            assert relax_validate(RELAX_ISSUE, res.body)

def test_get_extra_args(): #TODO: FIX THIS FAILING TEST
    """Test the /get method with extra nonsense arguments; extra arguments should be ignored."""
    for lclass in _get_license_classes():
        for query_string in _test_answer_query_strings(lclass):
            res = app.get('/license/%s/get%s&foo=bar' % (lclass, query_string))
            assert relax_validate(RELAX_ISSUE, res.body)

def test_issue_error():
    """Issue with no answers or empty answers should return an error."""
    res = app.get('/license/blarf/issue?answers=<foo/>')
    assert relax_validate(RELAX_ERROR, res.body)

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

if __name__ == '__main__':
    pass
