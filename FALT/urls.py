from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'FALT.views.home', name='home'),
    # url(r'^FALT/', include('FALT.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'comp1.views.index'),
    url(r'^read_word/$', 'comp1.views.read_word'),
    url(r'^test_ajax/$', 'comp1.views.test_ajax'),
    url(r'^syllables/$', 'comp1.views.syllables'),
    url(r'^main/$', 'comp1.views.mainRequest'),
    url(r'^file/$', 'comp1.views.fileRequest'),
)
