from django.conf.urls import patterns, include, url
from django.conf import settings

from wds.models import Member
from accounts.models import MyProfile
from django.db.models import Max
from django.contrib.auth.models import User, Permission
from django.views.generic.list import ListView
from userena.forms import SignupFormExtra

from afs import pts

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

def get_current_usernames():
    pts_query = pts.PTS(None, pts.PTS_UNAUTH)
    pts_result = pts_query.getEntry('system:wilg')
    names = [m._get_name() + "@mit.edu" for m in pts_result.members]
    return names

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wilg_django_site.views.home', name='home'),
    # url(r'^wilg_django_site/', include('wilg_django_site.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'wds.views.index', name='index'),
    url(r'^about', 'wds.views.about'),
    url(r'^rush', 'wds.views.rush'),
    url(r'^house', 'wds.views.house'),

    # omg django query syntax
    # get current member names
    url(r'^members', 
        ListView.as_view(queryset=MyProfile.objects.order_by('year')
                         .reverse().filter(
                user__email__in=get_current_usernames())
                         .order_by('-user__last_name'),
                         template_name="userena/profile_list.html"), 
        name='wds.views.members'), # this is a hack for active link highlighting...
    url(r'^_members', 'wds.views._members'),

    url(r'^alumnae', 'wds.views.alumnae'),
    url(r'^exec', 'wds.views._exec'),
    url(r'^events', 'wds.views.events'),
    url(r'^contact', 'wds.views.contact'),

    url(r'^current',  'mit.scripts_login'),
    url(r'^alumni',  'mit.scripts_login'),
    url(r'^resources', 'wds.views.resources'),
    url(r'^accounts/', include('userena.urls')),

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^slideshow/', include('slideshow.urls')),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
