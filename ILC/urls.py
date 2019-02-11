from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
# from django.contrib.auth.views import logout
from .views import  login_user, logout_user, topbar


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', login_user, name='login_user'),
    url(r'^logout/', logout_user, name='logout_user'),
    url(r'^samsung/', include('samsung.urls')),
    url(r'^$', topbar),
]
