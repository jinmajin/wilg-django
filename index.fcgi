#!/usr/bin/env python
import sys, os, time, threading, django.utils.autoreload
from subprocess import call

os.environ['DJANGO_SETTINGS_MODULE'] = "wilg_django_site.settings"

def reloader_thread():
  while True:
    if django.utils.autoreload.code_changed():
      os._exit(3)
    time.sleep(1)
t = threading.Thread(target=reloader_thread)
t.daemon = True
t.start()

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
