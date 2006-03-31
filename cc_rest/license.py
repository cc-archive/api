"""
license.py
$Id$

CC REST API method implementation.

(c) 2004, Creative Commons, Nathan R. Yergler
Licensed under the GNU GPL 2 or later.
"""

import libxml2
import libxslt

import quixote
import const

_q_exports = ['classes']

def classes (request):
    # use XPath to extract the license nodes from the source document
    doc = libxml2.parseFile(const.XML_SOURCE)
    ctxt = doc.xpathNewContext()

    # extract the label list
    labels = ctxt.xpathEval('//licenseclass/label')
    result = "<licenses>"
    
    for label in labels:
        # for each label, get the ID and add the XML to the result
        l_result = '<license id="%s">%s</license>' % \
                   (label.parent.xpathEval('@id')[0].content,
                    label.content)
        
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
        doc = libxml2.parseFile(const.XML_SOURCE)
        ctxt = doc.xpathNewContext()

        license = ctxt.xpathEval('//licenseclass[@id="%s"]' % self.name)
        if len(license) > 0:
            self.license = license[0]
            return self.license.serialize()
        #else:
        #    self.license = None
        #    return None

        # if not found, raise error
        raise quixote.errors.TraversalError("No such license: %s" % self.name)

    def issue(self, request):
        """Issues a CC license, based on the answers form variable;
        answers is assumed to contain a valid XML document, per the
        chooselicense-xml CC Tools project.

        Returns an XML document containing the license URL and RDF."""

        # retrieve the answers xml
        answer_xml = request.form.get('answers')

        # generate the answers XML document
        ctxt = libxml2.createPushParser(None, '', 0, 'answer.xml')
        ctxt.parseChunk(answer_xml, len(answer_xml), True)

        # apply the xslt transform
        transform = libxslt.parseStylesheetFile(const.XSLT_SOURCE)
        ans_doc = ctxt.doc()
        result = transform.applyStylesheet(ans_doc, None)

        # return the transformed document
        return transform.saveResultToString(result)

def _q_lookup(request, name):
    return License(request, name)

