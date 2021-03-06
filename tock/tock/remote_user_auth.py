from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth.middleware import RemoteUserMiddleware
from django.core.exceptions import ValidationError
from django.conf import settings

from employees.models import UserData


def email_to_username(email):
    """Converts a given email address to a Django compliant username"""
    email_list = email.lower().split('@')

    # If ALLOWED_EMAIL_DOMAINS, then ensure it is in the list of domains
    if settings.ALLOWED_EMAIL_DOMAINS:
        if email_list[1] in settings.ALLOWED_EMAIL_DOMAINS:
            pass
        else:
            raise ValidationError('Email Domain not in Allowed List')

    # Return the email address with only the first 30 characters, this is the
    # username
    return email_list[0][:30]


class TockUserBackend(RemoteUserBackend):

    def clean_username(self, email_address):
        """
        Performs any cleaning on the "username" prior to using it to get or
        create the user object.  Returns the cleaned username.

        By default, returns the username unchanged.
        """
        return email_to_username(email_address)


class EmailHeaderMiddleware(RemoteUserMiddleware):
    header = 'HTTP_X_FORWARDED_EMAIL'


class UserDataMiddleware(object):

    def process_request(self, request):
        """Ensure that authenticated users have associated `UserData` records.
        """
        if request.user.is_authenticated():
            UserData.objects.get_or_create(user=request.user)
