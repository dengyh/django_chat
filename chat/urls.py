#coding: utf-8
import settings
from django.conf.urls import patterns, include, url

urlpatterns = patterns('chat.views',
    url(r'^get/(\w+)/$', 'getNewMessage', {'templateName': 'new-messages.html'}), # for ajax
    url(r'^new/(\w+)/$', 'createNewMessage'), # for ajax
    url(r'^custom/$', 'getCustomID', {'templateName': 'custom-box.html'}), # for ajax
    url(r'^server/$', 'getServerMessage', {'templateName': 'server-box.html'}),
    url(r'^session/$', 'getSessionList', {'templateName': 'session-list.html'}),

    url(r'demo/(custom)/$', 'getDemo', {'templateName': 'custom.html'}),
    url(r'demo/(server)/$', 'getDemo', {'templateName': 'server.html'}),
)
