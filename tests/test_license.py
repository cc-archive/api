
import os

from tests.test_common import *

####################
## Path constants ##
####################
RELAX_ERROR = os.path.join(RELAX_PATH, 'error.relax.xml')
RELAX_LICENSECLASS = os.path.join(RELAX_PATH, 'licenseclass.relax.xml')
RELAX_ISSUE = os.path.join(RELAX_PATH, 'issue.relax.xml')

##################
## Test classes ##
##################
class TestLicense(TestApi):

    def test_invalid_class(self):
        """An invalid license class name should return an explicit error."""
        res = self.app.get('/license/noclass')
        assert relax_validate(RELAX_ERROR, res.body)

    def test_license_class_structure(self):
        """Test that each license class returns a valid XML chunk."""
        for lclass in self.data.license_classes():
            res = self.app.get('/license/%s' % lclass)
            assert relax_validate(RELAX_LICENSECLASS, res.body)

    def test_issue_invalid_class(self):
        """/issue should return an error with an invalid class."""
        res = self.app.get('/license/blarf/issue?answers=<foo/>')
        assert relax_validate(RELAX_ERROR, res.body)

    def test_get_invalid_class(self):
        """/get should return an error with an invalid class."""
        res = self.app.get('/license/%s/get' % hash(self))
        assert relax_validate(RELAX_ERROR, res.body)

    def test_issue_error(self):
        """Issue with no answers or empty answers should return an error."""
        res = self.app.get('/license/blarf/issue?answers=<foo/>')
        assert relax_validate(RELAX_ERROR, res.body)

class TestFailure(TestApi):

    def test_get_extra_args(self):
        """Test /get ignores extra nonsense arguments."""
        for lclass in self.data.license_classes():
            for query_string in self.data.query_string_answers(lclass):
                res = self.app.get('/license/%s/get%s&foo=bar' %
                                         (lclass, query_string))
                assert relax_validate(RELAX_ISSUE, res.body)

    def test_issue(self):
        """/issue issues every license class successfully."""
        for lclass in self.data.license_classes():
            for answers in self.data.xml_answers(lclass):
                res = self.app.get('/license/%s/issue?answers=%s' %
                                         (lclass, answers))
                assert relax_validate(RELAX_ISSUE, res.body)

    def test_get(self):
        """/get issues every license class successfully."""
        for lclass in self.data.license_classes():
            for query_string in self.data.query_string_answers(lclass):
                res = self.app.get('/license/%s/get%s' %
                                         (lclass, query_string))
                assert relax_validate(RELAX_ISSUE, res.body)
