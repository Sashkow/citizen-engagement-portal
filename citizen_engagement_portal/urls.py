"""citizen_engagement_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from volunteer import views as core_views

urlpatterns = [
    url(r'^$', core_views.home, name='home'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^oauth/', include('social_django.urls', namespace='social2')),  # <--
    url('auth/', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
]

#
# from django.contrib import admin
# from django.urls import path, include
# from django.conf.urls import url
# from django.contrib.auth.views import LogoutView, LoginView
# from volunteer.views import *
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     url('', include('social.apps.django_app.urls', namespace='social')),
#
#
#     # url(r'^$', index, name='index'),
#     # url(r'^login/$', LoginView.as_view(template_name='login.html'), name='login'),
#     # url(r'^logout/$', LogoutView.as_view(), name='logout'),
#
# ]
#
#
