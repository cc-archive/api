#!/usr/bin/env python

"""
soap.py
$Id$

Creative Commons API SOAP interface
(c) 2004, Nathan R. Yergler, Creative Commons
"""

import ZSI.dispatch
import xmlutils
import libxml2
import libxslt

XML_SOURCE = "questions.xml"
XSLT_SOURCE = 'chooselicense.xsl'

XML_DATA = xmlutils.XPathDict(file=XML_SOURCE)

def __xp_license(license):
    return [n for n in XML_DATA.xpnodes('//questions/license')
               if n['id'] == license]

def __xp_field(license, field_id):
    return [n for n in __xp_license(license)[0].xpnodes('field')
            if n['id'] == field_id]

def licenses():
    """Returns a list of licenses supported."""
    return [n['id'] for n in XML_DATA.xpnodes('//questions/license')]

def fields(license, lang='en'):
    """Returns a sequence of field identifiers which must be supplied
    in order to generate the desired license.
    """
    
    license = __xp_license(license)[0]

    return [n['id'] for n in license.xpnodes('field')]

def fieldDetail(license, field_id, lang='en'):
    """Returns a sequence of two element sequences (ie, immutable "dict"),
    which contains the information necessary for rendering a UI for a given
    license, field and (optionally) language.
    """
    
    XPATH_MAP = (
        ('id', 'id'),
        ('label', "label[@xml:lang='%s']" % lang),
        ('description', "description[@xml:lang='%s']" % lang),
        ('type', 'type'),
        )

    field = __xp_field(license, field_id)[0]

    return field.tuple_extract(XPATH_MAP)

def fieldEnum(license, field_id, lang='en'):
    """Returns a sequence of (id, label) pairs for the enumeration
    possibilities for a given field and license. If specified field is not
    of type "enum", an empty sequence is returned.
    """

    XPATH_MAP=(
        ('id', 'id'),
        ('label', "label[@xml:lang='%s']" % lang)
        )

    enums = __xp_field(license, field_id)[0].xpnodes('enum')

    return tuple([n.tuple_extract(XPATH_MAP) for n in enums])

def getLicense(license, answers):
    """Given a mapping of answers, returns a license URI.  Keys for the
    answers mapping are the field identifiers returned by fields.
    """

    # generate the answers XML document
    ctxt = libxml2.createPushParser(None, '', 0, 'answer.xml')

    answer_xml = """
    <answers>
      <license-%s>""" % license

    for key in answers:
        answer_xml = """%s
        <%s>%s</%s>""" % (answer_xml, key, answers[key], key)
    
    answer_xml = """%s
      </license-%s>
    </answers>
    """ % (answer_xml, license)

    ctxt.parseChunk(answer_xml, len(answer_xml), True)
    
    # apply the xslt transform
    transform = libxslt.parseStylesheetFile(XSLT_SOURCE)

    ans_doc = ctxt.doc()
    result = transform.applyStylesheet(ans_doc, None)
    
    # return the transformed document
    return transform.saveResultToString(result)
        
if __name__ == '__main__':
    # dispatch the request as a CGI call
    ZSI.dispatch.AsCGI()
