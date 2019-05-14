from django.core.management.base import BaseCommand, CommandError
from volunteer.models import EventsSubscriber, EventsParticipant, TaskApplication, Event
from djgeojson.fields import  PointField
from geopy.geocoders import Nominatim
import random
import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        EventsSubscriber.objects.all().delete()
        EventsParticipant.objects.all().delete()
        TaskApplication.objects.all().delete()