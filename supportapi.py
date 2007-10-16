from StringIO import StringIO
import sys
import os
import re
import traceback

from babel.messages.pofile import read_po

import cherrypy
import cherrypy._cperror as cperror
import lxml.etree 

import support

class SupportApi(object):

    def __loadLocale(self, language):
        po_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'license_xsl',
                               'i18n',
                               'i18n_po',
                               language,
                               'cc_org.po')

        if not(os.path.exists(po_file)):
            po_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   'license_xsl',
                                   'i18n',
                                   'i18n_po',
                                   'en',
                                   'cc_org.po')

        result = read_po(file(po_file, 'r'))
                
        # XXX inject the right key for the generic jurisdiction
        #result.strings['country.-'] = unicode.encode(
        #    result.get('util.Generic', 'Generic'), 'utf8')
        
        return result
    
    @cherrypy.expose
    def jurisdictions(self, select=None, locale='en', language=None,
                      **kwargs):

        # backward compatibility for crufted "language" param
        if language is None:
            language = locale
            
        # determine our actual functional locale
        language = support.actualLocale(language)
        
        # load the licenses file
        licenses_xml = lxml.etree.parse(support.LICENSES_XML)

        # load the .po file for translating country names or
        # load English if the requested locale is unavailable
        
        locale = self.__loadLocale(language)
        en = self.__loadLocale('en')
        
        # check if we should include the <select> element
        if select:
            yield('<select name="%s">\n' % select)
            
        # retrieve a list of the available jurisdictions in the requested lang
        jurisdictions = []
        j_nodes = licenses_xml.xpath('//jurisdiction-info[@launched="true"]')
        for j in j_nodes:
            jurisdictions.append( (j.xpath('@id')[0],
                                   j.xpath('./uri')[0].text) )

        # output each jurisdiction
        for j_id, j_url in jurisdictions:

            # we don't care about Unported here
            if j_id == '-':
                continue
            
            country_id = 'country.%s' % j_id

            if country_id in locale:
                country = locale[country_id].string
            elif country_id in en:
                country = en[country_id].string
            else:
                country = country_id
            
            yield(u'<option value="%s">%s</option>\n' % (j_url, country) )

        if select:
            yield('</select>')

    @cherrypy.expose
    def jurisdictions_js(self, select=None, locale='en', language=None,
                         **kwargs):

        # backward compatibility for crufted "language" param
        if language is None:
            language = locale

        # determine our actual functional locale
        language = support.actualLocale(language)
        
        # set the content type
        cherrypy.response.headers['Content-Type'] = 'text/javascript'

        # delegate to the basic method
        for line in self.jurisdictions(select, language):
            yield("document.write('%s');\n" % line.strip())

    
