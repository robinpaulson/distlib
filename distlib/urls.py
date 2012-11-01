from django.conf.urls import patterns, include, url
from distlib.distlibapp.books import searchbooks
from distlib.distlibapp.circles import searchcircles
from distlib.distlibapp.circles import createcircle
from distlib.distlibapp.views import login
from distlib.distlibapp.views import authenticate
from distlib.distlibapp.books import addbook
from distlib.distlibapp.books import addvolume
from distlib.distlibapp.views import signup
from distlib.distlibapp.circles import circledetails
from distlib.distlibapp.users import userdetails
from distlib.distlibapp.circles import addtocircle
from distlib.distlibapp.views import ask
from distlib.distlibapp.views import asked
from distlib.distlibapp.books import books
from distlib.distlibapp.circles import circles
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
    (r'^addbook/(.*?)/$', addvolume),
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
        {'document_root': 'C:/distlib/distlib/distlibapp/static/'}),                       
    # Examples:
    # url(r'^$', 'distlib.views.home', name='home'),
    # url(r'^distlib/', include('distlib.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
