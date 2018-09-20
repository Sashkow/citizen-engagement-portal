from volunteer.models import NotificationsType
from django.shortcuts import reverse
from notifications.models import Notification

def get_notification_type(notification):
    if notification.data:
        if  'type' not in notification.data:
            if 'type' in notification.data['data']:
                notification.data = notification.data['data']
            else:
                return None

        notification_type_id = notification.data['type']
        if NotificationsType.objects.filter(id=notification_type_id).exists():
            notifiation_type = NotificationsType.objects.get(id=notification_type_id)
            return notifiation_type
    return None



def notification_description(notification):
    notifiation_type = get_notification_type(notification)
    if notifiation_type:
        if notifiation_type.id == 1: #Подію змінено
            """{{властивість}} <a class="event-name" get_url="{{лінк}}">{{подія}}</a> змінено з {{було}} на {{стало}}"""
            event = notification.target
            property_name = event.__class__._meta.get_field(notification.data['event_field']).verbose_name.title()
            event_url = reverse('event',args=(event.id,))
            event_name = event.name
            if 'old_value' in notification.data:
                was = notification.data['old_value']
            else:
                was = '"не має"'
            became = str(getattr(event, notification.data['event_field']))
            description = str(notifiation_type.template)
            description = description.replace('{{властивість}}',property_name)
            description = description.replace('{{лінк}}', event_url)
            description = description.replace('{{подія}}', event_name)
            description = description.replace('{{було}}', was)
            description = description.replace('{{стало}}', became)
            return description

    else:
        print("unknown notification type")
        return "Невідома подія"

def notification_title(notification):
    notifiation_type = get_notification_type(notification)
    if notifiation_type:
        return notifiation_type.title


    return "Сповіщення"

def notification_image(notification):
    notifiation_type = get_notification_type(notification)
    if notifiation_type:
        if notifiation_type.id == 1: # Подію змінено
            image = notification.target.events_type.image.url
            return image

    return ""






