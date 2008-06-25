
import lxml
from StringIO import StringIO
import os

####################
## Path constants ##
####################
RELAX_PATH = 'schemata'
if not os.path.exists(RELAX_PATH):
    RELAX_PATH = os.path.join('tests', 'schemata')

#######################
## Utility functions ##
#######################
def relax_validate(schema_filename, instance_buffer):
    relaxng = lxml.etree.RelaxNG(lxml.etree.parse(schema_filename))
    instance = lxml.etree.parse(StringIO(instance_buffer))

    if not relaxng.validate(instance):
        print relaxng.error_log.last_error
        return False
    else:
        return True
