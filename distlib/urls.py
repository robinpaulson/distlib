from django.conf.urls import patterns, include, url
from distlib.distlibapp.views import searchbooks
from distlib.distlibapp.views import searchcircles
from distlib.distlibapp.views import createcircle
from distlib.distlibapp.views import login
from distlib.distlibapp.views import authenticate
from distlib.distlibapp.views import addbook
from distlib.distlibapp.views import signup
from distlib.distlibapp.views import circledetails
from distlib.distlibapp.views import userdetails
from distlib.distlibapp.views import addtocircle
from distlib.distlibapp.views import ask
from distlib.distlibapp.views import asked
from distlib.distlibapp.views import books
from distlib.distlibapp.views import circles
from distlib.distlibapp.views import notifications
from distlib.distlibapp.views import searches
from distlib.distlibapp.views import logout
from distlib.distlibapp.views import about
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
   (r'^ask/(.*?)/(.*?)/$', ask),
   (r'^asked/(.*?)/(.*?)/$', asked),
    (r'^createcircle/$', createcircle),
    (r'^searchbooks/$', searchbooks),
    (r'^searchcircles/$', searchcircles),
    (r'^login/$', login),
    (r'^authenticate/$', authenticate),
    (r'^addbook/$', addbook),
    (r'^signup/$', signup),
    (r'^circles/(.*?)/$',circledetails),
    (r'^addtocircle/(.*?)/$',addtocircle),
    (r'^user/(.*?)/$',userdetails),
    (r'^books/$', books),
    (r'^circles/$', circles),
    (r'^notifications/$', notifications),
    (r'^searches/$', searches),
    (r'^about/$', about),
    (r'^home/', books),
    (r'^logout/', logout),
    (r'^$', books),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'C;/distlib/distlib/static/'}),                       
    # Examples:
    # url(r'^$', 'distlib.views.home', name='home'),
    # url(r'^distlib/', include('distlib.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
