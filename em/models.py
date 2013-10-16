from django.db import models
from django.contrib import auth

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
    router = models.ManyToManyField(Router)
    feature_name = models.CharField(max_length=40, choices=FEATURE_CHOICES)

    def __str__(self):
        return self.feature_name

class RouterPage(models.Model):
    """
    Contains sample pages from routers used in development and testing.
    These are the admin pages from the router's web UI.
    """
    router = models.ForeignKey(Router)
    relative_url = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    body = models.TextField()
    comments = models.TextField(null=True, blank=True)

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
    router_page = models.ForeignKey(RouterPage)
    type = models.CharField(max_length=40, choices=ATTR_TYPES)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=1000)

class RouterManager(models.Model):
    """
    Maps a router to the Python class that can parse its output and
    manipulate its features. The manager field contains a fully-qualified
    Python class name, such as 'emserver.em.routers.make.model_version'
    """
    router = models.ForeignKey(Router)
    manager = models.CharField(max_length=400)

class Network(models.Model):
    """
    Contains information about a user's network.
    """
    user = models.ForeignKey(auth.models.User)
    router = models.ForeignKey(Router)
    router_mac_address = models.CharField(max_length=50, null=True)
    network_name = models.CharField(max_length=100,
                                    default="Default Network")
    is_default = models.BooleanField(default=False)
    first_seen = models.DateTimeField(auto_now_add=True, editable=False)
    last_seen = models.DateTimeField(auto_now=True, editable=False)
    times_seen = models.IntegerField(default=1)

class Device(models.Model):
    """
    Contains information about a device on a user's network.
    The fields installed_em_product and installed_em_version will
    contain information only if the user is known to have some EM
    product installed on the device.
    """
    network = models.ForeignKey(Network)
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
    user_assigned_name = models.CharField(
        max_length=100, null=True, blank=True)
    first_seen = models.DateTimeField(auto_now_add=True, editable=False)
    last_seen = models.DateTimeField(auto_now=True, editable=False)
    times_seen = models.IntegerField(default=1)
