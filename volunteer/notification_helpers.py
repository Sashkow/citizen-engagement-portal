from volunteer.models import NotificationsType, League, TaskApplication, User
from django.shortcuts import reverse
from notifications.models import Notification

def fix(notification):
    if notification.data:
        if  'type' not in notification.data:
            if 'type' in notification.data['data']:
                notification.data = notification.data['data']
    return notification


def get_notification_type(notification):
    if notification.data:
        if 'type' not in notification.data:
            return None

        notification_type_id = notification.data['type']
        if NotificationsType.objects.filter(id=notification_type_id).exists():
            notifiation_type = NotificationsType.objects.get(id=notification_type_id)
            return notifiation_type
    return None



def notification_description(notification):
    notification = fix(notification)
    notification_type = get_notification_type(notification)
    if notification_type:
        if notification_type.id == 1: #Подію змінено
            """{{властивість}} <a class="event-name" get_url="{{лінк}}">{{подія}}</a> змінено з {{було}} на {{стало}}"""
            event = notification.target
            if not event:
                return "Подію сповіщення було видалено."

            property_name = event.__class__._meta.get_field(notification.data['event_field']).verbose_name.title()

            event_url = reverse('volunteer_event',args=(event.id,))
            event_name = event.name
            if 'old_value' in notification.data:
                was = notification.data['old_value']
            else:
                was = '"не має"'
            became = str(getattr(event, notification.data['event_field']))
            description = str(notification_type.template)
            description = description.replace('{{властивість}}',property_name)
            description = description.replace('{{лінк}}', event_url)
            description = description.replace('{{подія}}', event_name)
            description = description.replace('{{було}}', was)
            description = description.replace('{{стало}}', became)
            return description

        elif notification_type.id == 2: # подія потребує допомоги
            event = notification.target
            if not(event):
                description = "Подію сповіщення було видалено"
                return description
            event_url = reverse('volunteer_event', args=(event.id,))
            event_url2 = reverse('form', args=(event.id,))
            event_name = event.name
            description = str(notification_type.template)
            description = description.replace('{{лінк}}', event_url)
            description = description.replace('{{лінк2}}', event_url2)
            description = description.replace('{{подія}}', event_name)
            return description
        elif notification_type.id == 3:  # вітаємо
            profile_edit_url = reverse('profile_edit')
            description = str(notification_type.template)
            description = description.replace('{{лінк}}', profile_edit_url)
            return description
        elif notification_type.id == 4:  # good job
            #Ти класно виконуєш завдання! Так тримати! Отримуєш {{монети}} монеток "{{тип}}" за добрі справи.
            description = str(notification_type.template)
            description = description.replace('{{монети}}', str(notification.data['currency_quantity']))
            description = description.replace('{{тип}}', str(notification.data['currency_type']))
            return description
        elif notification_type.id == 5: # new volunteer to do task
            # {{ім'я}} {{приізвище}} бажає виконати завдання <a class="event-name" get_url="{{лінк}}"> {{завдання}}</a>.
            # Зв’яжіться за поштою {{пошта}} для з’ясування деталей та призначте {{лінк2}} цю людину, якщо ви дійшли згоди.
            # Змінюйте статус події на "Проведено" після виконання завдання.
            event = notification.target
            recipient = notification.recipient
            sender  = notification.actor
            if sender == None:
                return "Акаунт відправника сповіщення було видалено"
            event_url = reverse('volunteer_event', args=(event.id,))
            event_edit_url = reverse('form', args=(event.id,))
            task_application = TaskApplication.objects.filter(user__django_user_id=sender, event=event)
            if task_application.exists():
                mail = task_application[0].contact
            else:
                mail = '"заявку скасовано"'

            sender_user = User.objects.filter(django_user_id = sender)
            if sender_user.exists():
                sender_user = sender_user[0]
            else:
                sender_user=sender

            description = str(notification_type.template)
            description = description.replace("{{ім'я}}", str(sender_user.first_name))
            description = description.replace("{{прізвище}}", str(sender_user.last_name))
            description = description.replace("{{пошта}}", str(mail))
            description = description.replace("{{лінк}}", str(event_url))
            description = description.replace("{{завдання}}", str(event.name))
            description = description.replace("{{лінк2}}", str(event_edit_url))
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
            if notification.target:
                image = notification.target.events_type.image.url
                return image

        if notifiation_type.id == 2: # подія потребує допомоги
            if notification.target:
                image = notification.target.events_type.image.url
                return image

        if notifiation_type.id == 3: # welcome
            image = League.objects.get(league="Пластикова ліга").league_image.url
            return image

        if notifiation_type.id == 4: # good job
            if notification.target:
                image = notification.target.events_type.image.url
                return image

        if notifiation_type.id == 5:  # new volunteer for task
            if notification.target:
                image = notification.target.events_type.image.url
                return image


    return ""