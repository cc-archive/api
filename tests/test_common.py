
import lxml
from StringIO import StringIO
import os
import operator

import cherrypy
import webtest # for the TestApi base class

##################
## Public names ##
##################
__all__ = (
           'RELAX_PATH',
           'relax_validate',
           'TestApi',
           'TestData', # TODO: remove this after the migration to classes
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

#####################
## Utility classes ##
#####################
class TestData:
    """Generates test data for use in exercising the CC API."""

    def _permute(self, lists): #TODO: document function
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

    def license_classes(self):
        return ['standard', 'publicdomain', 'recombo']

    def _field_enums(self, lclass):
        """Retrieve the license information for this class, and generate 
           a set of answers for use with testing."""
        return [
                ('commercial', ['y', 'n']),
                ('derivatives', ['y', 'sa', 'n']),
                ('jurisdiction', ['', 'us', 'de', 'uk'])
               ]

    def _get_locales(self):
        """Return a list of supported locales."""
        locales = [
                    'en', # English
                    'de', # German
                    # 'he', # Hebrew TODO: fix html <span dir="rtl"> formatting
                    'el', # Greek
                  ]
        return locales

    def xml_answers(self, lclass): # TODO: document function
        all_answers = self._field_enums(lclass)
        all_locales = self._get_locales()
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

    def query_string_answers(self, lclass): # TODO: document function
        all_answers = self._field_enums(lclass)
        all_locales = self._get_locales()
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

##########################
## Base class for tests ##
##########################
class TestApi:
    """Base class of test classes for the CC API. Defines test fixture
       behavior for creating and destroying webtest.TestApp instance of 
       the WSGI server."""

    def setUp(self):
        """Test fixture for nosetests:
           - sets up the WSGI app server
           - creates test data generator"""
        cherrypy.config.update({ 'global' : { 'log.screen' : False, } })
        cfgstr = 'config:%s' % (os.path.join(os.getcwd(), '..', 'server.cfg'))
        self.app = webtest.TestApp(cfgstr)
        self.data = TestData()

    def tearDown(self):
        """Test fixture for nosetests:
           - tears down the WSGI app server"""
        cherrypy.engine.exit()
