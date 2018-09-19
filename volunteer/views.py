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
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.http import HttpResponseForbidden

from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Max
from .forms import EditeEventForm
import datetime


from volunteer.models import *

from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse

from django.template import loader, Context
from django.template.loader import render_to_string
from .functionviews import *
import json

from django.template import RequestContext


import random

import json

from django.contrib.auth.decorators import login_required
from notifications.signals import notify

@login_required
def live_tester(request):
    # notify.send(sender=request.user, recipient=request.user, verb='you loaded the page')

    return render(request, 'test_live.html', {
        'unread_count': request.user.notifications.unread().count(),
        'notifications': request.user.notifications.all()
    })


def make_notification(request):
    the_notification = random.choice([
        'reticulating splines',
        'cleaning the car',
        'jumping the shark',
        'testing the app',
        'attaching the plumbus',
    ])

    notify.send(sender=request.user, recipient=request.user,
                verb='you asked for a notification - you are ' + the_notification)


def mark_all_as_read(request):
    user = request.user
    user.notifications.mark_all_as_read()


events_per_page = 6


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

    parameters = ['all_digest', 1, 'news']
    events, events_part, events_subs, events_quantity, events_org = get_events(Event, User, DigestList, EventsSubscriber, EventsParticipant, EventsPhoto, django_user, events_per_page, parameters, EventsType)
    pages, pages_range = get_pages_number(events_quantity, events_per_page, 1)

    league_user = League.objects.get(id = volunteer.league_id)
    achievements_league_list = list(Achievement.objects.filter(league = league_user).values_list('id', flat = True))
    achieve_quant = UserAchievement.objects.filter(user = volunteer, achievement_id__in = achievements_league_list).count()
    user_points = UserPoint.objects.filter(user = volunteer).select_related('currency')
    max_user_point = user_points.aggregate(Max('quantity'))

    types_events = EventsType.objects.all()

    curr_category = {}
    for type_e in types_events:
        img = Currency.objects.get(type_event = type_e.id).image.url
        curr_category[type_e.id] = img
    return render(request, 'core/profile.html', {'volunteer':volunteer,
                                                 'league_user':league_user,
                                                 'name':name,
                                                 'events':events,
                                                 'events_subs':events_subs,
                                                 'events_part':events_part,
                                                 'current':1,
                                                 'pages':pages_range,
                                                 'pages_max': pages,
                                                 'status':status,
                                                 'achieve_quant':achieve_quant,
                                                'unread_count': request.user.notifications.unread().count(),
                                                'notifications': request.user.notifications.all(),
                                                'types_events':types_events,
                                                 'events_org':events_org,
                                                 'user_points':user_points,
                                                 'max_points': max_user_point['quantity__max'],
                                                 'curr_category':curr_category
    })

def event(request, id):
    try:
        django_user = request.user
        volunteer = User.objects.get(django_user_id=django_user)
        the_event = Event.objects.get(pk=id)
        following = len(EventsSubscriber.objects.filter(event = the_event))
        going = len(EventsParticipant.objects.filter(event = the_event))
        photos = EventsPhoto.objects.filter(event=the_event)
        absolute_url = request.build_absolute_uri(reverse('event', args=(id,)))
        types_events = EventsType.objects.all()

        curr_category = {}
        for type_e in types_events:
            img = Currency.objects.get(type_event=type_e.id).image.url
            curr_category[type_e.id] = img
        if the_event.organizer == volunteer:
            org_user = 1
        else:
            org_user = 0
        if EventsSubscriber.objects.filter(event=the_event, user = volunteer).exists():
            subscribe = 1
        else:
            subscribe = 0
        if EventsParticipant.objects.filter(event = the_event, user = volunteer).exists():
            part = 1
        else:
            part = 0
        cont = {
            'curr_category':curr_category,
            'org_user':org_user,
            'request': request,
            'event': the_event,
            'following': following,
            'going': going,
            'photos': photos,
            'absolute_url': absolute_url,
            'subscribe':subscribe,
            'part':part
            }
        html = render_to_string('event_copy.html', cont)
        return_dict = {'html': html}
        return JsonResponse(return_dict)
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
        status_i = Status.objects.get(id = 1)
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
        EventsSubscriber.objects.filter(user = user_db, event = Event.objects.get(id = result)).delete()
        EventsParticipant.objects.create(user = user_db, event = Event.objects.get(id = result))
    else:
        EventsParticipant.objects.filter(user = user_db, event = Event.objects.get(id = result)).delete()
    #
    return JsonResponse(return_dict)


def type_filter(request):
    return_dict = {}
    django_user = request.user
    data = request.GET
    print(data)
    parametrs = [data['type'], data['page'], data['state']]
    types_events = EventsType.objects.all()
    print(parametrs)
    curr_category = {}
    for type_e in types_events:
        img = Currency.objects.get(type_event=type_e.id).image.url
        curr_category[type_e.id] = img
    if data['type'] not in ['all', 'all_digest'] and  not Event.objects.filter(events_type=EventsType.objects.get(id=data['type'])).exists():
        return JsonResponse(return_dict)
    else:
        events, events_part, events_subs, events_quantity, events_org = get_events(Event, User, DigestList, EventsSubscriber, EventsParticipant, EventsPhoto, django_user, events_per_page, parametrs, EventsType)
        types_events = EventsType.objects.all()
        pages, pages_range = get_pages_number(events_quantity, events_per_page, parametrs[1])
        cont = {
            'curr_category':curr_category,
            'events': events,
            'events_subs': events_subs,
            'events_part': events_part,
            'types_events': types_events,
            'pages': pages_range,
            'pages_max': pages,
            'current':int(parametrs[1]),
            'request': request,
            'selected':data['type'],
            'events_org': events_org
        }
        html = render_to_string('events_result.html', cont)
        return_dict = {'html': html}
        return JsonResponse(return_dict)


def profile_edit(request):
    django_user = request.user
    current_user = User.objects.get(django_user_id=django_user)
    if request.method == 'POST':
        return_dict = {}
        data = request.POST
        types = EventsType.objects.all()
        types = [id.id for id in types]
        for i in types:
            print(data[str(i)])
            if data[str(i)] == 'true' and not DigestList.objects.filter(user = current_user, type = EventsType.objects.get(id = i)).exists():
                print('in')
                DigestList.objects.create(user = current_user, type = EventsType.objects.get(id = i))
            elif data[str(i)] == 'false' and DigestList.objects.filter(user = current_user, type = EventsType.objects.get(id = i)).exists():
                print('out')
                DigestList.objects.filter(user=current_user, type=EventsType.objects.get(id=i)).delete()

        return JsonResponse(return_dict)
    else:
        dict_digest = {}
        type_events = EventsType.objects.all()
        for i in type_events:
            if DigestList.objects.filter(user = current_user, type = i).exists():
                dict_digest[i.id] = 1
            else:
                dict_digest[i.id] = 0
        cont = {'user':current_user,
                 'type_events': type_events,
                 'dict_digest':dict_digest}
        html = render_to_string('edit_profile.html', cont)
        return_dict = {'html': html}
        return JsonResponse(return_dict)

def get_achivments(request):

    if request.method == 'GET':
        django_user = request.user
        current_user = User.objects.get(django_user_id=django_user)
        leagues = League.objects.all()
        current_league = current_user.league.id
        achivments = Achievement.objects.filter(league__id = current_league)
        user_achivements = list(UserAchievement.objects.filter(user = current_user).values_list('achievement_id', flat = True))
        print(user_achivements)
        currency_dict = {}
        for i in achivments:
            currency_dict[i.id] = []
            img_example = AchievementValue.objects.filter(achievement__id = i.id).select_related('currency')
            for j in img_example:
                helper = {}
                quant = j.quantity
                img_path = j.currency.image.url
                helper['url'] = img_path
                helper['quant'] = quant
                currency_dict[i.id].append(helper)
    cont = {
        'leagues': leagues,
        'achivments': achivments,
        'currency_dict': currency_dict,
        'user_achivements': user_achivements,
        'current_league': current_league,
        'request': request
    }
    html = render_to_string('achievements_result.html', cont)
    return_dict = {'html': html}
    return JsonResponse(return_dict)





def achivments_legaue(request):
    django_user = request.user
    current_user = User.objects.get(django_user_id=django_user)
    if request.method == 'GET':
        current_league = current_user.league.id
        data = request.GET
        leagues = League.objects.all()
        achivments = Achievement.objects.filter(league=data['id'])
        user_achivements = list(UserAchievement.objects.filter(user=current_user).values_list('achievement_id', flat=True))
        currency_dict = {}
        for i in achivments:
            currency_dict[i.id] = []
            img_example = AchievementValue.objects.filter(achievement__id=i.id).select_related('currency')
            for j in img_example:
                helper = {}
                quant = j.quantity
                img_path = j.currency.image.url
                helper['url'] = img_path
                helper['quant'] = quant
                currency_dict[i.id].append(helper)
        cont = {
            'leagues':leagues,
            'achivments': achivments,
            'currency_dict': currency_dict,
            'user_achivements':user_achivements,
            'current_league':current_league,
            'request': request
        }
        html = render_to_string('achievements_result.html', cont)
        return_dict = {'html': html}
        return JsonResponse(return_dict)
    else:
        data = request.POST
        return_dict ={}


        achieve = AchievementValue.objects.filter(achievement = Achievement.objects.get(id = data['id']))
        for ach in achieve:
            user_balance = UserPoint.objects.get(user = current_user, currency = Currency.objects.get(id = ach.currency_id)).quantity
            print(user_balance)
            if user_balance < ach.quantity:
                # text_error = "Вам не вистачає " + str(ach.quantity - user_balance)+ ' ' + Currency.objects.get(id = ach.currency_id).currency
                return_dict = {'error': ach.quantity - user_balance,
                               'url_currency': Currency.objects.get(id = ach.currency_id).image.url}
                return JsonResponse(return_dict)
        for ach in achieve:
            instance = UserPoint.objects.get(user = current_user, currency = Currency.objects.get(id = ach.currency_id))
            instance.quantity -= ach.quantity
            instance.save()
            pointslist = PointsList.objects.create(user = current_user,  currency = Currency.objects.get(id = ach.currency_id), increase = False, points_quantity = ach.quantity)
            DecreasePointsInfo.objects.create(decrease = pointslist, decrease_type = DecreasePointsType.objects.get(id = 1), achievement = Achievement.objects.get(id = data['id']))
        UserAchievement.objects.create(achievement = Achievement.objects.get(id = data['id']), user = current_user)
        legaue_achievements = list(Achievement.objects.filter(league__id =current_user.league.id).values_list('id', flat = True))
        quant = UserAchievement.objects.filter(user = current_user, achievement__id__in = legaue_achievements).count()
        if quant == League.objects.get(id = current_user.league.id).quantity_achievement:
            current_user.league =League.objects.get(id = current_user.league.id  + 1)
            current_user.save()
            print('New league')
            return_dict = {
                'new_league' : League.objects.get(id = current_user.league.id).league
            }
        achievement = Achievement.objects.get(id=data['id'])

        cont = {
            'request': request,
            'achieve':achievement
        }
        html = render_to_string('new_achievement.html', cont)
        return_dict['html'] = html
        return_dict['success'] = True
        return JsonResponse(return_dict)


def test(request):
    return render(request, 'home_copy.html')


def test_event(request, id_event):
    print(id_event)
    event = Event.objects.get(id=id_event)
    status = Status.objects.all()
    subscribers = EventsSubscriber.objects.filter(event = event).count()
    parts = EventsParticipant.objects.filter(event = event).count()
    url_currency = Currency.objects.get(type_event = EventsType.objects.get(id = event.events_type.id)).image.url
    event_org_tasks = []
    if EventsOrgTask.objects.filter(event = event).exists():
        event_org_tasks = EventsOrgTask.objects.filter(event = event)


    form = EditeEventForm(request.POST or None, instance=Event.objects.get(id = id_event))

    cont = {
        'request':request,
        'event': event,
        'status': status,
        'subscribers': subscribers,
        'parts': parts,
        "event_org_tasks": event_org_tasks,
        'url_currency': url_currency,
        'form':form
    }
    html = render_to_string('event_edit.html', cont)
    return_dict = {'html': html}


    if request.POST and form.is_valid():
            form.save()

            # Save was successful, so redirect to another page
            return JsonResponse(return_dict)


    return JsonResponse(return_dict)


def form(request, id = None):
    if id:
        event = get_object_or_404(Event, pk=id)
        event = Event.objects.get(id=id)

    form = EditeEventForm(request.POST or None, instance=event)
    if request.POST and form.is_valid():
        form.save()

        # Save was successful, so redirect to another page
        redirect_url = reverse('/profile')
        return redirect(redirect_url)
    return_dict = {}
    cont = {
        'id':id,
        'form': form,
        'request':request
    }
    html = render_to_string('event_edit.html', cont)
    return_dict['html'] = html
    return JsonResponse(return_dict)

