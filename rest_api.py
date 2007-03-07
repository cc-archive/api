from StringIO import StringIO
import sys

import cherrypy
import cherrypy._cperror as cperror
import lxml.etree 

import support
import api_exceptions
import simplechooser
import supportapi

class LicenseClass:
    def __init__(self, classname):
	self.name = classname

    @cherrypy.expose
    def index(self, locale='en', **kwargs):

        # determine our actual functional locale
        locale = support.actualLocale(locale)
        
        doc = lxml.etree.parse(support.QUESTIONS_XML)

        license = doc.xpath('//licenseclass[@id="%s"]' % self.name)
        if len(license) > 0:
            self.license = license[0]
	    
	    # filter out the label and description tags for the
            # specified locale; fall back to English if a string isn't
            # localized
            support.pruneLocale(license[0], locale)
            return lxml.etree.tostring(license[0])
        else:
            return support.xmlError('invalidclass', 'Invalid License Class.')

    @cherrypy.expose
    def issue(self, answers=None, locale='en', **kwargs):

        # determine our actual functional locale
        locale = support.actualLocale(locale)
        
	if answers is None:
	    # return an XML error message
            return support.xmlError('missingparam',
                                    'A value must be provided for answers.')

        # attempt to issue the license, catching value errors
        try:
            # generate the answers XML document
            return support.issue(answers.decode(sys.getdefaultencoding()))
        except api_exceptions.AnswerXmlException, e:
            # mal-formed answers
            return support.xmlError(e.error_id, e.error_msg)
            
    @cherrypy.expose
    def get(self, locale='en', **kwargs):
        
        # determine our actual functional locale
        locale = support.actualLocale(locale)
        
        # generate the answers XML
        answers = "<answers><locale>%s</locale><license-%s>" % (
            locale, self.name)

        # get the list of valid fields for this license class
        fields = support.valid_fields(self.name)
        work_info = {}

        for k in kwargs:
            if k in fields:
                answers = answers + "<%s>%s</%s>" % (k, kwargs[k], k)
            else:
                work_info[k] = kwargs[k]

        str_work_info = "".join(
            ["<%s>%s</%s>" % (k, work_info[k], k) for k in work_info]
            )

        answers = answers +  "</license-%s><work-info>%s</work-info></answers>" % (self.name, str_work_info)

        # delegate to the normal issue method
        return self.issue(answers, locale)
        

class Licenses:
    @cherrypy.expose
    def default(self, l_class, action='index', **kwargs):
	# dispatch to the appropriate license class
	return getattr(LicenseClass(l_class), action)(**kwargs)

class RestApi:
    @cherrypy.expose
    def index(self, locale='en', **kwargs):

        # determine our actual functional locale
        locale = support.actualLocale(locale)
        
	# create the root level element to return
	l_classes = lxml.etree.Element('licenses')

	# use XPath to extract the license nodes from the source document
	doc = lxml.etree.parse(support.QUESTIONS_XML)

	# extract the label list
	classes = doc.xpath('//licenseclass')

	for label in classes:
	    # for each label, get the ID and add the XML to the result
	    lc = lxml.etree.SubElement(l_classes,
                                       'license',
                                       id=label.get('id'))

	    # select the appropriate locale's label, if available
            labeltext = label.xpath('label[@xml:lang="%s"]' % locale)
            if len(labeltext) > 0:
                # this label is localized
                lc.text = labeltext[0].text
            else:
                lc.text = label.xpath('label[@xml:lang="en"]')[0].text

	return lxml.etree.tostring(l_classes)

    classes=index
    classes.exposed = True

    license = Licenses()
    license.exposed = True

    @cherrypy.expose
    def details(self, locale='en', **kwargs):

        # determine the actual functional locale
        locale = support.actualLocale(locale)

        # make sure they supplied the required parameter
        if 'license-uri' not in kwargs:
           # missing parameter; return XML-encoded error
           return support.xmlError('missingparam',
                                   'A value for license-uri must be supplied.')

        license_uri = kwargs['license-uri']

        # make sure this is a valid license URI
        if not(self.validLicense(license_uri)):
            # not a valid license URI --
            # check if the trailing slash was just omitted
            if self.validLicense(license_uri + "/"):
                suggestion = license_uri + "/"
            else:
                suggestion = None
            
            # throw exception
            return support.xmlError('invalid',
                                    'Invalid license uri.',
                                    suggestion=suggestion)

        return support.license_details(license_uri, locale)
            
    @cherrypy.expose
    def locales(self, **kwargs):
        """Return a list of supported locales for i18n."""
        
	# create the root level element to return
	locales = lxml.etree.Element('locales')

        # create a sub element for each locale
        for item in support.locales():
	    # for each label, get the ID and add the XML to the result
	    lc = lxml.etree.SubElement(locales, 'locale', id=item)

        return lxml.etree.tostring(locales)

    def validLicense(self, uri, **kwargs):
        doc = lxml.etree.parse(support.LICENSES_XML)

        return doc.xpath('//version/@uri="%s"' % uri)
    
    def error(self):
        cherrypy.response.body = support.xmlError('pythonerr',
                                'Uncaught exception.',
                                sys.exc_info()
                                )
        
    def _cpOnError(self):
        """Convert uncaught errors to an XML representation."""
        try:
            raise
            #except cherrypy.NotFound:
            #    cherrypy.response.headerMap['Status'] = '404 Not Found'
            #    cherrypy.response.body = ['Page not found']
        except cherrypy.NotFound:
            cherrypy.response.body = 'foo'
            cherrypy.response.body = support.xmlError('pythonerr',
                                    'Uncaught exception.',
                                    sys.exc_info()
                                    )

def serveapi(host='localhost', port=8082):
    """Run the application using CherryPy's built-in server."""

    cherrypy.tree.mount(RestApi())
    cherrypy.tree.mount(simplechooser.SimpleChooser(), "/simple")
    cherrypy.tree.mount(supportapi.SupportApi(), "/support")
    
    #cherrypy.server.socket_host = host
    cherrypy.server.socket_port = port

    cherrypy.server.quickstart()
    cherrypy.engine.start()

def app_factory(*args):
    """Application factory for use with Python Paste deployments."""

    cherrypy.tree.mount(RestApi())
    cherrypy.tree.mount(simplechooser.SimpleChooser(), "/simple")
    cherrypy.tree.mount(supportapi.SupportApi(), "/support")

    cherrypy.engine.autoreload_match = None
    cherrypy.engine.start(blocking=False)
    
    return cherrypy.tree

if __name__ == '__main__':
    serveapi()


