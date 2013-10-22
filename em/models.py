from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

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
        ('https', 'Supports HTTP management console'),
        ('whitelist', 'Supports MAC address whitelist'),
        ('blacklist', 'Supports MAC address blacklist'),
        ('password_in_body', 'Router sends password in body of login page'),
        ('alt_mgmt_port', 'Can run admin UI on non-standard HTTP port'))
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
        ('image', 'Image URL'),
        ('link', 'Link URL'),
        ('form', 'HTML Form Attribute'),)
    router_page = models.ForeignKey(RouterPage, related_name='attributes')
    type = models.CharField(max_length=40, choices=ATTR_TYPES)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=250)

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
