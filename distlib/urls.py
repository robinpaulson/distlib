from django.conf.urls import patterns, include, url
from distlib.distlibapp.fblogin import fblogin
from distlib.distlibapp.books import searchBooksByCircle
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
from distlib.distlibapp.views import logout
from distlib.distlibapp.search import search
from distlib.distlibapp.videotags import getVideoTags
from distlib.distlibapp.videotags import putVideoTags
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
   (r'^ask/(.*?)/(.*?)/$', ask),
   (r'^asked/(.*?)/(.*?)/$', asked),
    (r'^createcircle/$', createcircle),
    (r'^search/$', search),
    (r'^searchbooks/$', searchBooksByCircle),
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
    (r'^home/', books),
    (r'^searchcircles/',circles),
    (r'^logout/', logout),
    (r'^fblogin/',fblogin),
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
    
    #Video tags
    (r'^putvideotags$', putVideoTags),
    (r'^getvideotags$', getVideoTags),
)
