
import os

from tests.test_common import *

####################
## Path constants ##
####################
RELAX_ERROR = os.path.join(RELAX_PATH, 'error.relax.xml')

##################
## Test classes ##
##################
class TestChooser(TestApi):

    def test_javascript(self):
        """Test javascript wrapper over /simple/chooser."""
        res = self.app.get('/simple/chooser')
        jsres = self.app.get('/simple/chooser.js')
        opts = res.body.strip().split('\n')
        jsopts = jsres.body.strip().split('\n')
        assert len(opts) == len(jsopts)
        for i in range(len(opts)):
            assert "document.write('%s');" % opts[i] == jsopts[i]
