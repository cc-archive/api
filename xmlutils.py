"""
$Header$
"""

import sys, time, feedparser, logging, pickle, traceback, libxml2, libxslt
from datetime import datetime, timedelta

from xml.sax import saxutils, make_parser, SAXParseException
from xml.sax.handler import feature_namespaces, feature_namespace_prefixes
from xml.sax import saxutils
from xml.sax.xmlreader import AttributesImpl
from StringIO import StringIO
import xml.sax._exceptions
import xml.sax.handler

global log, namespaces
log = logging.getLogger("%s"%__name__)

INDENT = '  '
ATOM_VERSION = '0.3'

namespaces = {}
# HACK: Borrow feedparser's top secret list of namespaces
try:
    # Copy a key/value-inverted version of feedparser's namespaces
    from feedparser import _FeedParserMixin
    namespaces.update(dict([(v,k) for k,v in 
                            _FeedParserMixin.namespaces.items()]))

    # Selectively delete troublesome namespace prefixes
    del namespaces['']
    del namespaces['rdf']
    
except ImportError:
    log.warn("HACK to borrow feedparser namespaces failed")

class XPathDict:
    namespaces=namespaces

    def __init__(self, doc=None, xml=None, file=None, node=None):
        self.ctxt = None

        self.free_doc = True
        if xml:    
            self.doc = libxml2.parseDoc(xml)
        elif file: self.doc = libxml2.parseFile(file)
        else:    
            self.doc      = doc
            self.free_doc = False

        ctxt = self.doc.xpathNewContext()
        ctxt.xpathRegisterNs('',       'http://purl.org/atom/ns#')
        ctxt.xpathRegisterNs('dbagg3', 'http://decafbad.com/2004/07/dbagg3/')
        ctxt.xpathRegisterNs('atom',   'http://purl.org/atom/ns#')
        ctxt.xpathRegisterNs('a',      'http://purl.org/atom/ns#')
        for k,v in self.namespaces.items():
            ctxt.xpathRegisterNs(k,v)

        self.ctxt = ctxt

        if node is not None:
            self.root = node
        else:
            self.root = self.doc.getRootElement()

        self.ctxt.setContextNode(node)

    def __del__(self):
        if self.ctxt: 
            self.ctxt.xpathFreeContext()
        if self.doc and self.free_doc: 
            self.doc.freeDoc()

    def __getitem__(self, xpath):
        try:
            return self.nodes(xpath)[0].content
        except:
            return None

    def __delitem__(self, xpath):
        nodes = self.nodes(xpath)
        for n in nodes:
            n.unlinkNode()
            n.freeNode()

    def __contains__(self, xpath):
        rs = self.nodes(xpath)
        return rs is not None and len(rs)>0

    def get(self, key, default=None):
        return self.__getitem__(self, key, default)

    def has_key(self, key):
        return self.__contains__(key)

    def nodes(self, xpath):
        return self.ctxt.xpathEval(xpath)

    def xpnodes(self, xpath):
        return [XPathDict(doc=self.doc, node=n) for n in self.nodes(xpath)]
    
    def cd(self, xpath=None, node=None):
        if node is None:
            node = self.ctxt.xpathEval(xpath)[0]
        self.root = node
        self.ctxt.setContextNode(node)

    def xml(self):
        return self.root.serialize(format=1)

    def tuple_extract(self, extract_keys, extract_xml=False):
        data = dict([(k, self[p]) for k,p in extract_keys \
                     if self.has_key(p)])
        if extract_xml:
            data['xml'] = self.doc.serialize()

        data = tuple([(n, data[n]) for n in data])
        return data

    def extract(self, extract_keys, extract_xml=False):
        return dict(tuple_extract(extract_keys, extract_xml))

class XMLGenerator(saxutils.XMLGenerator):

    INDENT=INDENT
    ATOM_VERSION=ATOM_VERSION
    namespaces=namespaces

    def __init__(self, encoding=None, stream=None, base_href='http://localhost'):
        if encoding == None: encoding = 'utf-8'
        if stream   == None: stream   = sys.stdout

        saxutils.XMLGenerator.__init__(self, stream, encoding=encoding)
        self.base_href = base_href
        self.encoding  = encoding
        self.reset()

    def reset(self):
        self._indent = 0
        self._emitted_NS = False

    def omitNS(self):
        self._emitted_NS = True

    def setNS(self, ns):
        self.namespaces = ns
        
    def doIndent(self):
        for x in range(self._indent): 
            self.characters(self.INDENT)

    def elemStart(self, name, attr={}):
        self.doIndent()
        
        if not self._emitted_NS:
            ns_attr = {
                'xml:base'     : self.base_href,
                'xmlns'        : 'http://purl.org/atom/ns#',
                'xmlns:dbagg3' : 'http://decafbad.com/2004/07/dbagg3/',
                'xmlns:xlink'  : 'http://www.w3.org/1999/xlink'
                }
            for k,v in self.namespaces.items(): 
                ns_attr['xmlns:%s'%k]=v
            ns_attr.update(attr)
            attr = ns_attr
            self._emitted_NS = True
            
        self.startElement(name, AttributesImpl(attr))
        self.characters('\n')
        self._indent += 1

    def elemEnd(self, name):
        self._indent -= 1
        self.doIndent()
        self.endElement(name)
        self.characters('\n')
    
    def elemWithContent(self, name, content, attr={}):
        self.doIndent()
        attr = dict( map( lambda k: (k, attr[k].encode(self.encoding, 'xmlcharrefreplace')), attr.keys() ) )
        self.startElement(name, AttributesImpl(attr))
        if content is not None:
            self.characters(content.encode(self.encoding, 'xmlcharrefreplace'))
        self.endElement(name)
        self.characters('\n')

    def linkBuild(self, rel, href, type, title):
        attr = { 'rel'   : rel,
                 'href'  : href,
                 'type'  : type,
                 'title' : title }
        self.elemWithContent('link', None, attr=attr)
