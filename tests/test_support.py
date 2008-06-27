
import os

from tests.test_common import *

####################
## Path constants ##
####################
RELAX_OPTIONS = os.path.join(RELAX_PATH, 'options.relax.xml')

##################
## Test classes ##
##################
class TestSupport(TestApi):

    def test_support_jurisdictions(self):
        """/support/jurisdictions served properly."""
        res = self.app.get('/support/jurisdictions') 
        body = res.body.replace('&', '&amp;') # makes the xml parser choke
        body = '<root>' + body + '</root>' # b/c it's not valid xml
        assert relax_validate(RELAX_OPTIONS, body)

    def test_javascript(self):
        """Test javascript wrapper over /support/jurisdictions."""
        res = self.app.get('/support/jurisdictions')
        jsres = self.app.get('/support/jurisdictions.js')
        opts = res.body.strip().split('\n')
        jsopts = jsres.body.strip().split('\n')
        assert len(opts) == len(jsopts)
        for i in range(len(opts)):
            assert "document.write('%s');" % opts[i] == jsopts[i]
