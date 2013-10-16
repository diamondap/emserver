import unittest
from tests import load_fixture
from em.libs.routers.identifier import Identifier

class IdentifierTest(unittest.TestCase):

    def setUp(self):
        self.html = load_fixture('html/router_index.html')
        self.url = 'http://192.168.1.1'
        self.port = 80
        self.headers = {'header1': 'header1_value',
                        'header2': 'header2_value',
                        'header3': 'header3_value'}

    def get_id_instance(self):
        return Identifier(html=self.html, url=self.url,
                          port=self.port, headers=self.headers)

    def test_parse_good_html(self):
        id_obj = self.get_id_instance()
        self.assertTrue(id_obj.parsing_succeeded())
        self.assertIsNone(id_obj.parse_exception)

    def test_parse_bad_html(self):
        invalid_html = 999  # integer is not valid HTML
        id_obj = Identifier(invalid_html, url=self.url,
                            port=self.port, headers=self.headers)
        self.assertFalse(id_obj.parsing_succeeded())
        self.assertIsInstance(id_obj.parse_exception, BaseException)

    def test_title(self):
        id_obj = self.get_id_instance()
        self.assertEqual("Medialink MWN-WAPR300N", id_obj.title())

    def test_links(self):
        id_obj = self.get_id_instance()
        links = ['advance.asp', 'advance.asp', 'advance.asp']
        self.assertEqual(links, id_obj.links())

    def test_forms(self):
        id_obj = self.get_id_instance()
        form = [{'name': 'basicset',
                 'method': 'post',
                 'action': '/goform/WizardHandle'}]
        self.assertEqual(form, id_obj.forms())

    def test_images(self):
        id_obj = self.get_id_instance()
        images = ['logo_420x30.jpg']
        self.assertEqual(images, id_obj.images())
