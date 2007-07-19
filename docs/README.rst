=======================
api.creativecommons.org
=======================
-----------------------------
Creative Commons Web Services
-----------------------------

:Author: Nathan R. Yergler
:Updated: $Date$

Creative Commons provides web service APIs which can be used to integrate 
the Creative Commons licensing engine into third party applications. 
We have release the 1.5 version of the API, which is documented in the 
`1.5 README`_  The 1.5 API is stable, and development is occuring in 
CVS HEAD.  

The current in-development API is described in the 
`Dev README`_.  These APIs are currently in beta, and we are soliciting 
feedback and suggestions. As such, the API may change in the future.

The Previous Releases are still supported by the server at their 
canonical URIs.

Sample Code
~~~~~~~~~~~
ccPublisher uses the REST interface. See class CcRest in wizard/pages/license.py for an example.

Other example usages:

* Python: The ccwsclient package provides basic abstraction of the REST interface via a Python class (`ccwsclient SVN`_).
* Java: The org.creativecommons.api package provides the CcRest class for using the REST web service from Java. Relies on JDOM and Jaxen. (`org.cc.api SVN`_)

Your comments, feedback and suggestions can be sent to software@creativecommons.org.

Revision History
~~~~~~~~~~~~~~~~~
 * 19 July 2007: Updated links.
 * 30 August 2005: 1.5 (`1.5 readme`_)
 * 2005 1.0 (`1.0 readme`_)

.. _1.0 readme: readme_10.html
.. _1.5 readme: readme_15.html
.. _Dev README: readme_dev.html
.. _`ccwsclient SVN`: http://cctools.svn.sourceforge.net/viewvc/cctools/api_client/trunk/python/ccwsclient/
.. _`org.cc.api SVN`: http://cctools.svn.sourceforge.net/viewvc/cctools/api_client/trunk/java/
