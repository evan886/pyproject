from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^register/$', register),
    url(r'^register_handler/$', register_handler),
    url(r'^check_name/$', check_name),
    url(r'^login/$', login),
    url(r'^checkloginstatus/$', check_login_status),
    url(r'^login_handler/$', login_handler),
    url(r'^loginstatus/$', login_status),
    url(r'^quitlogin/$', quit_login),
    url(r'^index/$', index),
    url(r'^$', user_center_info),
    url(r'^order/$', user_center_order),
    url(r'^address/$', user_center_address),
    url(r'^add/address/$', add_address),
    url(r'^changedefaultaddr/$', change_default_addr),
]
