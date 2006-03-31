"""
license.py
$Id$

CC REST API method implementation.

(c) 2004-2005, Creative Commons, Nathan R. Yergler
Licensed under the GNU GPL 2 or later.
"""

import lxml.etree

import quixote
import const
import support

_q_exports = ['classes']

def details(request):
    license_uri = request.form.get('license-uri')

    # work backwards, generating the answers from the license code
    code, jurisdiction = support.licenseUrlToCode(license_uri)
    answers = support.licenseCodeToAnswers(code, jurisdiction)

    return support.issue(answers)

def classes (request):
    # use XPath to extract the license nodes from the source document
    doc = lxml.etree.parse(const.XML_SOURCE)

    # extract the label list
    classes = doc.xpath('//licenseclass')
    result = "<licenses>"
    
    for label in classes:
        # for each label, get the ID and add the XML to the result
        l_result = '<license id="%s">%s</license>' % \
                   (label.attrib.get('id'),
                    label.xpath('label')[0].text)
        
        result = result + "\n" + l_result

    result = result + "</licenses>"
    return result

class License:
    """Implementation of license-specific methods for CC REST API."""
    
    _q_exports = ['issue']
    
    def __init__(self, request, name):
        self.name = name
        self.license = None

    def _q_index(self, request):
        doc = lxml.etree.parse(const.XML_SOURCE)

        license = doc.xpath('//licenseclass[@id="%s"]' % self.name)
        if len(license) > 0:
            self.license = license[0]
            return lxml.etree.tostring(self.license) #self.license.tostring()
        else:
            self.license = None
            return None

        # if not found, raise error
        raise quixote.errors.TraversalError("No such license: %s" % self.name)

    def issue(self, request):
        """Issues a CC license, based on the answers form variable;
        answers is assumed to contain a valid XML document, per the
        chooselicense-xml CC Tools project.

        Returns an XML document containing the license URL and RDF."""

        # retrieve the answers xml
        answer_xml = request.form.get('answers')

        return support.issue(answer_xml)

def _q_lookup(request, name):
    return License(request, name)

