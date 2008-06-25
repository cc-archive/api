
import os

from tests.test_common import *

####################
## Path constants ##
####################
RELAX_ERROR = os.path.join(RELAX_PATH, 'error.relax.xml')

##################
## Test classes ##
##################
class TestLicense(TestApi):

    def test_invalid_class(self):
        """An invalid license class name should return an explicit error."""
        res = self.app.get('/license/noclass')
        assert relax_validate(RELAX_ERROR, res.body)
