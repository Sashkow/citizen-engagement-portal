
from django.contrib import admin
from .models import *

# from notifications.models import Notification

admin.site.empty_value_display = '(None)'

from django import forms
from schedule.widgets import ColorInput
from volunteer.models import User


class EventAdminForm(forms.ModelForm):
    class Meta:
        exclude = []
        model = Event
        widgets = {
            'color_event': ColorInput,
        }


class EventsTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EventsType._meta.fields]
    exclude = ['id']
    form = EventAdminForm

admin.site.register(EventsType, EventsTypeAdmin)



class CityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in City._meta.fields]
    exclude = ['_id']

admin.site.register(City, CityAdmin)



class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.fields]
    exclude = ['blocked', 'ID']
    list_filter = ['city', 'blocked']
    search_fields = ['first_name', 'last_name']


admin.site.register(User, UserAdmin)



class DigestListAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DigestList._meta.fields]
    exclude = ['ID']
    list_filter = ['type']

admin.site.register(DigestList, DigestListAdmin)



class StatusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Status._meta.fields]
admin.site.register(Status, StatusAdmin)


class EventAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(EventAdmin, self).get_queryset(request)
        user = User.objects.filter(django_user_id=request.user).first()
        if user:
            city = user.city
            qs = qs.filter(city=city)
        return qs

    list_display = [field.name for field in Event._meta.fields]
    exclude = ['ID']
    list_filter = ['events_type']
    search_fields = ['name']



        # if request.session.get('company_goggles'):
        #     return qs.filter(**{ getattr(self, 'company_field', 'company') :
        #                   request.session['company_goggles'] })

admin.site.register(Event, EventAdmin)




class EventsSubscribrsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EventsSubscriber._meta.fields]
    exclude = ['ID']
    def get_queryset(self, request):
        qs = super(EventsSubscribrsAdmin, self).get_queryset(request)
        user = User.objects.filter(django_user_id=request.user).first()
        if user:
            city = user.city
            qs = qs.filter(event__city=city)
        return qs

admin.site.register(EventsSubscriber, EventsSubscribrsAdmin)

class EventsPartcipiantAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EventsParticipant._meta.fields]
    exclude = ['ID']

    def get_queryset(self, request):
        qs = super(EventsPartcipiantAdmin, self).get_queryset(request)
        user = User.objects.filter(django_user_id=request.user).first()
        if user:
            city = user.city
            qs = qs.filter(event__city=city)
        return qs

admin.site.register(EventsParticipant, EventsPartcipiantAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.fields]
    exclude = ['ID']
admin.site.register(Comment, CommentAdmin)

class ReportAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Report._meta.fields]
    exclude = ['ID']
admin.site.register(Report, ReportAdmin)

class EventsPhotoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EventsPhoto._meta.fields]
    exclude = ['ID']

    def get_queryset(self, request):
        qs = super(EventsSubscribrsAdmin, self).get_queryset(request)
        user = User.objects.filter(django_user_id=request.user).first()
        if user:
            city = user.city
            qs = qs.filter(event__city=city)
        return qs
admin.site.register(EventsPhoto, EventsPhotoAdmin)

class EventsOrgTaskAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EventsOrgTask._meta.fields]
    exclude = ['ID']
admin.site.register(EventsOrgTask, EventsOrgTaskAdmin)


class LeagueAdmin(admin.ModelAdmin):
    list_display = [field.name for field in League._meta.fields]
    exclude = ['ID']
admin.site.register(League, LeagueAdmin)

class CityLeagueDesignAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CityLeagueDesign._meta.fields]
    exclude = ['ID']
admin.site.register(CityLeagueDesign, CityLeagueDesignAdmin)

class CurrencyAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Currency._meta.fields]
    exclude = ['ID']
admin.site.register(Currency, CurrencyAdmin)

class UserPointAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserPoint._meta.fields]
    exclude = ['ID']
admin.site.register(UserPoint, UserPointAdmin)


class AchievementAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in Achievement._meta.fields if not field.name=='ID']
    # list_editable = [field.name for field in Achievement._meta.fields if not field.name=='ID']
    list_display = [ 'achievement', 'league', 'description', 'image', 'background_achieve', 'color_text_achieve']
    list_editable = ['background_achieve', 'color_text_achieve']
    # print(list_editable)
    # exclude = ['ID']
admin.site.register(Achievement, AchievementAdmin)


class AchievementValueAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AchievementValue._meta.fields]
    exclude = ['ID']
admin.site.register(AchievementValue, AchievementValueAdmin)

class PointsListAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PointsList._meta.fields]
    exclude = ['ID']
admin.site.register(PointsList, PointsListAdmin)

class UserAchievementAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserAchievement._meta.fields]
    exclude = ['ID']
admin.site.register(UserAchievement, UserAchievementAdmin)


class DecreasePointsTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DecreasePointsType._meta.fields]
    exclude = ['ID']
admin.site.register(DecreasePointsType, DecreasePointsTypeAdmin)


class DecreasePointsInfoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DecreasePointsInfo._meta.fields]
    exclude = ['ID']
admin.site.register(DecreasePointsInfo, DecreasePointsInfoAdmin)

class NotificationsTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in NotificationsType._meta.fields]
    exclude = ['ID']
admin.site.register(NotificationsType, NotificationsTypeAdmin)


class TupoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Tupo._meta.fields]
    exclude = ['ID']
admin.site.register(Tupo, TupoAdmin)

class NotificationTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in NotificaationType._meta.fields]
    exclude = ['ID']
admin.site.register(NotificaationType, NotificationTypeAdmin)

class IncreasePointsTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in IncreasePointsType._meta.fields]
    exclude = ['ID']
admin.site.register(IncreasePointsType, IncreasePointsTypeAdmin)


class IncreasePointsInfoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in IncreasePointsInfo._meta.fields]
    exclude = ['ID']
    def get_queryset(self, request):
        qs = super(IncreasePointsInfoAdmin, self).get_queryset(request)
        user = User.objects.filter(django_user_id=request.user).first()
        if user:
            city = user.city
            qs = qs.filter(event__city=city)
        return qs
admin.site.register(IncreasePointsInfo, IncreasePointsInfoAdmin)

class TaskApplicationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TaskApplication._meta.fields]
    exclude = ['ID']
    def get_queryset(self, request):
        qs = super(TaskApplicationAdmin, self).get_queryset(request)
        user = User.objects.filter(django_user_id=request.user).first()
        if user:
            city = user.city
            qs = qs.filter(event__city=city)
        return qs

admin.site.register(TaskApplication, TaskApplicationAdmin)









#
# class NotificationAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Notification._meta.fields]
#     exclude = ['ID','decrease','decrease_type','achievement']
#
# admin.site.unregister(Notification)
# admin.site.register(Notification, NotificationAdmin)




#
# class NotificationAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Notification._meta.fields]
#     exclude = ['ID','decrease','decrease_type','achievement']
#
# admin.site.unregister(Notification)
# admin.site.register(Notification, NotificationAdmin)
#
#
#


