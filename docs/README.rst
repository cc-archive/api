=======================
api.creativecommons.org
=======================
-----------------------------
Creative Commons Web Services
-----------------------------

:Author: Nathan R. Yergler
:Updated: $Date$

Creative Commons provides web service APIs which can be used to integrate the Creative Commons licensing engine into third party applications. We have release a 1.0 version of the API, which is documented in the `1.0 README`_  The 1.0 API is stable, and development is occuring in CVS HEAD.  The current in-development API is described in the `Dev README`_.  These APIs are currently in beta, and we are soliciting feedback and suggestions. As such, the API may change in the future.

Sample Code
~~~~~~~~~~~
ccPublisher uses the REST interface. See class CcRest in wizard/pages/license.py for an example.

Other example usages:

* Python: The ccwsclient package provides basic abstraction of the REST interface via a Python class (`ccwsclient CVS`_).
* Java: The org.creativecommons.api package provides the CcRest class for using the REST web service from Java. Relies on JDOM and Jaxen. (`org.cc.api CVS`_, Javadoc_)

Your comments, feedback and suggestions can be sent to software@creativecommons.org.

.. _1.0 readme: readme_10.html
.. _Dev README: readme_dev.html
.. _`ccwsclient CVS`: http://cvs.sourceforge.net/viewcvs.py/cctools/api/ccwsclient/
.. _`org.cc.api CVS`: http://cvs.sourceforge.net/viewcvs.py/cctools/api_client/java/
.. _Javadoc: http://api.creativecommons.org/doc/java/
