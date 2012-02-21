import re
import string

from django.core.exceptions import ValidationError
from django.core import validators
from django.utils.html import strip_tags

from product_details import product_details
from statsd import statsd
from tower import ugettext as _


# Simple email regex to keep people from submitting personal data.
EMAIL_RE = re.compile(r'[^\s]+@[^\s]+\.[^\s]{2,6}')

# IPv4 Address verifier
PRIVATE_IP_RE = re.compile(
    r'^(https?://)?' # http:// or https://
    r'(?:0\.0\.0\.0)|'
    r'(?:127\.0)|'
    r'(?:10\.)|'
    r'(?:172\.1[6-9]\.)|'
    r'(?:172\.2[0-9]\.)|'
    r'(?:172\.3[0-1]\.)|'
    r'(?:localhost)|'
    r'(?:192\.168\.)', re.IGNORECASE)

# Simple "possibly a URL" regex
URL_RE = re.compile(r'(://|www\.[^\s]|\.\w{2,}/)')


def validate_no_html(str):
    """Disallow HTML."""
    if strip_tags(str) != str:
        raise ValidationError(_('Feedback must not contain HTML.'))


def validate_no_email(str):
    """Disallow texts possibly containing emails addresses."""
    if EMAIL_RE.search(str):
        raise ValidationError(
            _('Your feedback seems to contain an email address. Please remove '
              'this and similar personal data from the text, then try again. '
              'Thanks!'))


def validate_no_private_ips(str):
    """Disallow private IPv4 IPs from being submitted."""
    if PRIVATE_IP_RE.search(str):
        raise ValidationError(
            _('URLs with IP addresses must contain public IP addresses.'))


def validate_no_urls(str):
    """Disallow text possibly containing a URL."""
    if URL_RE.search(str):
        raise ValidationError(
            _('Your feedback seems to contain a URL. Please remove this and '
              'similar personal data from the text, then try again. Thanks!'))


class ExtendedURLValidator(validators.URLValidator):
    """URL validator that allows about: and chrome: URLs."""
    regex = re.compile(
        r'^about:[a-z]+$|'  # about:something URLs
        r'^chrome://[a-z][/?\.\S]+$|'  # chrome://... URLs
        r'^https?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|' # domain...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
