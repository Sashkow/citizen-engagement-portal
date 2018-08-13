from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from volunteer import views as volunteer_views

import citizen_engagement_portal.settings as settings

from django.conf.urls.static import static

from django.urls import path

urlpatterns = [
    url(r'^$', volunteer_views.home, name='home'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^signup/$', volunteer_views.signup, name='signup'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--
    # url('auth/', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),

    # url(r'^home/$', core_views.home),
    url(r'^profile/$', volunteer_views.profile, name='profile'),
    url(r'^event/(?P<id>\w+)/', volunteer_views.event, name='event'),
    url(r'^newevent/$', volunteer_views.new_event, name='newevent'),
    url(r'^follow/$', volunteer_views.follow_event, name='follow_event'),
    ] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)