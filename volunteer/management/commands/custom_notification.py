from django.core.management.base import BaseCommand, CommandError
from volunteer.models import Event, User
from djgeojson.fields import  PointField

from notifications.signals import notify

from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import AnonymousUser

from volunteer.get_username import current_request



class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):


        django_user = User.objects.get(first_name = "Сашко", last_name="Виконавець").django_user_id

        event_instance = Event.objects.get(name = "Різдвяний ярмарок")

        message = "Доброго дня! Мене звати Ксенія. Я організатор Різдвяного ярмарку. Дякуємо, що відгукнулися стати волонтером. Напишіть, будь ласка, на ksenia.kosyuk@gmail.com або зателефонуйте 0978933516."


        notify.send(
            django_user,
            recipient=django_user,
            verb="custom",
            target=event_instance,
            # timestamp = datetime.datetime.now().strftime("$d %B %Y %h:%m"),
            data={'type': '6', 'message': message},  # Власне сповіщення
        )


