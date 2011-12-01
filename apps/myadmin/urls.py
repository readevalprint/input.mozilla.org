from django import http
from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin, auth
from django.shortcuts import redirect

from funfactory.urlresolvers import reverse
from session_csrf import anonymous_csrf

from myadmin import views

urlpatterns = patterns('',
    # Input stuff.
    url('^recluster/?$', views.recluster, name='myadmin.recluster'),
    url('^export_tsv/?$', views.export_tsv, name='myadmin.export_tsv'),
    url('^settings/?$', views.settings, name='myadmin.settings'),
    url('^login$', anonymous_csrf(auth.views.login), name='login'),
    # The Django admin.
    url('^', include(admin.site.urls)),
)


# Hijack the admin's login to use our pages.
def login(request):
    # If someone is already auth'd then they're getting directed to login()
    # because they don't have sufficient permissions.
    if request.user.is_authenticated():
        return http.HttpResponseForbidden()
    else:
        return redirect('%s?next=%s' % (reverse('login'), request.path))

admin.site.login = login
