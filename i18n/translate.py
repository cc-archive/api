import sys
import os
import fnmatch
import codecs

from msgfmt import make

from zope.pagetemplate.pagetemplatefile import PageTemplateFile
from zope.i18n.translationdomain import TranslationDomain
from zope.i18n.gettextmessagecatalog import GettextMessageCatalog

POFILE_DIR = '/home/nathan/Projects/iStr/i18n/'
MOFILE_DIR = '/home/nathan/Projects/iStr/'

# initialize the translation catalog
api_domain = TranslationDomain('icommons', ('en', ))


class alaZpt(PageTemplateFile):
    def pt_getContext(self, args=(), options={}, **kw):
        rval = PageTemplateFile.pt_getContext(self, args=args)
        options.update(rval)
        return options

def loadCatalogs(domain):
    langs = []
    
    def addCatalog(domain, mo_file):
        language = os.path.splitext(mo_file)[0].split('-')[-1]
        print 'loading catalog for %s...' % language
        if language == 'CVS':
            return

        domain.addCatalog(
            GettextMessageCatalog(language, 'icommons', mo_file))
        return language
        
    # check for our temporary directory; create if necessary
    tmp_path = os.path.join(os.getcwd(), '__mo')
    if not(os.path.exists(tmp_path)):
        os.mkdir(tmp_path)

    for mofile in fnmatch.filter(os.listdir(MOFILE_DIR), '*.mo'):
        langs.append(
            addCatalog(domain, os.path.join(MOFILE_DIR, mofile))
            )

    for pofile in fnmatch.filter(os.listdir(POFILE_DIR), '*.po'):
        # compile to .mo
        mo_fn = os.path.join(tmp_path, '%s.mo' % os.path.splitext(pofile)[0])
        make(os.path.join(POFILE_DIR, pofile), mo_fn)

        langs.append(
            addCatalog(domain, mo_fn)
            )

    return [n for n in langs if n is not None]
        
def lookupString(key, locale):
    return (api_domain.translate(key, target_language=locale) or
            api_domain.translate(key, target_language='en') or
            key)

if __name__ == '__main__':
    LOCALES = loadCatalogs(api_domain)
    
    in_fn = sys.argv[-1]
    out_fn = sys.argv[-1][:-3]

    template = alaZpt(in_fn)
    context = {'locales':LOCALES,
               'lookupString':lookupString,
               }
    
    #try:
    rendered = template(context=context, lookupString=lookupString)
    #except Exception, e:
    #    print 'aieee!'
    #    print e
    #    sys.exit(1)
    #else:
    print 'writing to %s..' % out_fn
    codecs.open(out_fn, 'w', 'utf8').write(rendered)
