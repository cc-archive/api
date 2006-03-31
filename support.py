import sys
from StringIO import StringIO
import traceback

import lxml.etree
from cherrypy.lib.filter.basefilter import BaseFilter


QUESTIONS_XML = 'questions.xml'
XSLT_SOURCE = 'chooselicense.xsl'

def pruneLocale(element, locale):
    """Prune elelments who have an xml:lang value other than locale."""

    XML_LANG = '{http://www.w3.org/XML/1998/namespace}lang'

    for node in element.xpath('//*[@xml:lang]'):
        if node.get(XML_LANG) != locale:
            node.xpath('..')[0].remove(node)
    
def xmlError(error_id, message, exc_info=None):
    """Generate an XML encoded error message with the specified error_id
    and message; exc_info is a 3 tuple, like that returned from
    sys.exc_info(), if specified."""
    
    error = lxml.etree.Element('error')
    lxml.etree.SubElement(error, 'id').text = error_id
    lxml.etree.SubElement(error, 'message').text = message

    # check if there's a current exception
    if exc_info is not None:
        exc_type, exc_value, tb = exc_info

        lxml.etree.SubElement(error, 'traceback').text = "".join(
            traceback.format_tb(tb)
            )
        lxml.etree.SubElement(error, 'exception',
                              type=str(exc_type)).text = str(exc_value)

    return lxml.etree.tostring(error)
    

def licenseUrlToCode(lurl):
    # Takes a license URL and converts it to a license code + jurisdiction.
    # Returns a tuple of (code, jurisdiction)

    pieces = [n for n in lurl.split('/') if n.strip()]
    pieces.reverse()

    # find out if we have a jurisdiction
    try:
       float(pieces[0])

       # no jurisdiction
       jurisdiction = ''
       code = pieces[1]
    except:
       # jurisidiction present
       jurisdiction = pieces[0]
       code = pieces[2]

    return (code, jurisdiction)

def licenseCodeToAnswers(licenseCode, jurisdiction=''):
    """Takes an old style license code (ie, by-nc-nd) and generates the
    appropriate answers.xml string for parsing by chooselicense.xsl.
    """

    answers = {'jurisdiction':jurisdiction}
    pieces = [n.strip() for n in licenseCode.split('-')]

    # determine the license type
    is_samp = len([n for n in pieces if n.find('sampling') > -1]) > 0
    is_pd = ('pd' in pieces)
    is_plain = not(is_samp or is_pd)

    # munch the pieces
    if is_samp:
       # this is a sampling license
       answers['sampling'] = [n for n in pieces if n.find('sampling') > -1][0]

    # generate and return the XML
    for p in pieces:
       # check for derivatives status
       if p in ['nd', 'sa']:
              if p == 'nd':
                     answers['derivatives'] = 'n'
              else:
                     answers['derivatives'] = p

       if p == 'nc':
              answers['commercial'] = 'n'

    if is_plain:
       lclass = 'standard'
    elif is_samp:
       lclass = 'recombo'
    elif is_pd:
       lclass = 'publicdomain'

    xml = """<answers>
    <license-%s>
    %s
    </license-%s>
    </answers>""" % (lclass, 
                                     "\n".join(["<%s>%s</%s>" % (n, answers[n], n) for n in answers.keys()]),
                                     lclass)

    return xml

def issue(answers_xml):
    
    # generate the answers XML document
    ctxt = lxml.etree.parse(StringIO(answers_xml)) 

    # apply the xslt transform
    transform = lxml.etree.XSLT(
        lxml.etree.parse(XSLT_SOURCE)
        )

    result = transform.apply(ctxt)

    # return the transformed document
    return transform.tostring(result)
    

class UrlSpaceFilter(BaseFilter):
    """Filter that masks the fact that the CP app may be in a sub-space of the
    URL root.
    """
    
    def beforeRequestBody(self):
        import cherrypy
        
        if not cherrypy.config.get('urlSpaceFilter.on', False):
            return
        
        req = cherrypy.request
        urlSpace = cherrypy.config.get('urlSpaceFilter.urlSpace', '')

        req.path = req.path.replace(urlSpace, '')
	if req.path == '':
	   req.path = '/'
        #req.base = newBaseUrl
