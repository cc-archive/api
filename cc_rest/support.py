
from StringIO import StringIO

import const
import lxml.etree

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
        lxml.etree.parse(const.XSLT_SOURCE)
        )

    result = transform.apply(ctxt)

    # return the transformed document
    return transform.tostring(result)
    
