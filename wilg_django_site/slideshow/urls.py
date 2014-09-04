from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
               (r'^media/s(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT }),
              )
