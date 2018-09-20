from background_task import background
from logging import getLogger
from notifications import signals
from volunteer.models import Event, EventsParticipant, EventsSubscriber, User
import datetime


from django.utils.timezone import localtime, now

logger = getLogger(__name__)

# def notify_event_soon(event_id):
#     if Event.objects.filter(id=event_id).exists():
#         event_instance = Event.objects.get(id=event_id)
#     else:
#         return None
#
#
#     # if event_instance.status.status == 'Готова до проведення' and event_instance.date_event
#
#     followers = list(EventsSubscriber.objects.filter(event=event_instance).values_list('user', flat=True))
#     participants = list(EventsParticipant.objects.filter(event=event_instance).values_list('user', flat=True))
#     print(followers, participants, type(followers), type(participants))
#     concerned = list(set(followers) or set(participants))
#
#     for recipient in concerned:
#         django_user = User.objects.get(id=recipient).django_user_id
#         sender = current_request().user
#         if not sender:
#             sender = AnonymousUser()
#         # recipient_obj = User.objects.get(id = recipient)
#
#         notify.send(
#             sender,
#             recipient=django_user,
#             verb="is_soon",
#             target = event_instance,
#             # timestamp = datetime.datetime.now().strftime("$d %B %Y %h:%m"),
#             data = {'type':'2',}, # Подія наближається
#         )
#
#
# @background(schedule=15)
# def schedule_notification(message):
#
#     signals.notify()
#     """Check whether some event is ended and we need to send peer-review notification"""
#     print("checking", message)
#     logger.debug('demo_task. message={0}'.format(message))
