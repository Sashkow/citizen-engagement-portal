from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from volunteer import views as core_views

from django.urls import path

urlpatterns = [

    url(r'^$', auth_views.login, name='login'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--
    # url('auth/', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),

    url(r'^profile/$', core_views.profile, name='profile'),
    url(r'^event/$', core_views.event),
    url(r'^newevent/$', core_views.new_event, name='newevent')
]