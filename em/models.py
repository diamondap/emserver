from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from urllib.parse import urlparse

class Router(models.Model):
    """
    Contains generic information about a router model.
    """
    AUTH_CHOICES = (
        ('none', 'No login/authentication is supported'),
        ('html', 'Login via HTML form'),
        ('http_basic', 'HTTP basic authentication'),
        ('http_digest', 'HTTP digest authentication'))
    PROTOCOL_CHOICES = (
        ('http', 'http'),
        ('https', 'https'))

    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    auth_protocol = models.CharField(max_length=20,
                                     choices=AUTH_CHOICES,
                                     default='html')
    protocol = models.CharField(max_length=20,
                                choices=PROTOCOL_CHOICES,
                                default='http')
    port = models.IntegerField(default=80)
    firmware_version = models.CharField(max_length=100)
    firmware_major = models.IntegerField(null=True, blank=True)
    firmware_minor = models.IntegerField(null=True, blank=True)
    firmware_point = models.IntegerField(null=True, blank=True)
    firmware_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    comments = models.TextField(null=True, blank=True)

    unique_together = (("manufacturer", "model", "firmware_version"),)

    def __str__(self):
        return "{0} {1} ({2})".format(
            self.manufacturer, self.model, self.firmware_version)

class RouterFeature(models.Model):
    """
    Information about router features.
    """
    FEATURE_CHOICES = (
        ('http', 'Supports HTTP management console'),
        ('https', 'Supports HTTPS management console'),
        ('whitelist', 'Supports MAC address whitelist'),
        ('blacklist', 'Supports MAC address blacklist'),
        ('mac_time_block', 'Supports MAC address blocking by day and time'),
        ('password_in_body', 'Router sends password in body of login page'),
        ('password_in_header', 'Router sends password in login page headers'),
        ('alt_mgmt_port', 'Can run admin UI on non-standard HTTP port'),
        ('remote_mgmt', 'Supports remote management'),
        )
    router = models.ManyToManyField(Router, related_name='features')
    feature_name = models.CharField(max_length=40, choices=FEATURE_CHOICES)

    def __str__(self):
        return self.get_feature_name_display()

class RouterPage(models.Model):
    """
    Contains sample pages from routers used in development and testing.
    These are the admin pages from the router's web UI.
    """
    router = models.ForeignKey(Router, related_name='pages')
    relative_url = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    body = models.TextField()
    comments = models.TextField(null=True, blank=True)
    _title = None

    def get_title(self):
        if self._title is None:
            try:
                self._title = self.attributes.get(type='title')
            except ObjectDoesNotExist:
                self._title = RouterPageAttribute()
                self._title.type = 'title'
                self._title.router_page = self
        return self._title

    def get_headers(self):
        return self.attributes.filter(type='header').order_by('name')

    def get_form_attributes(self):
        return self.attributes.filter(type='form_attr').order_by('name')

    def get_images(self):
        return self.attributes.filter(type='image_src').order_by('value')

    def get_links(self):
        return self.attributes.filter(type='link').order_by('value')

    def get_scripts(self):
        return self.attributes.filter(type='script').order_by('value')

    def get_form_fields(self):
        return self.attributes.filter(
            type__in=RouterPageAttribute.FORM_FIELD_TYPES).order_by('value')

    def __str__(self):
        return self.relative_url

class RouterPageAttribute(models.Model):
    """
    Contains information about attributes associated with router pages.
    These attributes can help us to identify a specific router from
    its index page or login page.
    """
    ATTR_TYPES = (
        ('header', 'HTTP Header'),
        ('title', 'Page Title'),
        ('image_src', 'Image URL'),
        ('link', 'Link URL'),
        ('form_attr', 'HTML Form Attribute'),
        ('text', 'HTML Text Input'),
        ('textarea', 'HTML TextArea'),
        ('radio', 'HTML Radio Input'),
        ('checkbox', 'HTML Checkbox Input'),
        ('password', 'HTML Password Input'),
        ('file', 'HTML File Input'),
        ('image', 'HTML Image Input'),
        ('hidden', 'HTML Hidden Input'),
        ('button', 'HTML Button Input'),
        ('submit', 'HTML Submit Input'),
        ('script', 'JavaScript File'),)
    FORM_FIELD_TYPES = ['text', 'textarea', 'radio', 'checkbox',
                        'password', 'file', 'image', 'hidden',
                        'button', 'submit']

    router_page = models.ForeignKey(RouterPage, related_name='attributes')
    type = models.CharField(max_length=40, choices=ATTR_TYPES)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return "[{0}] [{1}] -> {2}".format(self.type, self.name, self.value)

class RouterManager(models.Model):
    """
    Maps a router to the Python class that can parse its output and
    manipulate its features. The manager field contains a fully-qualified
    Python class name, such as 'emserver.em.routers.make.model_version'
    """
    router = models.ForeignKey(Router, related_name='manager')
    manager = models.CharField(max_length=400)

    def __str__(self):
        return self.manager

# http://standards.ieee.org/develop/regauth/oui/oui.txt
class MacManufacturer(models.Model):
    mac_prefix = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Device(models.Model):
    """
    Contains information about a device on a user's network.
    The fields installed_em_product and installed_em_version will
    contain information only if the user is known to have some EM
    product installed on the device.
    """
    mac_manufacturer = models.ForeignKey(MacManufacturer, null=True,
                                         related_name='mac_manufacturer')
    mac_address = models.CharField(max_length=50)
    last_ip4_address = models.IPAddressField(null=True, blank=True)
    last_ip6_address = models.GenericIPAddressField(
        protocol='IPv6', null=True, blank=True)
    device_type = models.CharField(max_length=50, null=True, blank=True)
    os_type = models.CharField(max_length=50, null=True, blank=True)
    os_version = models.CharField(max_length=50, null=True, blank=True)
    installed_em_product = models.CharField(
        max_length=50, null=True, blank=True)
    installed_em_version = models.CharField(
        max_length=50, null=True, blank=True)
    hostname = models.CharField(max_length=100, null=True, blank=True)
    first_seen = models.DateTimeField(auto_now_add=True, editable=False)
    last_seen = models.DateTimeField(auto_now=True, editable=False)
    times_seen = models.IntegerField(default=1)

    def get_name(self, user):
        name = None
        try:
            name = DeviceName.objects.filter(
                user=user, device=self).values('name')[0]
        except DoesNotExist:
            pass
        return name

    def __str__(self):
        return self.mac_address

class DeviceName(models.Model):
    """
    A single device may show up on several user accounts, since users may
    carry laptops, tablets and phones to each other's houses. We want each
    user to be able to give the device a custom name. Or more specifically,
    we don't want User A to name a device "piece of crap" and then have
    that name show up on User B's account.
    """
    user = models.ForeignKey(User, related_name='user')
    device = models.ForeignKey(Device, related_name='device')
    name = models.CharField(max_length=100, null=True, blank=True)

    unique_together = (("user", "device"),)

    def __str__(self):
        return self.name

# End of Django models. Below are non-Django models.

class RouterRequest():
    """
    This class contains information about HTTP requests that the client will
    have to send to the router. This is not a Django model. We don't save
    these.
    """
    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.port = kwargs.get('port')
        self.method = kwargs.get('method')
        self.headers = kwargs.get('headers')
        self.data = kwargs.get('data')
        self.request_type = kwargs.get('request_type')

    def __str__(self):
        return "RouterRequest {0} {1}".format(self.method, self.url)


class RouterResponse():
    """
    This class contains information about an HTTP response that our remote
    client received and then passed back to the server. This is not a
    Django model. We don't save these.
    """

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.method = kwargs.get('method')
        self.status_code = kwargs.get('status_code')
        self.port = kwargs.get('port')
        self.headers = kwargs.get('headers')
        self.body = kwargs.get('body')

    def __str__(self):
        return "RouterResponse {0} {1}".format(self.method, self.url)

    @classmethod
    def convert_headers(self, http_headers):
        """
        Convert special http_headers object to standard dict.
        """
        headers = {}
        for key in http_headers:
            headers[key] = http_headers[key]
        return headers

    @classmethod
    def get_port_from_url(self, url):
        parsed = urlparse(url)
        return parsed.port

class NetClient:
    """
    Contains information about a single client on the network.
    """
    def __init__(self, *args, **kwargs):
        self.ip = kwargs.get('ip')
        self.mac = kwargs.get('mac')
        self.hostname = kwargs.get('hostname')
        self.conn_type = kwargs.get('conn_type')
        self.device_type = kwargs.get('device_type')
        self.os_type = kwargs.get('os_type')
        self.is_whitelisted = kwargs.get('is_whitelisted')
        self.is_blacklisted = kwargs.get('is_blacklisted')
        self.nickname = kwargs.get('nickname')

    def __str__(self):
        return "NetClient {0}".format(self.ip)

    def merge(self, other):
        """
        Merges all of the values from another NetClient object into this
        NetClient object. Anytime the other object's attribute value is
        not None, it will overwrite this NetClient's attribute value.

        Returns self.
        """
        if self.ip != other.ip:
            raise ValueError('Cannot merge NetClient objects with '
                             'different IP addresses.')
        for key in self.__dict__:
            val = getattr(self, key)
            other_val = getattr(other, key)
            if other_val is not None and other_val != '':
                setattr(self, key, other_val)
        return self


    @classmethod
    def merge_lists(self, list1, list2):
        """
        Merges two lists of NetClient objects. The resulting lists will
        contain all the members of both lists, with no duplicates. The
        merge uses the following logic:

        1. If an object's property is None in one list and not None in the
        other list, the non-None property wins.
        2. If a property is not None in both lists, the value of the property
        in list2 wins.

        NetClient objects are considered unique by IP address. (Yes, IP, not
        MAC, because we are comparing devices currently attached to the
        network. The router will always give us the IP addresses, which are
        unique at the moment, but it will not always give us the MAC address.)

        You may run into problems if either list includes the same IP address
        more than once.
        """
        ips = set()
        clients = []
        for client in list1:
            list2_client = next((c for c in list2 if c.ip == client.ip), None)
            if list2_client is not None:
                client = client.merge(list2_client)
            if not client.ip in ips:
                clients.append(client)
                ips.add(client.ip)
            else:
                raise ValueError("Mutilple entries in list1 have IP "
                                 "address '{0}'".format(client.ip))
        for client in list2:
            seen = set()
            if client.ip in seen:
                raise ValueError("Mutilple entries in list2 have IP "
                                 "address '{0}'".format(client.ip))
            if not client.ip in ips:
                clients.append(client)
                ips.add(client.ip)
            seen.add(client.ip)
        return clients

class NetState:

    def __init__(self, *args, **kwargs):
        self.clients = kwargs.get('clients')
        self.manager = kwargs.get('manager')
        self.router = kwargs.get('router')
