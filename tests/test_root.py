
import os

from tests.test_common import *

####################
## Path constants ##
####################
RELAX_CLASSES = os.path.join(RELAX_PATH, 'classes.relax.xml')

##################
## Test classes ##
##################
class TestRoot(TestApi):

    def test_synonyms(self):
        """Test that /classes and / are synonyms."""
        root = self.app.get('/').body
        classes = self.app.get('/').body
        assert root == classes

    def test_classes_structure(self):
        """Test the return values of /classes."""
        res = self.app.get('/classes')
        assert relax_validate(RELAX_CLASSES, res.body)

