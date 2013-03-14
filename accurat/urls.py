"""
Project: ACCURAT Demo Translation Services
 Author: Christian Federmann <cfedermann@dfki.de>
"""
from django.conf.urls.defaults import patterns, url #, include

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'accurat.views.home', name='home'),
    url(r'^translate/$', 'accurat.views.translate', name='translate'),

    (r'^login/$', 'accurat.views.login',
      {'template_name': 'login.html'}),

    (r'^logout/$', 'accurat.views.logout',
      {'next_page': '/'}),


    # url(r'^accurat/', include('accurat.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
