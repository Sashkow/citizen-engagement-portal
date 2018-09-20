
from django.contrib.auth.models import User as DjangoUser
from volunteer.models import User as VolunteerUser
def save_user_name(backend, user, response, *args, **kwargs):
    first_name = backend.strategy.session_get('first_name')
    second_name = backend.strategy.session_get('second_name')

    django_user = user
    if not VolunteerUser.objects.filter(django_user_id=django_user).exists():
        volunteer = VolunteerUser.objects.create(django_user_id = django_user)
        
    elif len(VolunteerUser.objects.filter(django_user_id=django_user))> 1:
        print("User Duplicates!")
        return None #404
    else:
        volunteer = VolunteerUser.objects.get(django_user_id=django_user)

    if first_name or second_name:
        volunteer.first_name = first_name
        volunteer.second_name = second_name

    elif not volunteer.first_name:
        if django_user.first_name or django_user.last_name:
            volunteer.first_name = django_user.first_name
            volunteer.second_name = django_user.last_name

    volunteer.save()
