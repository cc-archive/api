"""
translate.py

Pass one or more template files through a TAL parser with some simple
locale look-up functions in the context for straightforward i18n expansion.

Copyright 2005, Nathan R. Yergler, Creative Commons
Licensed to the public under the GNU GPL version 2.

Sample Usages:
--------------

translate.py --cvs template.xml.in

   Checks out .po files from CVS and passes template.xml.in through the
   parser, generating template.xml.

translate.py --podir ../pofiles -o .. template.xml.in

   Reads .po files from ../pofiles/ and generates template.xml in the parent
   directory (..).

"""

__version__ = "$Revision$"

import sys
import os
import fnmatch
import tempfile
import subprocess
import optparse
import re

from simpletal import simpleTAL, simpleTALES

CVSROOT = ":pserver:anonymous@cvs.sf.net:/cvsroot/cctools"
CVSMODULE = "zope/iStr/i18n"

POFILE_DIR = '/home/nathan/Projects/iStr/i18n/'

class CvsWrapper(object):
    def __init__(self, root, module):
        """Create a new wrapper on a CVS connection.
        @param root The CVSROOT for the module, specified with the same format
                    as -d to cvs.  For example:
                    :pserver:anonymous@cvs.sf.net:/cvsroot/cctools
        @param module The CVS module to checkout.
        """
        
        self.__root = root
        self.__module = module

        self.__codir = None
        
    def co(self):
        """Checkout the module to a directory in the temporary folder."""
        target = self.__module.split('/')[-1]
        targetdir = tempfile.gettempdir()

        CVS_CMD_LINE = "cvs -d%s login; cvs -d%s co -d %s %s" % (
            self.__root, self.__root, target, self.__module)
        
        cvs = subprocess.Popen(CVS_CMD_LINE, cwd=targetdir, shell=True)
        cvs.wait()

        self.__codir = os.path.join(targetdir, target)
        return self.__codir
    
    def listFiles(self):
        """Returns a sequence of files checked out from the module.
        Each entry is the fully qualified path name.  The module is checked
        out from CVS into a temporary directory."""
        
        if self.__codir is None:
            # need to checkout the module
            self.__codir = self.co()

        return [os.path.join(self.__codir, n) for n in 
                os.listdir(self.__codir)]
    
    def release(self):
        """Release our checked out copy by removing the files."""

        if self.__codir is not None:
            os.path.rmdir(self.__codir)
        
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
        
def lookupString(key, locale):
    global LOCALES
    
    result = LOCALES[locale].get(key, None) or \
             LOCALES['en'].get(key, None) or \
             key

    return result

def loadCatalogs(source_dir):
    """Load the translation catalogs and return a dictionary mapping
    the locale code to the PoFile object."""

    langs = {}
    
    for pofile in fnmatch.filter(os.listdir(source_dir), '*.po'):
        language = os.path.splitext(pofile)[0].split('-')[-1]

        if language == 'CVS':
            continue
        
        print 'loading catalog for %s...' % os.path.basename(pofile)
        langs[language] = PoFile(os.path.join(source_dir, pofile))

    return langs

def loadOpts():
    """Parse command line options; returns a tuple of (opts, args)."""
    parser = optparse.OptionParser(usage="%prog [--cvs|--podir podir] files",
                                   version="%%prog %s" % __version__)

    parser.add_option('--podir', dest='podir',
                     help='Directory containing .po translation files.')
    parser.add_option('--cvs', dest='cvs', action='store_true',
                     help='Checkout .po translations from CVS.')
    parser.add_option('-o', '--output', dest='outputDir',
                      help='Save output files to specified directory'
                      '(defaults to the same directory as input files).')
    parser.set_defaults(cvs=False)
    
    return parser.parse_args()
    
if __name__ == '__main__':
    global LOCALES

    # parse command line parameters and check for sanity
    (opts, args) = loadOpts()
    if (not(opts.cvs)) and (getattr(opts, 'podir', None) is None):
        print >> sys.stderr, "You must specify either --podir or --cvs."
        sys.exit(1)

    # do the CVS checkout if necessary
    if (opts.cvs):
        langsource = CvsWrapper(CVSROOT, CVSMODULE)
        opts.podir = langsource.co()
        
    # load the catalogs
    LOCALES = loadCatalogs(opts.podir)

    # determine our output directory
    output_dir = getattr(opts, 'outputDir', None)

    # set up our TAL context
    context = simpleTALES.Context(allowPythonPath=1)
    context.addGlobal ("locales", LOCALES.keys())
    context.addGlobal ("lookupString", lookupString)

    # iterate over the specified
    for in_fn in args:
        if output_dir is None:
            # just output to the same directory
            out_fn = in_fn[:-3]
        else:
            out_fn = os.path.join(output_dir, os.path.basename(in_fn)[:-3])

        template = simpleTAL.compileXMLTemplate (open (in_fn, 'r'))
        output = file(out_fn, 'w')

        print 'writing to %s..' % out_fn
        template.expand (context, output, 'utf8')

