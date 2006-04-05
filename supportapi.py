from StringIO import StringIO
import sys
import os
import re
import traceback

import cherrypy
import cherrypy._cperror as cperror
import lxml.etree 

import support

        
class PoFile(object):
    def __init__(self, filename):
        self.filename = filename
        self.language = None
        
        self.reload()

    def reload(self):
        """Reload the .po file and parse it's contents."""
        var_re = re.compile('\$\{.*?\}', re.I|re.M|re.S)
        
        self.metadata = {}
        self.strings = {}

        curkey = None
        input_file = file(self.filename, 'r')
        
        for line in input_file:
            line = line.strip()
            if line == "":
                continue
            
            # parse each line in the file
            words = line.split(' ', 1)

            # check for a message 
            if words[0].lower() == 'msgid':
                curkey = words[1][1:-1]

            # check for a translation
            elif words[0].lower() == 'msgstr':
                value = words[1][1:-1]

                value = value.replace('\\"', '"')
                match = var_re.search(value)
                while match is not None:
                    if value[match.start() - 1] != '"':

                        #<xsl:value-of select="$license-name"/>
                        value = value[:match.start()] + \
                                '<xsl:value-of select="$' + \
                                value[match.start() + 2:match.end() - 1] + \
                                '"/>' + value[match.end():]
                    else:
                        value = value[:match.start()] + \
                                '{$' + \
                                value[match.start() + 2:match.end() - 1] + \
                                '}' + value[match.end():]
                        
                    match = var_re.search(value, match.end())
                    
                self.strings[curkey] = value
                curkey = None

            # check for metadata
            elif line[0] == line[-1] == '"':
                key, value = [n.strip() for n in
                              line[1:-1].strip().split(':', 1)]

                # check for bogus escaped CRs
                if value[-2:] == '\\n':
                    value = value[:-2]
                    
                self.metadata[key] = value

                if key == 'Language-Code':
                    self.language = value

            else:
                print 'unknown line:\n%s' % line
                
    def __getitem__(self, key):
        return self.strings[key]

    def get(self, key, default):
        if key in self.strings:
            return unicode(self.strings[key], 'utf8')
        else:
            return default

class SupportApi(object):

    def __loadLocale(self, language):
        po_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'license_xsl',
                               'i18n',
                               'i18n_po',
                               'icommons-%s.po' % language)

        if not(os.path.exists(po_file)):
            po_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   'license_xsl',
                                   'i18n',
                                   'i18n_po',
                                   'icommons-en.po')

        result = PoFile(po_file)

        # inject the right key for the generic jurisdiction
        result.strings['country.-'] = unicode.encode(
            result.get('util.Generic', 'Generic'), 'utf8')
        
        return result
    
    @cherrypy.expose
    def jurisdictions(self, select=None, language='en'):

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
        for j in jurisdictions:
            country = locale.get('country.%s' % j[0],
                                 en.get('country.%s' % j[0], j[0])
                                 )
            
            yield(u'<option value="%s">%s</option>\n' % (j[1], country) )

        if select:
            yield('</select>')

    @cherrypy.expose
    def jurisdictions_js(self, select=None, language='en'):
        # set the content type
        cherrypy.response.headerMap['Content-Type'] = 'text/javascript'

        # delegate to the basic method
        for line in self.jurisdictions(select, language):
            yield("document.write('%s');\n" % line.strip())

    
