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
        links = [{'href': 'advance.asp',
                  'text': 'document.write(_("Advanced Settings"));'},
                 {'href': 'advance.asp',
                  'text': 'document.write(_("Advanced Settings"))'},
                 {'href': 'advance.asp',
                  'text': 'document.write(_("Advanced Settings"))'},]
        self.assertEqual(links, id_obj.links())

    def test_form_attrs(self):
        id_obj = self.get_id_instance()
        form = [{'name': 'basicset',
                 'method': 'post',
                 'action': '/goform/WizardHandle'}]
        self.assertEqual(form, id_obj.form_attrs())

    def test_images(self):
        id_obj = self.get_id_instance()
        images = ['logo_420x30.jpg']
        self.assertEqual(images, id_obj.images())

    def test_form_elements(self):
        id_obj = self.get_id_instance()
        elems = [{'type': 'hidden', 'value': 'index.asp', 'name': 'GO'},
                 {'type': 'hidden', 'value': None, 'name': 'v12_time'},
                 {'type': 'hidden', 'value': None, 'name': 'WANT1'},
                 {'type': 'radio', 'value': '2', 'name': 'isp'},
                 {'type': 'radio', 'value': '3', 'name': 'isp'},
                 {'type': 'text', 'value': None, 'name': 'PPW'},
                 {'type': 'text', 'value': None, 'name': 'SSID'},
                 {'type': 'text', 'value': None, 'name': 'wirelesspassword'},
                 {'type': 'button', 'value': '', 'name': 'button'}]
        self.assertEqual(elems, id_obj.form_elements())

    def test_scripts(self):
        id_obj = self.get_id_instance()
        scripts = ['lang/b28n.js',
                   'gozila.js',
                   'table.js',
                   'menu.js',
                   '[Inline 1]',
                   '[Inline 2]',
                   '[Inline 3]',
                   '[Inline 4]',
                   '[Inline 5]',
                   '[Inline 6]',
                   '[Inline 7]',
                   '[Inline 8]']
        self.assertEqual(scripts, id_obj.scripts())
