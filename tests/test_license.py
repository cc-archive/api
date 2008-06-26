
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


class TestLicenseIssue(TestApi):

    def test_issue_invalid_class(self):
        """/issue should return an error with an invalid class."""
        res = self.app.get('/license/blarf/issue?answers=<foo/>')
        assert relax_validate(RELAX_ERROR, res.body)

    def test_issue_error(self):
        """Issue with no answers or empty answers should return an error."""
        res = self.app.get('/license/blarf/issue?answers=<foo/>')
        assert relax_validate(RELAX_ERROR, res.body)

    def _issue(self, lclass):
        """Common /issue testing code."""
        for answers in self.data.xml_answers(lclass):
            res = self.app.get('/license/%s/issue?answers=%s' % 
                                      (lclass, answers))
            print 'lclass: %s' % lclass
            print 'answers: %s' % answers
            print
            assert relax_validate(RELAX_ISSUE, res.body)

    def test_issue_license_standard(self):
        """/issue issues standard licenses successfully."""
        self._issue('standard')

    def test_issue_license_publicdomain(self):
        """/issue issues publicdomain licenses successfully."""
        self._issue('publicdomain')

    def test_issue_license_recombo(self):
        """/issue issues recombo licenses successfully."""
        self._issue('recombo')


class TestLicenseGet(TestApi):

    def test_get_invalid_class(self):
        """/get should return an error with an invalid class."""
        res = self.app.get('/license/%s/get' % hash(self))
        assert relax_validate(RELAX_ERROR, res.body)

    def test_get_extra_args(self):
        """Test /get ignores extra nonsense arguments."""
        for lclass in self.data.license_classes():
            for query_string in self.data.query_string_answers(lclass):
                res = self.app.get('/license/%s/get%s&foo=bar' %
                                         (lclass, query_string))
                assert relax_validate(RELAX_ISSUE, res.body)

    def _get(self, lclass):
        """Common /get testing code."""
        for query_string in self.data.query_string_answers(lclass):
            res = self.app.get('/license/%s/get%s' %
                                     (lclass, query_string))
            print 'lclass: %s' % lclass
            print 'query_string: %s' % query_string
            print
            assert relax_validate(RELAX_ISSUE, res.body)

    def test_get_license_standard(self):
        """/get issues standard licenses successfully."""
        self._get('standard')

    def test_get_license_publicdomain(self):
        """/get issues publicdomain licenses successfully."""
        self._get('publicdomain')

    def test_get_license_recombo(self):
        """/get issues recombo licenses successfully."""
        self._get('recombo')
