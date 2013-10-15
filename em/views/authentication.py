from django.contrib.auth.models import User
from django.contrib import auth
from django.core.validators import email_re
from django.http import HttpResponseRedirect
from django.views.decorators.http import (require_GET, require_POST)
from django.shortcuts import (render, redirect)
from django.contrib import messages
from django.db import connection
from emserver import settings
from emserver.libs import utils
#from emserver import models


NINETY_DAYS = (60 * 60 * 24 * 90)


class AuthenticationError(Exception):
    "General exception for authentication errors"

    def __init__(self, message):
        self.message = message

    def __unicode__(self):
        return unicode(self.__class__.__name__ + self.message)

class InvalidLoginContextError(Exception):
    """
    This error is raised when a valid user attempts to log in to a part of the
    system that they are not allowed to log in to.
    """

    def __init__(self, message):
        self.message = message

    def __unicode__(self):
        return unicode(self.__class__.__name__ + self.message)


class BasicBackend:
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class EmailBackend(BasicBackend):

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return auth.authenticate(username=user.username, password=password)
        return None


def authenticate(username=None, password=None):
    "Authenticates user"
    user = EmailBackend().authenticate(username, password)
    if user is None:
        #emc_util.log.info("Login attempt failed user {0}".format(username))
        raise AuthenticationError("Invalid user name or password")
    if not user.is_active:
        #emc_util.log.info("Login rejected for disabled user {0}".format(
        #        username))
        raise AuthenticationError("Your account has been disabled")
    return user


@require_POST
def login(request):
    "Logs the user into the site."
    try:
        user = authenticate(request.POST['email'], request.POST['password'])
        create_session(user, request)
        next_page = None
        if request.GET:
            next_page = request.GET['next']
        if next_page:
            return HttpResponseRedirect(next_page)
        return redirect('home')
    except AuthenticationError as ex:
        messages.error(request, ex.message)
        request.session.flush()
    except Exception as ex:
        emc_util.log.exception(ex)
        messages.error(request, ex.message)
        request.session.flush()
    return render(request, 'home/index.html')


@require_GET
def logout(request):
    "Logs the user out of the site, and gets rid of their session."
    if request and request.user:
        emc_util.log.info("{0} logged out".format(request.user))
    request.session.flush()
    return redirect('home')


def create_session(user, request):
    auth.login(request, user)
    request.session.set_expiry(NINETY_DAYS)
