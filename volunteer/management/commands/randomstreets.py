from django.core.management.base import BaseCommand, CommandError
from volunteer.models import Event
from djgeojson.fields import  PointField
from geopy.geocoders import Nominatim
import random
import time

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        events = Event.objects.all()
        total = len(events)
        view_box = [(49.4770, 26.9048), (49.3631, 27.0995)]  # khmelnitsky city
        nom = Nominatim(user_agent="changer.in.ua", view_box=view_box, bounded=True)
        # if self.city:
        #     city = self.city.city
        # else:
        #     city = City.DEFAULT_CITY
        i = 0

        for event in events:
            i+=1
            print("event",i,'of',total)
            latitude = random.uniform(view_box[0][0],view_box[1][0])
            longtitude = random.uniform(view_box[0][1], view_box[1][1])

            address = nom.reverse((latitude,longtitude))
            event.address = address.address
            print(address)
            event.save()
            time.sleep(2)