# chooselicense-xml unit test
# 10 Feb 2005
# Nathan R. Yergler

import sys
import lxml.etree
import unittest


def RelaxValidate(schemaFileName, instanceFileName):

    relaxng = lxml.etree.RelaxNG(lxml.etree.parse(schemaFileName))
    instance = lxml.etree.parse(instanceFileName)

    return relaxng.validate(instance)
    
if __name__ == '__main__':
    # make sure the appropriate arguments were passed in
    if len(sys.argv) != 3:
        # wrong args; print usage message and exist
        print
        print "usage: relax.py [schema_file] [xml_file]"
        print
        sys.exit(1)

    result = RelaxValidate(sys.argv[1], sys.argv[2])
    if result != 1:
        print "%s does not conform (one day this will be a better error message)" % sys.argv[2]
    else:
        print "%s conforms to specified schema, %s." % (
            sys.argv[2], sys.argv[1])
    

    print
    
