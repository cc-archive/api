=======================
api.creativecommons.org
=======================
---------------------------------
CC Web Services Documentation
---------------------------------

 :Author: Nathan R. Yergler
 :Version: 2.0-candidate (CVS HEAD)
 :Updated: $Date$

.. contents:: Document Index
   :backlinks: None
   :class: docindex

This document covers the current development release of CC Web Services.  
This should be considered unstable and only used for application testing 
and development.  Production applications should use the current stable 
version, as the development API can and will change.  Information on the 
curent version can be found at http://api.creativecommons.org.


Changes Since 1.5
=================

  * /rest/dev/details
      Added validation for the specified license URI; returns error 
      block if invalid
  * /simple/chooser
      The ``language`` parameter is no longer supported; use ``locale`` 
      instead.
  * /support/jurisdictions
      The ``language`` parameter is no longer supported; use ``locale`` 
      instead.

Access Method
=============

The Creative Commons Web Services are accessible via a REST interface.  
The interface is rooted at http://api.creativecommons.org/rest/dev.
  
Valid Calls
===========

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
  elements matches the 
  enum id for the selected choice.  Only values specified as the ``id``
  attribute for ``enum`` elements are accepted as values for each field.
  If other values are specified, the server will return an ``invalidanswer``
  error.
  
  The <license-standard> tag is the license class prepended with ``license-``.

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

  The information passed to the licensing web service may be augmented with
  optional information about the work to be licensed.  If included this 
  information will be included in the returned RDF and RDF-in-comment.  For
  example::

    <answers>
      <locale>en</locale>
      <license-standard>
        <commercial>n</commercial>
        <derivatives>y</derivatives>
        <jurisdiction></jurisdiction>
      </license-standard>
      <work-info>
        <title>The Title</title>
	<work-url>http://example.com/work</work-url>
	<source-url>http://example.com/source</source-url>
	<type>Text</type>
	<year>2006</year>
	<description>A brief description...</description>
	<creator>John Q. Public</creator>
	<holder>John Q. Public</holder>
      </work-info>
    </answers>

  All work-info sub-elements are optional.

/license/<class>/get?
~~~~~~~~~~~~~~~~~~~~~

  Called with an HTTP GET and a query string containing a parameter for each
  ``field`` specified in the previous call to /license/<class>.  The value
  of each parameter should match one of the enum values provided.

  For example, a call to retrieve a Creative Commons standard license might
  look like:

  /license/standard/get?commercial=n&derivatives=y&jurisdiction=

  This example would issue a by-nc license in the generic (default) 
  jurisdiction.  Note each element name matches a field id, and the 
  content of the elements match the enum id for the selected choice.  Only
  those values specified as ``enum`` element ``id`` attributes are accepted
  as values for each parameter.

  The XML returned from this call is identical to the return from 
  /license/<class>/issue (see above).

  A locale parameter may also be specified.  If supplied, the license 
  name returned will be localized to the selected locale.  If omitted, 
  English will be used.  

/details?license-uri=[uri]
~~~~~~~~~~~~~~~~~~~~~~~~~~

  Called with an HTTP POST or GET with a single form variable, 
  ``license-uri``.  The
  value of license-uri is the URI of an existing Creative Commons license.  
  The call returns the same result as issue.  Note that at this time
  ``details`` does not support localization.

  If the uri specified by ``license-uri`` is not a valid Creative Commons 
  license, the web service will reject the request and return an error block.
  For example, ::

    <error>
      <id>invalid</id>
      <message>Invalid license uri.</message>
    </error>


/simple/chooser
~~~~~~~~~~~~~~~

  Returns a simple license chooser in the form of an HTML-drop down.  The
  format of the returned chooser can be customized with the following 
  parameters

  ============== ========= ==============================================
  Name           Number    Description
  ============== ========= ==============================================
  jurisdiction   0 or 1    Returns licenses for the specified 
                           jurisdiction.  Example: de
  exclude        0 or more Excludes license urls containing the specified
                           string.  Example: nc will exclude 
                           NonCommercial licenses.
  locale         0 or 1    Locale to use for license names; defaults to
                           English (en).  Example: ja
  select         0 or 1    If specified, the value used for the name 
                           attribute of the <select> element; if not 
                           specified, the select element is omitted.
  ============== ========= ==============================================

  In addition to these parameters, the Simple Chooser can be further 
  customized by invoking as either /simple/chooser or /simple/chooser.js.
  If invoked as the former, the result is raw HTML.  If invoked as the
  latter, the result is wrapped in document.write() calls.

/support/jurisdictions
~~~~~~~~~~~~~~~~~~~~~~

  Returns a simple jurisdiction chooser in the form of an HTML drop-down. The
  format of the returned chooser can be customized with the following 
  parameters

  ============== ========= ==============================================
  Name           Number    Description
  ============== ========= ==============================================
  locale         0 or 1    Locale to use for license names; defaults to
                           English (en).  Example: ja
  select         0 or 1    If specified, the value used for the name 
                           attribute of the <select> element; if not 
                           specified, the select element is omitted.
  ============== ========= ==============================================

  In addition to these parameters, the dropdown call can be further 
  customized by invoking as either /support/jurisdictions or 
  /support/jurisdictions.js.
  If invoked as the former, the result is raw HTML.  If invoked as the
  latter, the result is wrapped in document.write() calls.

 
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
~~~~~~~~~~~~~~~~~~~~~~~~

 ============== ==================================================
   id            description
 ============== ==================================================
 missingparam    A required parameter is missing; for convenience
                 the web service
                 will check both GET and POST for form values.
 invalidclass    Returned when details are requested for an 
                 invalid license class.  For example, calling
                 ``/license/blarf`` will return this error code.
 pythonerr       A Python exception has occured.
 invalidanswer   Returned when a value passed into issue or get
                 for a field (question) is not a valid value.
 ============== ==================================================

Additional Resources
====================

 * The Creative Commons developer mailing list, cc-devel; information available
   at http://lists.ibiblio.org/mailman/listinfo/cc-devel
 * `Creative Commons Developer Wiki`_ 
 * `CC Web Services in the Wiki`_

.. _`Creative Commons Developer Wiki`: http://wiki.creativecommons.org/Developer.. _`CC Web Services in the Wiki`: http://wiki.creativecommons.org/Creative_Commons_Web_Services