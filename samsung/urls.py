from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from .views import samsung, view, new, test, summary_mounth, exel

urlpatterns = [
    url(r'^new/$', new, name='new'),
    url(r'^view/(?P<id>\d+)/$', view, name='detail'),
    url(r'^test/$', test, name='test'),
    url(r'^exel/$', exel, name='exel_out'),
    url(r'^summary_mounth/$', summary_mounth, name='summary'),
    url(r'^$', samsung, name='samsung'),
]
