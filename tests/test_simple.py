
import os

from tests.test_common import *

####################
## Path constants ##
####################
RELAX_SIMPLECHOOSER = os.path.join(RELAX_PATH, 'simplechooser.relax.xml')

##################
## Test classes ##
##################
class TestChooser(TestApi):

    def test_simple_chooser(self):
        """/simple/chooser served properly."""
        res = self.app.get('/simple/chooser') 
        body = '<root>' + res.body + '</root>' # b/c it's not valid xml
        assert relax_validate(RELAX_SIMPLECHOOSER, body)

    def test_javascript(self):
        """Test javascript wrapper over /simple/chooser."""
        res = self.app.get('/simple/chooser')
        jsres = self.app.get('/simple/chooser.js')
        opts = res.body.strip().split('\n')
        jsopts = jsres.body.strip().split('\n')
        assert len(opts) == len(jsopts)
        for i in range(len(opts)):
            assert "document.write('%s');" % opts[i] == jsopts[i]
