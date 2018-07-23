from django.db import models


#RETURN TO VERBOSE_NAME

class EventsType(models.Model):
    type = models.CharField(max_length=80)


class City(models.Model):
    city = models.CharField(max_length=100)


class Rank(models.Model):
    rank = models.CharField(max_length=80)
    quantity_of_points = models.IntegerField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)


class User(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    date_of_registration = models.DateField(auto_now_add=True)
    photo = models.ImageField(null=True, blank=True)
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE)
    raiting_points = models.IntegerField(default=0)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    blocked = models.BooleanField(default=False)




class DigestList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(EventsType, on_delete=models.CASCADE)


class District(models.Model):
    district = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

class Event(models.Model):
    name = models.CharField(max_length=300)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    date_event = models.DateTimeField(null=True, blank=True)
    events_type = models.ForeignKey(EventsType, on_delete=models.CASCADE)
    address = models.CharField(max_length=300)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    publication_date = models.DateField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)


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
    photo = models.ImageField()
    is_it_cover = models.BooleanField(default=False)