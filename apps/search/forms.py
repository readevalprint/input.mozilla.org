from datetime import date

from django.conf import settings
from django import forms
from django.forms.util import ErrorDict

from product_details import product_details
from product_details.version_compare import Version
from tower import ugettext_lazy as _lazy

from input import (FIREFOX, MOBILE, PLATFORM_USAGE, LATEST_BETAS,
                   KNOWN_DEVICES, KNOWN_MANUFACTURERS)
from input.fields import DateInput, SearchInput
from feedback.models import VersionCount

PROD_CHOICES = (
    (FIREFOX.short, FIREFOX.pretty),
    (MOBILE.short, MOBILE.pretty),
)

VERSIONS = VersionCount.objects.filter(active=1)

VERSION_CHOICES = {
    FIREFOX: ([('--', _lazy(u'-- all --', 'version_choice'))] +
              [(v.version, v.version) for v in VERSIONS
              if v.product == FIREFOX.id]),
    MOBILE: ([('--', _lazy(u'-- all --', 'version_choice'))] +
             [(v.version, v.version) for v in VERSIONS
             if v.product == MOBILE.id]),
}

SENTIMENT_CHOICES = [('', _lazy('-- all --', 'sentiment_choice')),
    ('happy', _lazy('Praise')),
    ('sad', _lazy('Issues')),
    ('ideas', _lazy('Ideas')),
]
SENTIMENTS = ('happy', 'sad', 'ideas')

PLATFORM_CHOICES = ([('', _lazy('-- all --', 'platform_choice'))] +
              [(p.short, p.pretty) for p in PLATFORM_USAGE])

MANUFACTURER_CHOICES = [('Unknown', _lazy('Unknown'))] + [(m, m) for m in
                                                          KNOWN_MANUFACTURERS]

DEVICE_CHOICES = [('Unknown', _lazy('Unknown'))] + [(d, d) for d in
                                                    KNOWN_DEVICES]

LOCALE_CHOICES = [
    ('', _lazy('-- all --', 'locale_choice')),
    ('Unknown', _lazy('Unknown')),
] + [(lang, lang) for lang in sorted(product_details.languages)]


class ReporterSearchForm(forms.Form):
    q = forms.CharField(required=False, label='', widget=SearchInput(
        attrs={'placeholder': _lazy('Search by keyword')}))
    product = forms.ChoiceField(choices=PROD_CHOICES, label=_lazy('Product:'),
                                initial=FIREFOX.short, required=False)
    version = forms.ChoiceField(required=False, label=_lazy('Version:'),
            choices=VERSION_CHOICES[FIREFOX])
    sentiment = forms.ChoiceField(required=False, label=_lazy('Sentiment:'),
                                  choices=SENTIMENT_CHOICES)
    locale = forms.ChoiceField(required=False, label=_lazy('Locale:'),
                               choices=LOCALE_CHOICES)
    platform = forms.ChoiceField(required=False, label=_lazy('PLATFORM:'),
                           choices=PLATFORM_CHOICES)
    manufacturer = forms.ChoiceField(required=False,
                                     choices=MANUFACTURER_CHOICES)
    device = forms.ChoiceField(required=False, choices=DEVICE_CHOICES)
    date_start = forms.DateField(required=False, widget=DateInput(
        attrs={'class': 'datepicker'}), label=_lazy('Date range:'))
    date_end = forms.DateField(required=False, widget=DateInput(
        # L10n: This indicates the second part of a date range.
        attrs={'class': 'datepicker'}), label=_lazy('to'))
    page = forms.IntegerField(widget=forms.HiddenInput, required=False)

    # TODO(davedash): Make this prettier.
    def __init__(self, *args, **kwargs):
        """Pick version choices and initial product based on site ID."""
        super(ReporterSearchForm, self).__init__(*args, **kwargs)
        self.fields['version'].choices = VERSION_CHOICES[FIREFOX]

        # Show Mobile versions if that was picked by the user.
        picked = None
        if self.is_bound:
            try:
                picked = self.fields['product'].clean(self.data.get('product'))
            except forms.ValidationError:
                pass
        if (picked == MOBILE.short or not self.is_bound and
            settings.SITE_ID == settings.MOBILE_SITE_ID):
            # We default to Firefox. Only change if this is the mobile site.
            self.fields['product'].initial = MOBILE.short
            self.fields['version'].choices = VERSION_CHOICES[MOBILE]

    def clean(self):
        cleaned = self.cleaned_data

        # default date_end to today
        if (self.cleaned_data.get('date_start') and
            not self.cleaned_data.get('date_end')):
            self.cleaned_data['date_end'] = date.today()

        # Flip start and end if necessary.
        if (cleaned.get('date_start') and cleaned.get('date_end') and
            cleaned['date_start'] > cleaned['date_end']):
            (cleaned['date_start'], cleaned['date_end']) = (
                    cleaned['date_end'], cleaned['date_start'])

        # Ensure page is a natural number.
        try:
            cleaned['page'] = int(cleaned.get('page'))
            assert cleaned['page'] > 0
        except (TypeError, AssertionError):
            cleaned['page'] = 1

        if not cleaned.get('version'):
            cleaned['version'] = (getattr(FIREFOX, 'default_version', None) or
                                    Version(LATEST_BETAS[FIREFOX]).simplified)
        elif cleaned['version'] == '--':
            cleaned['version'] = ''

        return cleaned

    def full_clean(self):
        """
        Like Django's but we don't delete cleaned_data on error.
        """
        self._errors = ErrorDict()
        if not self.is_bound: # Stop further processing.
            return
        self.cleaned_data = {}
        # If the form is permitted to be empty, and none of the form data has
        # changed from the initial data, short circuit any validation.
        if self.empty_permitted and not self.has_changed():
            return
        self._clean_fields()
        self._clean_form()
        self._post_clean()
        # Errors are for data-prudes
        for field in self._errors.keys():
            self.cleaned_data[field] = ''
        self._errors = ErrorDict()
