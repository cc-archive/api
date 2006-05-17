"""
Creative Commons Web Services Test Harness
Copyright (c) 2005-2006,
     Nathan R. Yergler, 
     Creative Commons (software@creativecommons.org)

Based on test code from the CherryPy Project, 
Copyright (c) 2004, CherryPy Team (team@cherrypy.org)
All rights reserved.

See docs/LICENSE for redistribution restrictions.

"""

import os
import sys
import unittest
from StringIO import StringIO
import random

# fix up the PYTHON PATH to include the directory we're running from
sys.path.insert(0, os.getcwd())

from rest_api import *

cherrypy.config.update({
    'global': {
        'server.logToScreen': False,
        'server.environment': "production",
    }
})

RELAX_PATH = './relax'
QUESTIONS_XML = (os.path.join('license_xsl', 'questions.xml'),
                 'questions.relax.xml')
LICENSES_XML = (os.path.join('license_xsl', 'licenses.xml'),
                'licenses.relax.xml')

import cherrypy.test.helper as helper

def RelaxValidate(schemaFileName, instanceFileName):

    relaxng = lxml.etree.RelaxNG(lxml.etree.parse(schemaFileName))
    instance = lxml.etree.parse(instanceFileName)

    return relaxng.validate(instance)

def permute(Lists):
  import operator
  if Lists:
    result = map(lambda I: (I,), Lists[0])

    for list in Lists[1:]:
      curr = []
      for item in list:
        new = map(operator.add, result, [(item,)]*len(result))
        curr[len(curr):] = new
      result = curr
  else:
    result = []

  return result

class TestXmlFiles(unittest.TestCase):

    def testQuestionsXml(self):
	"""Make sure questions.xml is compliant."""
        self.assert_(RelaxValidate(os.path.join(RELAX_PATH, QUESTIONS_XML[1]), 
				   QUESTIONS_XML[0]),
                    "questions.xml does not comply to the Relax-NG schema.")

    def testLicensesXml(self):
	"""Make sure licenses.xml is compliant."""
        self.assert_(RelaxValidate(os.path.join(RELAX_PATH, LICENSES_XML[1]), 
				   LICENSES_XML[0]),
                    "licenses.xml does not comply to the Relax-NG schema.")
                    

class CcApiTest(helper.CPWebCase):
    def testLocalizations(self):
        """Test that /locales returns a list of supported languages."""
        self.getPage('/locales')

        assert RelaxValidate(os.path.join(RELAX_PATH,
                                          'locales.relax.xml'),
                             StringIO(self.body))

    def testClasses(self):
	"""Test that /classes and / are synonyms."""
	self.getPage('/')
	root_body = self.body
	
	self.getPage('/classes')
	classes_body = self.body

	assert root_body == classes_body

    def testInvalidClass(self):
        """An invalid license class name should return an explicit error."""
        
        self.getPage('/license/noclass')

        assert RelaxValidate(os.path.join(RELAX_PATH,
                                          'error.relax.xml'),
                             StringIO(self.body))

    def testClassesStructure(self):
	"""Test the return value of /classes to ensure it fits with our
	claims."""
	self.getPage('/classes')
	
	assert RelaxValidate(os.path.join(RELAX_PATH, 'classes.relax.xml'),
			     StringIO(self.body))

    def __getLicenseClasses(self):
	"""Get the license classes."""
	self.getPage('/classes')

	classes = []
	classdoc = lxml.etree.parse(StringIO(self.body))
	for license in classdoc.xpath('//license/@id'):
	    classes.append(license)

	return classes

    def __fieldEnums(self, lclass):
        """Retrieve the license information for this class, and generate
        a set of answers for use with testing."""


        self.getPage('/license/%s' % lclass)

        all_answers = []
        classdoc = lxml.etree.parse(StringIO(self.body))

        for field in classdoc.xpath('//field'):
            field_id = field.get('id')
            
            answer_values = []
            for e in field.xpath('./enum'):
                answer_values.append(e.get('id'))

            all_answers.append((field_id, answer_values))

        return all_answers

    def __testAnswersXml(self, lclass):

        all_answers = self.__fieldEnums(lclass)

        for answer_comb in permute([n[1] for n in all_answers]):
            
            answers_xml = lxml.etree.Element('answers')
            class_node = lxml.etree.SubElement(answers_xml, 'license-%s' % lclass)


            for a in zip([n[0] for n in all_answers], answer_comb):
                a_node = lxml.etree.SubElement(class_node, a[0])
                a_node.text = a[1]

            yield lxml.etree.tostring(answers_xml)

    def __testAnswerQueryStrings(self, lclass):
        all_answers = self.__fieldEnums(lclass)

        for answer_comb in permute([n[1] for n in all_answers]):

            params = zip([n[0] for n in all_answers], answer_comb)
            param_strs = ["=".join(n) for n in params]
            result = "?" + "&".join(param_strs)

            yield result
        
    def testLicenseClassStructure(self):
	"""Test that each license class returns a valid XML chunk."""

	for lclass in self.__getLicenseClasses():
	    self.getPage('/license/%s' % lclass)

	    try:
		assert RelaxValidate(os.path.join(RELAX_PATH, 
					      'licenseclass.relax.xml'),
				 StringIO(self.body))
	    except AssertionError:
                print self.body
		print "Returned value for %s does not comply with " \
		      "RelaxNG schema." % lclass
		raise AssertionError
		    
    def testIssue(self):
	"""Test that every license class will be successfully issued via
        the /issue method."""

	for lclass in self.__getLicenseClasses():

            for answers in self.__testAnswersXml(lclass):
              print >> sys.stderr, ',',
              try:
                
                self.getPage('/license/%s/issue?answers=%s' % (lclass, answers))
              
                assert RelaxValidate(os.path.join(RELAX_PATH, 
                                               'issue.relax.xml'),
                                     StringIO(self.body))

              except AssertionError:
                print "Issue license failed for:\nlicense class: %s\n" \
                      "answers: %s\n" % (lclass, answers)
                raise AssertionError

    def testGet(self):
	"""Test that every license class will be successfully issued
        via the /get method."""

	for lclass in self.__getLicenseClasses():

            for queryString in self.__testAnswerQueryStrings(lclass):
              print >> sys.stderr, ';',
              try:
                
                self.getPage('/license/%s/get%s' % (lclass, queryString))

                assert RelaxValidate(os.path.join(RELAX_PATH, 
                                               'issue.relax.xml'),
                                     StringIO(self.body))

              except AssertionError:
                print "Get license failed for:\nlicense class: %s\n" \
                      "answers: %s\n" % (lclass, queryString)
                raise AssertionError

    def testIssueError(self):
        """Issue with no answers or empty answers should return an error."""

	for lclass in self.__getLicenseClasses():
            self.getPage('/license/%s/issue' % lclass)

            assert RelaxValidate(os.path.join(RELAX_PATH,
                                              'error.relax.xml'),
                                 StringIO(self.body))

    def testI18n(self):
	"""Make sure i18n calls work right."""

    def testLicenseDetails(self):
	"""Test that the license details call responds appropriately."""

        # test valid URIs
	TEST_URIS = ('http://creativecommons.org/licenses/by-nc-nd/2.5/',
                     'http://creativecommons.org/licenses/by-nc-sa/2.5/',
                     'http://creativecommons.org/licenses/by-sa/2.5/',
                     'http://creativecommons.org/licenses/by/2.0/nl/',
                    )

        for uri in TEST_URIS:
            self.getPage('/details?license-uri=%s' % uri)

            try:              
                assert RelaxValidate(os.path.join(RELAX_PATH, 
                                               'issue.relax.xml'),
                                     StringIO(self.body))

            except AssertionError:
                print "License details failed for the URI %s" % uri
                raise AssertionError

        # test that an invalid URI raises an error
        uri = "http://creativecommons.org/licenses/blarf"
        self.getPage('/details?license-uri=%s' % uri)

        assert RelaxValidate(os.path.join(RELAX_PATH,
                                          'error.relax.xml'),
                             StringIO(self.body))

    def testDetailsError(self):
        """A call to /details with no license-uri should return a
        missingparam error."""

        self.getPage('/details')

        assert RelaxValidate(os.path.join(RELAX_PATH,
                                          'error.relax.xml'),
                             StringIO(self.body))

if __name__ == "__main__":
    helper.testmain()
