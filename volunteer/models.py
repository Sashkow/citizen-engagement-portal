from django.db import models


#RETURN TO VERBOSE_NAME

class Events_type(models.Model):
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
    foto = models.ImageField(null=True)
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE)
    raiting_points = models.IntegerField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    blocked = models.BooleanField(default=False)

    def __str__(self):
        return  '%s %s' % (self.first_name, self.last_name)



class Digest_list(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(Events_type, on_delete=models.CASCADE)




class Event(models.Model):
    name = models.CharField(max_length=200)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    date_event = models.DateTimeField()
    events_type = models.ForeignKey(Events_type, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    # district = models.ForeignKey()
    publication_date = models.DateField(auto_now_add=True)
    description = models.TextField(null=True)

    def __str__(self):
        return '%s %s' % (self.name, self.date_event)


class Events_subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("user", "event"),)



class Events_participant(models.Model):
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




class Points_history(models.Model):
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


class Events_foto(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    foto = models.ImageField()
    is_it_cover = models.BooleanField(default=False)