from django.conf.urls import url
from apple import views


urlpatterns = [

    url(r'^$', views.home, name='home'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

    url(r'^signup/$', views.signup, name='signup'),

    url(r'^talk/(?P<pk>\d+)/remove/$', views.talk_remove, name='talk_remove'),
]
