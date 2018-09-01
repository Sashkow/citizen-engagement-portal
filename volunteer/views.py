# from django.shortcuts import render
# from django.http import HttpResponse
# from django.contrib.auth.decorators import login_required
#
# # Create your views here.
#
#
# @login_required
# def index(request):
#     return render(request, 'index.html')
#     # return HttpResponse('ok, Google')

from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import datetime


from volunteer.models import *

from volunteer.forms import NewEventForm

from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse
from django.template import loader, Context
from django.template.loader import render_to_string
from .functionviews import *
import json

from django.template import RequestContext

# @login_required
# def home(request):
#     return render(request, 'core/home.html')

events_per_page = 1


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1')
            )
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def home(request):
    if request.user.is_authenticated:
        return redirect(reverse('profile'))
    else:
        return redirect(reverse('login'))

@login_required
def profile(request):
    session_key = request.session.session_key
    django_user = request.user
    volunteer = User.objects.filter(django_user_id = django_user)
    status = Status.objects.filter(id__range = (1, 2))
    if len(volunteer) == 0:
        volunteer = User.objects.create(django_user_id = django_user)
    elif len(volunteer)> 1:
        print("Duplicates!")
        return None
    else:
        volunteer = volunteer.first()

    if django_user.first_name:
        name = django_user.first_name
    elif django_user.username:
        name = django_user.username
    else:
        name = "Волонтер_ка"

    parameters = ['all', 1]
    events, events_part, events_subs, events_quantity = get_events(Event, User, EventsSubscriber, EventsParticipant, EventsPhoto, django_user, events_per_page, parameters, EventsType)
    pages, pages_range = get_pages_number(events_quantity, events_per_page, 1)

    types_events = EventsType.objects.all()

    return render(request, 'core/profile.html', {'volunteer':volunteer,
                                                 'name':name,
                                                 'events':events,
                                                 'events_subs':events_subs,
                                                 'events_part':events_part,
                                                 'types_events':types_events,
                                                 'current':1,
                                                 'pages':pages_range,
                                                 'pages_max': pages,
                                                 'status':status})

def event(request, id):
    try:
        the_event = Event.objects.get(pk=id)
        following = len(EventsSubscriber.objects.filter(event = the_event))
        going = len(EventsParticipant.objects.filter(event = the_event))
        photos = EventsPhoto.objects.filter(event=the_event)

        return render(request, 'event.html', {
            'event' : the_event,
            'following': following,
            'going': going,
            'photos': photos
        })
    except ObjectDoesNotExist:
        return HttpResponse("event with id:{} not found".format(id))


@login_required
def new_event(request):

    data = request.POST
    date = check_key_in_dict('date', data)

    if date != None:
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()

    status = check_key_in_dict_int('status', data)
    if status != None:
        status_i = Status.objects.get(id = check_key_in_dict_int('status', data))
    else:
        status_i = None
    events_or_task = True if check_key_in_dict('type', data) == 'event' else False


    new_event_v  = Event.objects.create(
        name = check_key_in_dict('name', data),
        organizer = User.objects.get_or_create(django_user_id = request.user)[0],
        events_or_task = events_or_task,
        events_type = EventsType.objects.get(id = check_key_in_dict_int('category', data)),
        date_event = date,
        city = City.objects.get(id=1),
        address = check_key_in_dict('address', data),
        status = status_i,
        max_part = check_key_in_dict_int('from', data),
        min_part = check_key_in_dict_int('to', data),
        recommended_points = check_key_in_dict_int('points_quant', data),
        contact = check_key_in_dict('email', data),
        description = check_key_in_dict('description_e', data)
    )
    if status == 1:
        nmb = check_key_in_dict_int('numb', data)
        for i in range(nmb):
            str_name = 'task_arr['+str(i)+'][name_task]'
            str_points = 'task_arr['+str(i)+'][point_task]'
            str_descr = 'task_arr['+str(i)+'][descr_task]'

            name_task = request.POST.get(str_name)
            points_task = int(request.POST.get(str_points))
            descr_task = request.POST.get(str_descr)

            EventsOrgTask.objects.create(
                event = Event.objects.get(id = new_event_v.id),
                task_name = name_task,
                task_description = descr_task,
                recommended_points = points_task

            )
        print(nmb)
    return_dict  ={}
    return JsonResponse(return_dict)


@login_required
def follow_event(request):
    return_dict = dict()
    data = request.POST
    result = int(data['id_event'].replace(',', '').replace(' ',''))
    user_db = User.objects.get(django_user_id = request.user)
    if int(data['add']) == 1:
        EventsSubscriber.objects.create(user = user_db, event = Event.objects.get(id = result))
    else:
        EventsSubscriber.objects.filter(user = user_db, event = Event.objects.get(id = result)).delete()

    return JsonResponse(return_dict)

def subscribe_event(request):
    return_dict = dict()
    data = request.POST
    result = int(data['id_event'].replace(',', '').replace(' ',''))
    user_db = User.objects.get(django_user_id = request.user)
    if int(data['add']) == 1:
        EventsParticipant.objects.create(user = user_db, event = Event.objects.get(id = result))
    else:
        EventsParticipant.objects.filter(user = user_db, event = Event.objects.get(id = result)).delete()

    return JsonResponse(return_dict)


def type_filter(request):
    return_dict = {}
    django_user = request.user
    data = request.GET
    parametrs = [data['type'], data['page']]
    print(parametrs)

    if data['type']!= 'all' and  not Event.objects.filter(events_type=EventsType.objects.get(id=data['type'])).exists():
        return JsonResponse(return_dict)
    else:
        events, events_part, events_subs, events_quantity = get_events(Event, User, EventsSubscriber, EventsParticipant, EventsPhoto, django_user, events_per_page, parametrs, EventsType)
        types_events = EventsType.objects.all()
        pages, pages_range = get_pages_number(events_quantity, events_per_page, parametrs[1])
        cont = {
            'events': events,
            'events_subs': events_subs,
            'events_part': events_part,
            'types_events': types_events,
            'pages': pages_range,
            'pages_max': pages,
            'current':int(parametrs[1]),
            'request': request
        }
        html = render_to_string('events_result.html', cont)
        return_dict = {'html': html}
        return JsonResponse(return_dict)

