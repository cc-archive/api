import os
import sys
from StringIO import StringIO
import traceback

import lxml.etree
import tidy
#from cherrypy.lib.filter.basefilter import BaseFilter

import api_exceptions


#import cc.license
from multiprocessing import Process, Array
from copy import deepcopy

DATA_DIR = os.path.join( os.path.dirname(os.path.abspath(__file__)),
                         'license_xsl')

QUESTIONS_XML = os.path.join(DATA_DIR, 'questions.xml')
LICENSES_XML = os.path.join(DATA_DIR, 'licenses.xml')
XSLT_SOURCE = os.path.join(DATA_DIR, 'chooselicense.xsl')

def pruneLocale(element, locale):
    """Prune elelments who have an xml:lang value other than locale."""

    XML_LANG = '{http://www.w3.org/XML/1998/namespace}lang'

    for node in element.xpath('//*[@xml:lang]'):
        if node.get(XML_LANG) != locale:
            node.clear()
            node.xpath('..')[0].remove(node)
            del node
    
def xmlError(error_id, message, exc_info=None, suggestion=None):
    """Generate an XML encoded error message with the specified error_id
    and message; exc_info is a 3 tuple, like that returned from
    sys.exc_info(), if specified."""
    
    error = lxml.etree.Element('error')
    lxml.etree.SubElement(error, 'id').text = error_id
    lxml.etree.SubElement(error, 'message').text = message

    if suggestion:
        print suggestion
        lxml.etree.SubElement(error, 'suggestion').text = suggestion

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
    pieces = pieces[pieces.index('licenses') + 1 :]
    pieces.reverse()

    # check if we have license-code only
    if len(pieces) == 1:
        # one piece? must be a license code
        return (pieces[0], '')
    
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

def licenseCodeToAnswers(licenseCode, jurisdiction='', locale=''):
    """Takes an old style license code (ie, by-nc-nd) and generates the
    appropriate answers.xml string for parsing by chooselicense.xsl.
    """

    answers = {'jurisdiction':jurisdiction}
    pieces = [n.strip() for n in licenseCode.split('-')]

    # determine the license type
    is_samp = len([n for n in pieces if n.find('sampling') > -1]) > 0
    is_pd = ('pd' in pieces) or ('publicdomain' in pieces)
    is_plain = not(is_samp or is_pd)

    # munch the pieces
    if is_samp:
       # this is a sampling license -- which is just a single question
       answers['sampling'] = "".join(pieces).replace('+', 'plus')

    # generate and return the XML
    for p in pieces:
       # check for derivatives status
       if p in ['nd', 'sa']:
              if p == 'nd':
                     answers['derivatives'] = 'n'
              else:
                     answers['derivatives'] = p

       if p == 'nc' and not(is_samp):
              answers['commercial'] = 'n'

    if is_plain:
       lclass = 'standard'
    elif is_samp:
       lclass = 'recombo'
    elif is_pd:
       lclass = 'publicdomain'

    xml = """<answers>
    <locale>%s</locale>
    <license-%s>
    %s
    </license-%s>
    </answers>""" % (locale, lclass, 
                                     "\n".join(["<%s>%s</%s>" % (n, answers[n], n) for n in answers.keys()]),
                                     lclass)

    return xml

def valid_jurisdictions():
    """Load the list of valid, launched jurisdictions."""

    license_xml = lxml.etree.parse(LICENSES_XML)

    return license_xml.xpath('//jurisdiction-info[@launched="true"]/@id')

def valid_classes():
    """Return a list of valid license classes, extracted from questions.xml"""

    questions = lxml.etree.parse(QUESTIONS_XML)

    return questions.xpath('//licenseclass/@id')

def valid_fields(license_class):
    """Returns a list of valid field names for the license class."""

    questions = lxml.etree.parse(QUESTIONS_XML)

    return questions.xpath('//licenseclass[@id="%s"]/field/@id' %
                           license_class)

def valid_values(license_class, field_id):
    """Returns a list of valid values for the specified field and license."""

    questions = lxml.etree.parse(QUESTIONS_XML)

    return questions.xpath('//licenseclass[@id="%s"]/field[@id="%s"]/enum/@id'
                           % (license_class, field_id))

def validateAnswers(answers_xml):
    """Take a string containing the answers.xml for a license and make
    sure they pass basic sanity checks.  Return True if they pass, raise
    an AnswerXmlException (or sub-class) if they do not."""

    # parse the answers
    answers_doc = lxml.etree.parse(StringIO(answers_xml))

    # validate license class
    license_root = None
    license_class = None
    for c in valid_classes():
        if len(answers_doc.xpath('//license-%s' % c)) > 0:
            license_root = answers_doc.xpath('//license-%s' % c)[0]
            license_class = c

            break

    # see if we exited without finding a <license-*> element
    if license_root is None:
        raise api_exceptions.InvalidClassException()

    # validate each field answer
    for f in license_root:
        if f.tag == 'locale':
            continue
        
        if f.text not in valid_values(license_class, f.tag):
            # special case handling for jurisdiction
            if f.tag == 'jurisdiction': # and f.text not in (None, '-', ''):
                # fall back to the generic jurisdiction
                f.text = '-'
                continue
            
            raise api_exceptions.InvalidFieldValue(f.tag, f.text)
    
    # all tests pass -- return the XML document (which we may have twiddled)
    return answers_doc


def buildResultsTree(rdf_string=None, rdfa_string=None):

    results = lxml.etree.XML('<result></result>')

    if rdf_string is None or rdfa_string is None:
        return results
    
    rdf_tree = lxml.etree.parse(StringIO(rdf_string))
    rdfa_tree = lxml.etree.parse(StringIO(rdfa_string))
    
    # form an element tree to return to issue()
    lxml.etree.SubElement(results, 'license-uri').text = \
                    'http://creativecommons.org/publicdomain/zero/1.0/'
    lxml.etree.SubElement(results, 'license-name').text = 'CC0'

    # deprecated, but still needs to be supported
    rdf_segment = deepcopy(rdf_tree) # rdf_tree is mutable
    # an <rdf> tree with an empty <Work> tree and the rdfa as children
    rdf_segment.getroot().insert(0, lxml.etree.Element('Work') )
    lxml.etree.SubElement(results, 'rdf').append( rdf_segment.getroot() )

    # append the results from the cc.license formatter
    lxml.etree.SubElement(results, 'licenserdf').append( rdf_tree.getroot() )
    lxml.etree.SubElement(results, 'html').append( rdfa_tree.getroot() )

    return results

def issue_CC0(ctxt):
    """
    !!!HackYikeS!!!

    CC0 in the license_xsl based api was hackish from the forefront
    and this routine is no exception.

    When a CC0 license is requested, rather than relying on license_xsl to
    tranform the answers, instead the more up-to-date cc.license API is used
    to represent the license in RDF and HTML+RDFa formats.

    Because librdf and lxml both utilize libxml2, there is a unavoidable
    error that will occur on the lxml side whenever librdf is imported into
    the same Python thread. This is due to a global lock that is placed on
    libxml2 made during the rdflib negotiations with the libxml2 library.

    To avoid this lock, rdflib must be imported in a seperate process, so that
    the XSLT transformations in issue() may succeed. This is approach is far
    from ideal, but it works and until the REST api is moved to an RDF backend,
    this will need to make do.

    """

    if not ctxt.findall('license-zero'):
        return buildResultsTree() # returns an empty results etree
    
     # prepare the paramters for the cc.license formatter
    work_dict = dict(
        work_title = ctxt.findtext('work-info/title') or '',
        actor_href = ctxt.findtext('work-info/work-url') or '',
        name = ctxt.findtext('work-info/creator') or '')

    locale = ctxt.findtext('locale') or 'en_US'

    # pointers that the subprocess will set
    cc0_rdf =  Array('c', 750) 
    cc0_rdfa = Array('c', 750)

    """ This api call brought to you by Python 2.6's multiprocessing module."""
    def cc_license_api_process (rdf_string, rdfa_string,
                                work_info, locale):

        # dire solution
        import cc.license

        cc0 = cc.license.by_code('CC0') 
        formatter = cc.license.formatters.classes.CC0HTMLFormatter()
        
        # set the shared variables
        rdf_string.value = cc0.rdf
        rdfa_string.value = formatter.format(cc0, work_info, locale)

    # create and join a new subprocess
    p = Process(target=cc_license_api_process,
                args=(cc0_rdf, cc0_rdfa, work_dict, locale))
    # start and wait for cc.license
    p.start()
    p.join()

    # pass along the information to be constructed into an ETree
    return buildResultsTree(cc0_rdf.value, cc0_rdfa.value)
        
def issue(answers_xml):

    # validate the answers
    # validateAnswers(answers_xml)
        
    # generate the answers XML document
    ctxt = validateAnswers(answers_xml) # lxml.etree.parse(StringIO(answers_xml)) 

    # apply the xslt transform
    transform = lxml.etree.XSLT(lxml.etree.parse(XSLT_SOURCE))

    result = transform.apply(ctxt)

    if result.getroot() == None:
        # give CC0 a whack
        return lxml.etree.tostring(issue_CC0(ctxt))
    
    # return the transformed document, after passing it through tidy
    return transform.tostring(result)

def license_details(license_uri, locale='en'):
    """Return an XML element which roots the information
    that would typically be issued for the license URI;
    if specified, locale is used to localize the license
    names."""

    # work backwards, generating the answers from the license code
    code, jurisdiction = licenseUrlToCode(license_uri)
    answers = licenseCodeToAnswers(code, jurisdiction, locale)

    return issue(answers)
    
def locales():
    """Return a list of available locales based on the translations in
    licenses.xml."""

    # use XPath to extract the license nodes from the source document
    doc = lxml.etree.parse(QUESTIONS_XML)

    # extract and return the locale list
    return set([n for n in doc.xpath('//@xml:lang')])

def actualLocale(locale):
    """Determine and return the actual locale based on the requested one.
    If the requested locale is supported, simply return that.  If not, check
    the language only specification (i.e. es instead of es_ES).  If that
    is not supported, return our fallback (English)."""

    supported_locales = locales()
    if locale in supported_locales:
        return locale

    if locale.split('_')[0] in supported_locales:
        return locale.split('_')[0]

    return 'en'

def actualJurisdiction(jurisdiction, default='-'):
    """Check if the specified jurisdiction is actually supported; if it
    is, return it unchanged.  Otherwise return the [default] value."""
    
    if jurisdiction in valid_jurisdictions():
        return jurisdiction

    return default

## class UrlSpaceFilter(BaseFilter):
##     """Filter that masks the fact that the CP app may be in a sub-space of the
##     URL root.
##     """
    
##     def beforeRequestBody(self):
##         import cherrypy
        
##         if not cherrypy.config.get('urlSpaceFilter.on', False):
##             return
        
##         req = cherrypy.request
##         urlSpace = cherrypy.config.get('urlSpaceFilter.urlSpace', '')

##         req.path = req.path.replace(urlSpace, '')
## 	if req.path == '':
## 	   req.path = '/'
##         #req.base = newBaseUrl
