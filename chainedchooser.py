from StringIO import StringIO
import sys

import cherrypy
import cherrypy._cperror as cperror
import lxml.etree as ET

import simplejson
import support

class ChainedChooser(object):

    def __init__(self):
        pass

    @cherrypy.expose
    def index(self):
        """ Here, have a kitty. Learning exercise in CherryPy """
        return "<pre>"\
                "           _.---.._             _.---...__\n"\
                "        .-'   /\   \          .'  /\     /\n"\
                "        `.   (0 )   \        /   (0 )   /\n"\
                "          `.  \/   .'\      /`.   \/  .'\n"\
                "            ``---''   )    (   ``---''\n"\
                "                    .';.--.;`.\n"\
                "  NOTHING         .' /_...._\ `.\n"\
                "    HERE        .'   `.a  a.'   `.\n"\
                "     2         (        \/        )\n"\
                "     C          `.___..-'`-..___.'\n"\
                "                   \          /\n"\
                "                    `-.____.-'  Felix Lee &lt;flee@cse.psu.edu&gt;"\
                "</pre>"
    
    
    @cherrypy.expose    
    def chooser(self, license='by', jurisdiction='-', version=None, 
                locale='en', **kwargs):
                
        """ 
        This does nothing right now.
        The plan would be to return the form markup and a javascript include.
        Where all of the javascripting will take place is beyond me.
        
        I just wanted to offload the i18n from Django, and that is accomplished
        with the license_json method below.
        """
        # make sure this locale is supported, else fallback to en
        locale = support.actualLocale(locale)
        
        select_tag = "<select name='cc_license_%s' id='cc_license_%s_id'></select>"
        
        # i think we need to output the js first
        
        # output the select elements
        yield( select_tag % ('name','name') )
        yield( select_tag % ('jurisdiction','jurisdiction') )
        yield( select_tag % ('version','version') )
        
        # let javascript work its magic
        return
        
    @cherrypy.expose
    def licenses_json(self, exclude=None, locale='en'):
        """ Return a JSON string of all of the available licenses """
        
        tree = ET.parse(support.LICENSES_XML)
        
        # xpath queries
        lq = "//licenseclass[@id='standard']/license"
        jq = "//license[@id='%s']/jurisdiction"
        vq = "//license[@id='%s']/jurisdiction[@id='%s']/version"
       
        # ambiguous accronym/abbrev
        std_licenses = tree.xpath(lq)
        
        licenses_json_dict = dict()
        
        for l in std_licenses:
            
            result = ET.fromstring(support.issue(support.licenseCodeToAnswers(l.get('id'),None,locale)))
            
            lname = " ".join(result.xpath('//license-name')[0].text.split(" ")[:-2])
        
            licenses_json_dict[lname] = (l.get('id'), 
                
                [(j.get('id'), (j.get('id'), 
                
                    [ v.get('id') for v in tree.xpath(vq % (
                        l.get('id'), j.get('id')))]
                        
                )) for j in tree.xpath(jq % l.get('id'))]
            
            )
        
        json = simplejson.dumps(licenses_json_dict, sort_keys=True)
        
        cherrypy.response.headers['Content-Type'] = 'text/json'
        
        return json
        
        
if __name__ == '__main__':

    cherrypy.root = ChainedChooser()
    cherrypy.config.update(file='rest_api.cfg')

    cherrypy.server.start()
