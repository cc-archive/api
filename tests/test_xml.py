
import os
import lxml

from tests.test_common import RELAX_PATH

#######################
## Utility functions ##
#######################
def relax_validate(schema_filename, instance_filename):
    relaxng = lxml.etree.RelaxNG(lxml.etree.parse(schema_filename))
    instance = lxml.etree.parse(instance_filename)

    if not relaxng.validate(instance):
        print relaxng.error_log.last_error
        return False
    else:
        return True

####################
## Path constants ##
####################
XSL_PATH = os.path.join(os.pardir, 'license_xsl')
QUESTIONS_SCHEMA = os.path.join(RELAX_PATH, 'questions.relax.xml')
QUESTIONS_XML = os.path.join(XSL_PATH, 'questions.xml')
LICENSES_SCHEMA = os.path.join(RELAX_PATH, 'licenses.relax.xml')
LICENSES_XML = os.path.join(XSL_PATH, 'licenses.xml')

def test_questions_xml():
    """Make sure questions.xml is compliant."""
    assert relax_validate(QUESTIONS_SCHEMA, QUESTIONS_XML)

def test_licenses_xml():
    """Make sure licenses.xml is compliant."""
    assert relax_validate(LICENSES_SCHEMA, LICENSES_XML)
