from django.test import TestCase
from tests import load_fixture
from em.libs import utils

class UtilsTest(TestCase):

    def setUp(self):
        pass

    def test_re_first_match(self):
        regex = r' [Ff]irst '
        string1 = 'Should return the first instance of first.'
        string2 = 'Should return the First instance of first.'
        string3 = 'Will not return first, because of trailing comma.'
        self.assertEqual(" first ", utils.re_first_match(regex, string1))
        self.assertEqual(" First ", utils.re_first_match(regex, string2))
        self.assertIsNone(utils.re_first_match(regex, string3))


    def test_re_first_capture(self):
        regex = r' [Ff]i(rst) '
        string1 = 'Should return the first instance of first.'
        string2 = 'Should return the First instance of something.'
        string3 = 'Will not return first, because of trailing comma.'
        self.assertEqual("rst", utils.re_first_capture(regex, string1))
        self.assertEqual("rst", utils.re_first_capture(regex, string2))
        self.assertIsNone(utils.re_first_capture(regex, string3))
