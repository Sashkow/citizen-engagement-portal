from django.db import models
from django.contrib.auth.models import User as DjangoUser

from volunteer.helpers import has_changed
from notifications.signals import notify

from volunteer.get_username import current_request

from django.contrib.auth.models import AnonymousUser

import datetime

import locale




#RETURN TO VERBOSE_NAME


from citizen_engagement_portal import settings
import os

class EventsType(models.Model):
    type = models.CharField(max_length=80)

    def __str__(self):
        return self.type


class City(models.Model):
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.city

class Rank(models.Model):
    rank = models.CharField(max_length=80)
    quantity_of_points = models.IntegerField()
    city = models.ForeignKey(City, on_delete=models.CASCADE, default='1')

    def __str__(self):
        return '%s %s %s' % (self.rank, '|', self.city)


class User(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    date_of_registration = models.DateField(auto_now_add=True)
    photo = models.ImageField(upload_to=os.path.join(settings.MEDIA_ROOT,'avatars'), null=True, blank=True)
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE, default='2')
    raiting_points = models.IntegerField(default=0)
    city = models.ForeignKey(City, on_delete=models.CASCADE, default='1')
    blocked = models.BooleanField(default=False)
    django_user_id = models.ForeignKey(DjangoUser, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s' % (self.first_name, '|', self.last_name)


class DigestList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(EventsType, on_delete=models.CASCADE)


class District(models.Model):
    district = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s' % (self.district, '|', self.city)


class Event(models.Model):
    name = models.CharField(max_length=300)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    date_event = models.DateTimeField(null=True, blank=True)
    events_type = models.ForeignKey(EventsType, on_delete=models.CASCADE)
    address = models.CharField(max_length=300)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    publication_date = models.DateField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if has_changed(self,'date_event'):
            followers = list(EventsSubscriber.objects.filter(event = self).values_list('user', flat=True))
            participants = list(EventsParticipant.objects.filter(event = self).values_list('user', flat=True))
            print(followers, participants, type(followers), type(participants))
            concerned = list(set(followers) or set(participants))

            for recipient in concerned:
                django_user = User.objects.get(id=recipient).django_user_id
                sender = current_request().user
                if not sender:
                    sender = AnonymousUser()
                # recipient_obj = User.objects.get(id = recipient)
                notify.send(
                    sender,
                    recipient = django_user,
                    verb = 'Час події '+str(self.name) + ' змінено на ' + str(self.date_event.strftime("%d %b %H:%M")) + ". Сповіщення отримано",
                    # timestamp = datetime.datetime.now().strftime("$d %B %Y %h:%m")
                )

            super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return '%s %s %s' % (self.name, '|', self.date_event)



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


class PointsHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateTimeField()
    points = models.IntegerField()
    is_it_org = models.BooleanField()

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