from urllib.parse import urlparse
from requests.models import Response
from bs4 import BeautifulSoup
from em.models import Router, RouterPageAttribute

class Identifier:
    """
    This class parses a page from a router's Web UI and extracts some
    attributes from the page's HTML. It can compare those attributes to
    attributes of known pages to try to identify the router.
    """

    def __init__(self, *args, **kwargs):
        self.html = kwargs.get('html', None)
        self.url = kwargs.get('url', None)
        self.headers = kwargs.get('headers', None)
        self.port = kwargs.get('port', None)
        self.doc = None
        self.parse_exception = None
        self._parse_html()

    @classmethod
    def get_instance(self, url, http_response):
        """
        Given a URL and an instance of requests.models.Response, this
        returns a fully-instantiated Identifier. Param URL is a string
        URL, like 'http://192.168.1.1/login.html'. Param http_response
        is an instance of requests.models.Response. Return value is an
        instance of em.libs.router.identifier.Identifier.
        """
        if http_response.status_code == 200:
            headers = {}
            for name in http_response.headers.keys():
                headers[name] = http_response.headers[name]
            parsed_url = urlparse(url)
            return Identifier(html=http_response.text,
                              url=parsed_url.path,  # use the relative URL!
                              port=parsed_url.port,
                              headers=headers)
        else:
            raise RuntimeError("Cannot handle a non-200 HTTP Response.")

    def _parse_html(self):
        """
        Parses the HTML in the object's HTML attribute. Returns True
        or False to indicated whether parsing succeeded, and sets
        self.parse_exception if parsing failed.
        """
        try:
            self.doc = BeautifulSoup(self.html)
            return True
        except (BaseException, TypeError) as ex:
            self.parse_exception = ex
            return False

    def parsing_succeeded(self):
        """
        Returns True/False to indicate whether parsing the HTML succeeded.
        """
        return self.parse_exception is None

    def title(self):
        """
        Returns the title of the HTML document as a string.
        """
        if self.doc.title:
            return self.doc.title.string

    def links(self):
        """
        Returns the href attribute of the all the links in the HTML document
        as a list of strings.
        """
        links = []
        for link in self.doc.find_all('a'):
            links.append(link.get('href'))
        return links

    def forms(self):
        """
        Returns a list of dictionaries, each of which contains the attributes
        of a single form on the page. Attributes typically include name,
        method and action.
        """
        forms = []
        for form in self.doc.find_all('form'):
            forms.append(form.attrs)
        return forms

    def images(self):
        """
        Returns the src attribute of all the images on the page as a list
        of strings.
        """
        images = []
        for img in self.doc.find_all('img'):
            images.append(img.get('src'))
        return images

    def identify(self):
        """
        Returns the router type id, make, model and firmware.
        """
        # TODO: Implement identify
        return Router.objects.all()[0]
