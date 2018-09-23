from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.forms.models import model_to_dict
from notifications.models import Notification

from volunteer.helpers import has_changed
from notifications.signals import notify

# from notifications.models import Notification
# Notification.data

from volunteer.get_username import current_request

from django.contrib.auth.models import AnonymousUser

from babel.dates import format_datetime

from copy import deepcopy






import datetime

import locale




#RETURN TO VERBOSE_NAME


from citizen_engagement_portal import settings
import os


from django.db.models.signals import pre_save, post_save, post_init
from django.dispatch import receiver






def notify_event_changes(event_instance, event_field, old_value):
    followers = list(EventsSubscriber.objects.filter(event=event_instance).values_list('user', flat=True))
    participants = list(EventsParticipant.objects.filter(event=event_instance).values_list('user', flat=True))
    print(followers, participants, type(followers), type(participants))
    concerned = list(set(followers) or set(participants))

    for recipient in concerned:
        django_user = User.objects.get(id=recipient).django_user_id
        sender = current_request().user
        if not sender:
            sender = AnonymousUser()
        # recipient_obj = User.objects.get(id = recipient)

        event_field_verbose_name = Event._meta.get_field(event_field).verbose_name.title()
        if event_field == 'date_event':
            event_field_value = format_datetime(getattr(event_instance, event_field), locale='uk_UA')
        else:
            event_field_value = getattr(event_instance, event_field)

        notify.send(
            sender,
            recipient=django_user,
            verb="changed",
            target = event_instance,
            # timestamp = datetime.datetime.now().strftime("$d %B %Y %h:%m"),
            data = {'type':'1', 'event_field':event_field, 'old_value' : old_value}, # Подію змінено
        )

# class NotificationType(models.Model):
#     type = models.CharField(max_length=80)


class EventsType(models.Model):
    type = models.CharField(max_length=80)
    image = models.FileField(upload_to=os.path.join(settings.MEDIA_ROOT,'achievements',), null=True, blank=True)

    def __str__(self):
        return self.type

class Status(models.Model):
    status = models.CharField(max_length=80)
    frontend_value = models.CharField(max_length=80, null=True, blank=True)
    color_background = models.CharField(max_length = 13, null=True, blank=True)
    image = models.FileField(upload_to=os.path.join(settings.MEDIA_ROOT,'status',), null=True, blank=True)

    def __str__(self):
        return self.status

class City(models.Model):
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.city


class League(models.Model):
    DEFAULT_PK = 1
    league = models.CharField(max_length = 80)
    quantity_achievement  =models.IntegerField()
    league_image = models.FileField(upload_to=os.path.join(settings.MEDIA_ROOT,'achievements'),null=True, blank=True)
    user_frame = models.FileField(upload_to=os.path.join(settings.MEDIA_ROOT,'achievements'),null=True, blank=True)
    background_color = models.CharField(max_length =20, null=True, blank=True)
    background_image = models.FileField(upload_to=os.path.join(settings.MEDIA_ROOT,'profile_backgrounds'), null=True, blank=True)
    color_league_txt = models.CharField(max_length =20, null=True, blank=True)
    color_volunteer_name = models.CharField(max_length =20, null=True, blank=True)
    color_menu_item = models.CharField(max_length =20, null=True, blank=True)
    color_current_grad1 = models.CharField(max_length =20, null=True, blank=True)
    color_current_grad2 = models.CharField(max_length =20, null=True, blank=True)
    color_current_text = models.CharField(max_length =20, null=True, blank=True)
    color_current_border = models.CharField(max_length =20, null=True, blank=True)

    def __str__(self):
        return self.league


class User(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    date_of_registration = models.DateField(auto_now_add=True)
    photo = models.ImageField(upload_to=os.path.join(settings.MEDIA_ROOT,'avatars'), null=True, blank=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE, null=True, blank=True, default=League.DEFAULT_PK)
    city = models.ForeignKey(City, on_delete=models.CASCADE, default='1')
    blocked = models.BooleanField(default=False)
    django_user_id = models.ForeignKey(DjangoUser, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        is_new_user = False
        if self.pk is None:
            is_new_user = True

        super(User, self).save(*args, **kwargs)

        if is_new_user:
            currencies = Currency.objects.all()
            for currency in currencies:
                UserPoint.objects.create(user=self, # sosal
                                         currency=currency,
                                         quantity=0)

            events_type = EventsType.objects.all()
            for type_e in events_type:
                DigestList.objects.create(
                    user=self,
                    type=type_e
                )

    def __str__(self):
        return '%s %s %s' % (self.first_name, '|', self.last_name)


class DigestList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(EventsType, on_delete=models.CASCADE)



class Event(models.Model):
    name = models.CharField(max_length=300)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    events_or_task = models.BooleanField(default=True)
    events_type = models.ForeignKey(EventsType, on_delete=models.CASCADE)
    date_event = models.DateTimeField(null=True, blank=True, verbose_name='Час')
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE,  null=True, blank=True, verbose_name='Статус')
    max_part = models.IntegerField(null=True, blank=True)
    min_part = models.IntegerField(null=True, blank=True)
    recommended_points = models.IntegerField()
    contact = models.EmailField(null=True, blank=True)
    publication_date = models.DateField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)


    def save(self, *args, **kwargs):
        is_new_event = False
        if self.pk is None:
            is_new_event = True
        else:
            old_instance = Event.objects.get(pk = self.pk)
            old_status = old_instance.status.id
            old_type = old_instance.events_type.id
            currency = Currency.objects.get(type_event__id=old_type)

        super(Event, self).save(*args, **kwargs)

        if not is_new_event and self.status.id == 3 and old_status!=self.status.id:
            part = list(EventsParticipant.objects.filter(event = Event.objects.get(pk = self.pk)).values_list('user__id', flat = True))
            part_user = User.objects.filter(id__in = part)

            for user in part_user:
                points_list = PointsList.objects.create(user = user, currency = currency, points_quantity = self.recommended_points)
                IncreasePointsInfo.objects.create(increase = points_list, increase_type_id = 1,  event_id = self.id)
                user_points = UserPoint.objects.get(user = user, currency = currency)
                user_points.quantity +=  self.recommended_points
                user_points.save()

            if len(part_user)>=3 and self.events_or_task == True:
                points_list = PointsList.objects.create(user = self.organizer, currency = currency, points_quantity = self.recommended_points)
                IncreasePointsInfo.objects.create(increase=points_list, increase_type_id=2, event_id=self.id)
                user_points = UserPoint.objects.get(user=self.organizer, currency=currency)
                user_points.quantity += 30
                user_points.save()
            elif self.events_or_task == False:
                points_list = PointsList.objects.create(user=self.organizer, currency=currency,points_quantity=self.recommended_points)
                IncreasePointsInfo.objects.create(increase=points_list, increase_type_id=2, event_id=self.id)
                user_points = UserPoint.objects.get(user=self.organizer, currency=currency)
                user_points.quantity += 30
                user_points.save()

            print('It is victory!')



    def __str__(self):
        return '%s %s %s' % (self.name, '|', self.date_event)

    def as_dict(self):
        return model_to_dict(self)


@receiver(pre_save, sender=Event)
def eventpresave(sender, **kwargs):
    instance = kwargs['instance']
    if instance.pk:
        instance._old_date_event = deepcopy(Event.objects.get(pk = instance.pk).date_event)
        instance._old_status = deepcopy(Event.objects.get(pk = instance.pk).status)
        print("pre_save")


@receiver(post_save, sender=Event)
def eventpostsave(sender, **kwargs):
    instance = kwargs['instance']
    if not kwargs['created']:
        print(instance.date_event, instance._old_date_event)
        if instance.date_event != instance._old_date_event:
            notify_event_changes(instance, 'date_event', str(instance._old_date_event))
            print("date has changed!")

        if instance.status != instance._old_status:
            notify_event_changes(instance, 'status', str(instance._old_status))
            print("sttus has changed!")
    print("post_save")


class EventsOrgTask(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=80)
    task_description = models.TextField(null=True, blank=True)
    done = models.BooleanField(default=False)
    canceled = models.BooleanField(default = False)
    recommended_points = models.IntegerField()

class EventsSubscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("user", "event"),)


class EventsParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("user", "event"),)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    class Meta:
        unique_together = (("user", "event", "date"),)


class Report(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from+")
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to+")
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = (("user_from", "user_to"),)


class EventsPhoto(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=os.path.join(settings.MEDIA_ROOT,'event_images'),)
    is_it_cover = models.BooleanField(default=False)

    def as_dict(self):
        return model_to_dict(self)


    def __str__(self):
        return self.photo.path


    def get_url(self):
        return self.photo.url

#NEW FOTS

# League

class Currency(models.Model):
    currency = models.CharField(max_length = 80)
    type_event = models.ForeignKey(EventsType, on_delete = models.CASCADE)
    image = models.FileField(upload_to=os.path.join(settings.MEDIA_ROOT,'currency'),)

    def __str__(self):
        return self.currency

class UserPoint(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete = models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('user', 'currency',)

class Achievement(models.Model):
    achievement = models.CharField(max_length = 200)
    league = models.ForeignKey(League, on_delete = models.CASCADE)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to=os.path.join(settings.MEDIA_ROOT,'achievements'),null=True, blank=True)
    background_achieve = models.CharField(max_length = 15, null=True, blank=True)
    color_text_achieve = models.CharField(max_length = 15, null=True, blank=True)



    def __str__(self):
        return self.achievement

class AchievementValue(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete = models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete = models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('achievement', 'currency',)


class UserAchievement(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    class Meta:
        unique_together = ('achievement', 'user',)

class PointsList(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    date = models.DateField(auto_now_add=True)
    currency = models.ForeignKey(Currency, on_delete = models.CASCADE)
    increase = models.BooleanField(default = True)
    points_quantity = models.IntegerField()

class IncreasePointsType(models.Model):
    increase_type = models.CharField(max_length = 100)

    def __str__(self):
        return self.increase_type

class DecreasePointsType(models.Model):
    decrease_type = models.CharField(max_length = 100)

    def __str__(self):
        return self.decrease_type

class IncreasePointsInfo(models.Model):
    increase = models.ForeignKey(PointsList, on_delete = models.CASCADE)
    increase_type = models.ForeignKey(IncreasePointsType, on_delete = models.CASCADE)
    event = models.ForeignKey(Event, on_delete = models.CASCADE)

class DecreasePointsInfo(models.Model):
    decrease = models.ForeignKey(PointsList, on_delete = models.CASCADE)
    decrease_type = models.ForeignKey(DecreasePointsType, on_delete = models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete = models.CASCADE)

class NotificationsType(models.Model):
    title = models.CharField(max_length = 100)
    template = models.TextField(null=True, blank=True)
    model_name = models.CharField(max_length = 100)
    image_field_name = models.CharField(max_length = 100)

class Tupo(models.Model):
    f = models.CharField(max_length=100)

    # model_name = 'Invoice'
    # app_name = 'invoice'
    # from django.apps import apps
    # Invoice = apps.get_model(app_label=app_name, model_name=model_name)
    # i = Invoice.objects.filter(id=1234).first()

#
# class Notification(object):
#     notification_type = models.ForeignKey(NotificationType, on_delete = models.CASCADE)
#     sender = models.ForeignKey(User, on_delete = models.CASCADE)
#     recipient = models.ForeignKey(User, on_delete=models.CASCADE)
#     is_read = models.BooleanField(default=False)
#     timestamp = models.DateTimeField(null=True, blank=True, verbose_name='Отримано')

#
#
#
#     def description(self):
#         if self.notification_type.title == 'Оцініть подію':
#             pass
#             # from model_name get fields and insert
#
#     def image(self):
#         pass
#         # from model_name get image_field_name, return url








class NotificaationType(models.Model):
    title = models.CharField(max_length = 100)
    template = models.TextField(null=True, blank=True)
    model_name = models.CharField(max_length = 100)
    image_field_name = models.CharField(max_length = 100)

#def user_post_save(sender, instance, **kwargs):
#
#    if kwargs['created']:
#        django_user = instance
#        volunteer = User.objects.create(django_user_id=django_user)
#
#        if not volunteer.first_name:
#            if django_user.first_name or django_user.last_name:
#                volunteer.first_name = django_user.first_name
#                volunteer.second_name = django_user.last_name
#
#        volunteer.save()
#
#models.signals.post_save.connect(user_post_save, sender=DjangoUser)



