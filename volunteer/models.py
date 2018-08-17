from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.forms.models import model_to_dict


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

    def __str__(self):
        return '%s %s %s' % (self.name, '|', self.date_event)

    def as_dict(self):
        return model_to_dict(self)




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

    def as_dict(self):
        return model_to_dict(self)


    def __str__(self):
        return self.photo.path


    def get_url(self):
        return self.photo.url
