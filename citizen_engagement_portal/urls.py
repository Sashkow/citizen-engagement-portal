from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from volunteer import views as volunteer_views

import citizen_engagement_portal.settings as settings

from django.conf.urls.static import static

from django.urls import path
import notifications.urls

import social_django.urls

from volunteer.views import live_tester, make_notification, mark_all_as_read
from volunteer.models import Event
from djgeojson.views import GeoJSONLayerView
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$', volunteer_views.home, name='home'),
    url(r'^wayback/', volunteer_views.home, name='home'),
    url(r'^login/$', auth_views.login,  name='login'),
    # url(r'^usual_login/$', auth_views.login, {'template_name': 'usual_login.html'}, name='usual_login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^signup/$', volunteer_views.signup, name='signup'),
    url(r'^usual_login/$', volunteer_views.usual_login, name='usual_login'),
    url(r'^intropage/$', volunteer_views.intropage, name='intropage'),


    url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--
    url(r'^success_oauth/$', volunteer_views.just_after_scuccess_auth, name='success_oauth'),
    # url('auth/', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),

    url(r'^test_make/', make_notification),
    url(r'^mark_all_as_read/', mark_all_as_read),
    url(r'^test/', live_tester),

    # url(r'^home/$', core_views.home),
    url(r'^profile/$', volunteer_views.profile, name='profile'),
    url(r'^notifications/$', volunteer_views.notifications, name='notifications'),

    url(r'^event/(?P<id>\w+)/', volunteer_views.event, name='volunteer_event'),
    url(r'^newevent/$', volunteer_views.new_event, name='newevent'),

    url(r'^follow/$', volunteer_views.follow_event, name='follow_event'),
    url(r'^subscribe/$', volunteer_views.subscribe_event, name='subscribe_event'),
    url(r'^typefilter/$', volunteer_views.type_filter, name='type_filter'),
    url(r'^profile/edit', volunteer_views.profile_edit, name='profile_edit'),
    url(r'^achivments/$', volunteer_views.get_achivments, name='achivments'),
    url(r'^achivment_legaue/$', volunteer_views.achivments_legaue, name='achivments_legaue'),
    url(r'^form/(?P<id>\d+)/', volunteer_views.event_edit, name='form'),
    url(r'^refresh/digest/$', volunteer_views.refresh_digest, name='refresh_digest'),
    url(r'^changeorgtask/(?P<id>\d+)/', volunteer_views.change_org_task, name='changetask'),
    url(r'^changephoto/', volunteer_views.change_photo, name='changephoto'),
    url(r'^app/task/', volunteer_views.app_task, name='app_task'),
    url(r'^task/executor', volunteer_views.task_executor, name='task_executor'),
    url(r'^get/org/tasks', volunteer_views.get_event_org_tasks, name='get_event_org_tasks'),

    url(r'^dispatch_social_login/$', volunteer_views.dispatch_social_login, name='dispatch_social_login'),
    url(r'^notifications/$', volunteer_views.notifications, name='notifications'),
    url(r'^notifications_count/$', volunteer_views.notifications_count, name='notifications_count'),

    url(r'^map/$', volunteer_views.map_show, name = "map"),


    url(r'^canceledtask/(?P<id>\d+)$', volunteer_views.cancel_task, name = "cancel_task"),

    url(r'^data.geojson$', GeoJSONLayerView.as_view(
        model=Event,
        properties=('name', 'description','events_type', 'get_events_type_url', 'get_events_type_marker_url', 'get_event_url')
    ), name='event_geo_data'),
    url(r'^fullcalendar/', login_required(TemplateView.as_view(template_name="fullcalendar.html")), name='fullcalendar'),
    # url(r'^wayback/$', login_required(TemplateView.as_view(template_name="wayback.html")), name='wayback'),
    url(r'^schedule/', include('schedule.urls')),

    url(r'^terms_of_use/$', TemplateView.as_view(template_name="terms_of_use.html"), name='terms_of_use'),


              ] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)