# from volunteer.models import EventsSubscriber, EventsParticipant, User
# from django.contrib.auth.models import User as DjangoUser
# from django.contrib.auth.models import AnonymousUser
# from notifications.signals import notify


def has_changed(instance, field):
    if not instance.pk:
        return False
    old_value = instance.__class__._default_manager.filter(pk=instance.pk).values(field).get()[field]
    return not getattr(instance, field) == old_value


