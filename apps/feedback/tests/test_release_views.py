from nose.tools import eq_

from input import FIREFOX, LATEST_RELEASE
from input.tests import FX_UA, ViewTestCase, enforce_ua
from input.urlresolvers import reverse


class ReleaseTests(ViewTestCase):
    """Test feedback for Firefox release versions."""

    def _get_page(self, ver=None):
        """Request release feedback page."""
        extra = dict(HTTP_USER_AGENT=FX_UA % ver) if ver else {}

        return self.client.get(reverse('feedback'), **extra)

    @enforce_ua
    def test_feedback(self):
        """No UA: redirect."""
        r = self._get_page()
        eq_(r.status_code, 200)

    def post_feedback(self, data, ajax=False, follow=True):
        """POST to the release feedback page."""
        options = dict(HTTP_USER_AGENT=(FX_UA % '20.0'), follow=follow)
        if ajax:
            options['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'

        return self.client.post(reverse('feedback'), data, **options)
