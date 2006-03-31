=======================
api.creativecommons.org
=======================
---------------------------------
CC Web Services Documentation
---------------------------------

 :Author: Nathan R. Yergler
 :Version: 1.5
 :Updated: $Date$

.. contents:: Document Index
   :backlinks: None
   :class: docindex

This document covers the 1.5 release of CC Web Services.  
Information on the version in development can be found at 
http://api.creativecommons.org.  The 1.5 API is frozen and will not change; 
however, translations and jurisdictions will be added as they become available.

Changes Since 1.0
=================

  * /rest/dev/licenses/[class] 
      Now returns an XML fragment whose top level element is <licenseclass>, not <license>
  * /rest/dev/details
      Added details method for retrieving license details from their URI
  * /rest/dev/issue
      Now returns an additional element, ``<licenserdf>`` which contains the RDF block
      for the license only (no Work block).
  * Invalid calls now return XML-encoded error messages.
  * /locales method returns supported internationalized locales
  * All methods can return localized text.  Note that in some cases a locale
    will have a mix of English and the native language -- English is currently
    the fallback for all locales and is used in the case of partial
    translations.
  * The server has been reimplemented as a WSGI_ compliant application.
  * A test suite has been implemented for the server code.

Access Method
=============

Creative Commons Web Services 1.5 are accessible via a REST interface.  
The interface is rooted at http://api.creativecommons.org/rest/1.5.
  
Valid Calls
^^^^^^^^^^^

/locales
~~~~~~~~
  Returns an XML document detailing the available values which may be specified
  for ``locale`` in other calls.  The returned document has the following 
  format ::

    <locales>
      <locale id="en_CA"/>
      <locale id="fr"/>

      ...
    </locales>

  A future development version may include labels for the locales if users
  desire it.

/[?locale=xx]
~~~~~~~~~~~~~
  (synonym for /classes)

  Returns an XML document describing the available license classes.  A license class
  is a "family" of licenses.  Current classes are standard (basic CC licenses), 
  publicdomain, and recombo (the Sampling licenses).  
  Classes may be added at any time in the future without
  breaking 1.0 compatibility.

  A partial example of the returned document is::

     <licenses>
       <license id="standard">Creative Commons</license>
       <license id="publicdomain">Public Domain</license>
       <license id="recombo">Sampling</license>
     </licenses>

  If a value for locale is supplied, the service will attempt to return
  localized class descriptions.  If not specified, English will
  be returned.

/license/<class>[?locale=xx]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  Called with a license class id from the call above as <class>.  
  Returns an XML
  document describing the list of fields which must be supplied in 
  order to issue
  a license of the given class.

  If a value for locale is supplied, the service will attempt to return
  localized labels and descriptions.  If not specified, English will
  be returned.

  A partial example of the returned document for 
  http://api.creativecommons.org/rest/dev/license/standard ::

    <licenseclass id="standard">
     <label xml:lang="en">Creative Commons</label>
      <field id="commercial">
     <label xml:lang="en">Allow commercial uses of your work?</label>
     <description xml:lang="en">The licensor permits others to copy, distribute, display, and perform the work.  In return, the licensee may not use the work for commercial purposes, unless they get the licensor's permission.</description>
     <type>enum</type>
     <enum id="y">
       <label xml:lang="en">Yes</label>
     </enum>
     <enum id="n">
       <label xml:lang="en">No</label>
     </enum>
    </field>
    <field id="derivatives">
     <label xml:lang="en">Allows modifications of your work?</label>
     <description xml:lang="en">The licensor permits others to copy, distribute and perform only unaltered copies of the work, not derivative works based on it.</description>
     <type>enum</type>
     <enum id="y">
       <label xml:lang="en">Yes</label>
     </enum>
     <enum id="sa">
       <label xml:lang="en">ShareAlike</label>
     </enum>
     <enum id="n">
       <label xml:lang="en">No</label>
     </enum>
    </field>
    <field id="jurisdiction">
     <label xml:lang="en">Jurisdiction of your license:</label>
     <description xml:lang="en">If you desire a license governed by the Copyright Law of a specific jurisdiction, please select the appropriate jurisdiction.</description>
     <type>enum</type>
     <enum id="">
       <label xml:lang="en">Generic</label>
     </enum>
     <enum id="at">
       <label xml:lang="en">Austria</label>
     </enum>
    </field>
   </licenseclass>


  Note that a given field or enum element may have more than one label, so long as they
  have unique xml:lang attributes.  Future language translations may be added at any time
  in the future without breaking 1.0 compatibility.

/license/<class>/issue
~~~~~~~~~~~~~~~~~~~~~~

  Called with an HTTP POST whose contents are a single form variable, 
  ``answers``. 
  The value of answers is an XML string containing values which match 
  each ``field``
  element found in the earlier license/[class] call.  A sample answers 
  string for the 
  previous example is::

    <answers>
      <locale>en</locale>
      <license-standard>
        <commercial>n</commercial>
        <derivatives>y</derivatives>
        <jurisdiction></jurisdiction>
      </license-standard>
    </answers>

  This example would issue a by-nc license in the generic (default) 
  jurisdiction.  Note
  each element name matches a field id, and the content of the 
  elements match the 
  enum id for the selected choice.  The <license-standard> tag is the
  license class prepended with ``license-``.

  The ``<locale>`` element is optional.  If supplied, the license name returned
  will be localized to the selected locale.  If omitted, English will be
  used.  

  The issue method uses the chooselicense.xsl document to generate the 
  resulting XML 
  document.  The result of this sample call would be an XML document, such as::

    <?xml version="1.0"?>

    <result>
      <license-uri>http://creativecommons.org/licenses/by/2.0/Generic/</license-uri>
      <license-name>Attribution 2.0</license-name>
      <rdf>
        <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns="http://web.resource.org/cc/" xmlns:dc="http://purl.org/dc/elements/1.1/">
          <Work rdf:about="">
            <license rdf:resource="http://creativecommons.org/licenses/by/2.0/Generic/"/>
          </Work>
          <License rdf:about="http://creativecommons.org/licenses/by/2.0/Generic/">
            <permits rdf:resource="http://web.resource.org/cc/Reproduction"/>
            <permits rdf:resource="http://web.resource.org/cc/Distribution"/>
            <requires rdf:resource="http://web.resource.org/cc/Notice"/>
            <requires rdf:resource="http://web.resource.org/cc/Attribution"/>
            <permits rdf:resource="http://web.resource.org/cc/DerivativeWorks"/>
          </License>
        </rdf:RDF>
      </rdf>
      <licenserdf>
        <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns="http://web.resource.org/cc/" xmlns:dc="http://purl.org/dc/elements/1.1/">
          <License rdf:about="http://creativecommons.org/licenses/by/2.0/Generic/">
            <permits rdf:resource="http://web.resource.org/cc/Reproduction"/>
            <permits rdf:resource="http://web.resource.org/cc/Distribution"/>
            <requires rdf:resource="http://web.resource.org/cc/Notice"/>
            <requires rdf:resource="http://web.resource.org/cc/Attribution"/>
            <permits rdf:resource="http://web.resource.org/cc/DerivativeWorks"/>
          </License>
        </rdf:RDF>
      </licenserdf>
      <html><!--Creative Commons License-->
          <a rel="license" href="http://creativecommons.org/licenses/by/2.0/Generic/">
          <img alt="Creative Commons License" border="0" src="http://creativecommons.org/images/public/somerights20.gif"/></a><br/>
		This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/2.0/Generic/">Creative Commons License</a>.
		<!--/Creative Commons License--><!-- <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns="http://web.resource.org/cc/" xmlns:dc="http://purl.org/dc/elements/1.1/"><Work rdf:about=""><license rdf:resource="http://creativecommons.org/licenses/by/2.0/Generic/"/></Work><License rdf:about="http://creativecommons.org/licenses/by/2.0/Generic/"><permits rdf:resource="http://web.resource.org/cc/Reproduction"/><permits rdf:resource="http://web.resource.org/cc/Distribution"/><requires rdf:resource="http://web.resource.org/cc/Notice"/><requires rdf:resource="http://web.resource.org/cc/Attribution"/><permits rdf:resource="http://web.resource.org/cc/DerivativeWorks"/></License></rdf:RDF> --></html>
    </result>
        
  Note the <html> element contains the entire RDF-in-comment which the standard CC license
  engine returns.

/details?license-uri=[uri]
~~~~~~~~~~~~~~~~~~~~~~~~~~

  Called with an HTTP POST or GET with a single form variable, 
  ``license-uri``.  The
  value of license-uri is the URI of an existing Creative Commons license.  
  The call returns the same result as issue.  Note that at this time
  ``details`` does not support localization.


Error Handling
==============

 Errors occuring from either invalid input or server-side problems are 
 returned as an XML block, with an ``<error>`` top level element.  For 
 example, a call to details with no ``license-uri`` would return the following
 text::

   <error>
     <id>missingparam</id>
     <message>A value for license-uri must be supplied.</message>
   </error>

 Error messages are currently not localized.

 If the error occurs due to a server side error, two additional elements
 may be specified: ``<exception>`` and ``<traceback>``.  
 ``<traceback>`` will contain
 the text of the Python stack trace.  This is usually uninteresting for
 end users, but may help developers when reporting errors.

 ``<exception>`` contains the Python exception information.  
 A contrived example::

   <exception type="KeyError">
     Unknown Key.
   </exception>

 Note that the actual contents of the ``<exception>`` element is dependent
 on the actual error that occurs; these will only be returned when an 
 otherwise unhandled error has occured.


Currently Defined Errors
^^^^^^^^^^^^^^^^^^^^^^^^

 ============== ==================================================
   id            description
 ============== ==================================================
 missingparam    A required parameter is missing; for convenience
                 the web service
                 will check both GET and POST for form values.
 invalidclass    An unknown license class was specified in the URL.
 pythonerr       A Python exception has occured.
 ============== ==================================================

Additional Resources
====================

 * The Creative Commons developer mailing list, cc-devel; information available
   at http://lists.ibiblio.org/mailman/listinfo/cc-devel
 * `Creative Commons Developer Wiki`_ 

.. _WSGI: http://www.python.org/peps/pep-0333.html
.. _`Creative Commons Developer Wiki`: http://wiki.creativecommons.org/wiki/Developer