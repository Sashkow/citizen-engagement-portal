from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from volunteer import views as volunteer_views

import citizen_engagement_portal.settings as settings

from django.conf.urls.static import static

from django.urls import path
import notifications.urls

from volunteer.views import live_tester, make_notification, mark_all_as_read

urlpatterns = [
    url(r'^$', volunteer_views.home, name='home'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^signup/$', volunteer_views.signup, name='signup'),

    url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--
    # url('auth/', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),

    url(r'^test_make/', make_notification),
    url(r'^mark_all_as_read/', mark_all_as_read),
    url(r'^test/', live_tester),

    # url(r'^home/$', core_views.home),
    url(r'^profile/$', volunteer_views.profile, name='profile'),
    url(r'^event/(?P<id>\w+)/', volunteer_views.event, name='event'),
    url(r'^newevent/$', volunteer_views.new_event, name='newevent'),
    url(r'^follow/$', volunteer_views.follow_event, name='follow_event'),
    url(r'^subscribe/$', volunteer_views.subscribe_event, name='subscribe_event'),
    url(r'^typefilter/$', volunteer_views.type_filter, name='type_filter'),
    url(r'^profile/edit', volunteer_views.profile_edit, name='profile_edit'),
    url(r'^achivments/$', volunteer_views.get_achivments, name='achivments'),
    url(r'^achivment_legaue/$', volunteer_views.achivments_legaue, name='achivments_legaue'),
    url(r'^testerer/$', volunteer_views.test, name='test'),
    url(r'^eventedit/(?P<id_event>\w+)/', volunteer_views.test_event, name='edit_event'),
    url(r'^form/(?P<id>\d+)/', volunteer_views.form, name='form'),

              ] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)