from django.contrib import admin
from .models import *


admin.site.empty_value_display = '(None)'


class EventsTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EventsType._meta.fields]
    exclude = ['id']

admin.site.register(EventsType, EventsTypeAdmin)



class CityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in City._meta.fields]
    exclude = ['_id']

admin.site.register(City, CityAdmin)



class RankAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Rank._meta.fields]
    exclude = ['Id']
admin.site.register(Rank, RankAdmin)



class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.fields]
    exclude = ['rating_points', 'blocked', 'ID']
    list_filter = ['rank', 'city', 'blocked']
    search_fields = ['first_name', 'last_name']

admin.site.register(User, UserAdmin)



class DigestListAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DigestList._meta.fields]
    exclude = ['ID']
    list_filter = ['type']

admin.site.register(DigestList, DigestListAdmin)


class DistrictAdmin(admin.ModelAdmin):
    list_display = [field.name for field in District._meta.fields]
    exclude = ['ID']
    list_filter = ['city']
    search_fields = ['district']

admin.site.register(District, DistrictAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Event._meta.fields]
    exclude = ['ID']
    list_filter = ['events_type', 'district']
    fieldsets = (
        (None, {
            'fields': ('name', 'organizer', 'date_event', 'events_type',)
        }),
        ('Address', {
            'fields': ('district', 'address',)
        }),
        ('Description', {
            'classes': ('collapse',),
            'fields' : ('description',),
        })
    )
    search_fields = ['name']

admin.site.register(Event, EventAdmin)

class EventsSubscribrsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EventsSubscriber._meta.fields]
    exclude = ['ID']
admin.site.register(EventsSubscriber, EventsSubscribrsAdmin)

class EventsPartcipiantAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EventsParticipant._meta.fields]
    exclude = ['ID']
admin.site.register(EventsParticipant, EventsPartcipiantAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.fields]
    exclude = ['ID']
admin.site.register(Comment, CommentAdmin)

class ReportAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Report._meta.fields]
    exclude = ['ID']
admin.site.register(Report, ReportAdmin)

class PointsHistoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PointsHistory._meta.fields]
    exclude = ['ID']
admin.site.register(PointsHistory, PointsHistoryAdmin)

class EventsPhotoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EventsPhoto._meta.fields]
    exclude = ['ID']
admin.site.register(EventsPhoto, EventsPhotoAdmin)


















