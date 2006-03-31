# chooselicense-xml unit test
# 10 Feb 2005
# Nathan R. Yergler

import sys
import libxml2
import unittest

def callback(ctx, str):
    print '---'
    print ctx, str
    
    #global log
    #log.write("%s%s" % (ctx, str))

libxml2.debugMemory(1)
libxml2.lineNumbersDefault(1)

#libxml2.registerErrorHandler(callback, "")


def fileRead(filename, attrib):
    myFile = open(filename, attrib)
    contents = myFile.read()
    myFile.close()
    return contents


def isValid(schemaFileName, instanceFileName):
    success = False
    schema = fileRead(schemaFileName, 'r')
    instance = fileRead(instanceFileName, 'r')
    rngParser = libxml2.relaxNGNewMemParserCtxt(schema, len(schema))
    rngSchema = rngParser.relaxNGParse()
    ctxt = rngSchema.relaxNGNewValidCtxt()
    doc = libxml2.parseDoc(instance)
    ret = doc.relaxNGValidateDoc(ctxt)
    
    if ret == 0:
        success = True
    # Validation completed, let's clean up
    doc.freeDoc()
    del rngParser, rngSchema, ctxt
    libxml2.relaxNGCleanupTypes()
    libxml2.cleanupParser()
    if libxml2.debugMemory(1) != 0:
        print "Memory leaked %d bytes" % libxml2.debugMemory(1)
        libxml2.dumpMemory()
    return success
    
if __name__ == '__main__':
    isValid(sys.argv[-2], sys.argv[-1])
    
