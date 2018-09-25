from django.core.management.base import BaseCommand, CommandError
from volunteer.models import Event
from schedule.models import Calendar
from schedule.models import Event as CalendarEvent

import datetime


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        calendar_name = 'volunteer_calendar'
        calendar_slug = 'volunteer_calendar_slug'
        if Calendar.objects.filter(name = calendar_name).exists():
            Calendar.objects.filter(name = calendar_name).delete()
            Calendar.objects.create(name=calendar_name)

        calendar = Calendar.objects.create(name=calendar_name, slug = calendar_slug)




        events = Event.objects.all()

        i = 0

        for event in events:
            i+=1
            if event.date_event:
                data = {
                    'title': event.name,
                    'start': event.date_event,
                    'end': datetime.datetime(event.date_event.year,event.date_event.month, event.date_event.day, 23, 59),
                    # 'end_recurring_period': datetime.datetime(today.year + 30, 6, 1, 0, 0),
                    # 'rule': rule,
                    'calendar': calendar
                }
                CalendarEvent.objects.create(**data)
                # calendar_event.save()
                print(i, event)