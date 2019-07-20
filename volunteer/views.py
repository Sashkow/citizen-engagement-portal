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

from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm, AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.http import HttpResponseForbidden

from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Max
from .forms import EditeEventForm, EventOrgTaskForm, UserForm, NewEventForm, TaskApplicationForm, OrgTaskApplicationForm
import datetime
from django.contrib.auth.models import User as DjangoUser
from volunteer.models import User as VolunteerUser
from volunteer.models import *

from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse

from django.template import loader, Context
from django.template.loader import render_to_string
from .functionviews import *

from datetime import timedelta, datetime
from babel.dates import format_timedelta
from django.core import serializers
from django.forms.models import model_to_dict
import json

from django.template import RequestContext


import random

from django.utils.decorators import classonlymethod
import pprint

import json

from django.contrib.auth.decorators import login_required
from notifications.signals import notify
from django.template import RequestContext

from volunteer.notification_helpers import notification_description, notification_title, notification_image




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
    user.notifications.mark_all_as_unread()
    # return redirect(reverse('notifications'))



events_per_page = 6

# user = authenticate(username=username, password=password)
#     if user is not None:
#         if user.is_active:
#             login(request, user)
#             # Redirect to a success page.
#         else:
#             # Return a 'disabled account' error message
#     else:
#         # Return an 'invalid login' error message.

def usual_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            print('unbelieveble')
            # form.save()

            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password')
            # user = authenticate(username=username, password=raw_password)
            user = form.get_user()

            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'login_form': form, 'usual_login':True })


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
    return render(request, 'registration/login.html', {'form': form, 'usual_signup':True})


def home(request):
    if request.user.is_authenticated:
        return redirect(reverse('profile'))
    else:
        return redirect(reverse('intropage'))


@login_required
def profile(request):
    page_title = "Профіль"

    session_key = request.session.session_key
    django_user = request.user
    volunteer = User.objects.filter(django_user_id = django_user)

    status = Status.objects.filter(id__range = (1, 2))

    volunteer = volunteer.first()

    if django_user.first_name:
        name = django_user.first_name
    elif django_user.username:
        name = django_user.username
    else:
        name = "Волонтер_ка"

    parameters = ['all_digest', 1, 'news', 'none', 'none']
    events, events_part, events_subs, events_quantity, events_org, events_task_app= get_events(Event, TaskApplication,  Status, User, DigestList, EventsSubscriber, EventsParticipant, EventsPhoto, django_user, events_per_page, parameters, EventsType)

    pages, pages_range = get_pages_number(events_quantity, events_per_page, 1)

    league_user = volunteer.league
    achievements_league_list = list(Achievement.objects.filter(league = league_user).values_list('id', flat = True))
    achieve_quant = UserAchievement.objects.filter(user = volunteer, achievement_id__in = achievements_league_list).count()
    user_points = UserPoint.objects.filter(user = volunteer).select_related('currency')
    max_user_point = user_points.aggregate(Max('quantity'))

    types_events = EventsType.objects.all()
    status_events = Status.objects.all()
    cities = City.objects.all()


    curr_category = {}
    for type_e in types_events:
        img = Currency.objects.get(type_event = type_e.id).image.url
        curr_category[type_e.id] = img

    form = NewEventForm()
    form_task = TaskApplicationForm()
    # form_org_task = OrgTaskApplicationForm()
    return render(request, 'core/profile.html', {
        'volunteer':volunteer,
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
        'curr_category':curr_category,
        'status_events': status_events,
        'cities': cities,
        'form': form,
        'events_task_app':events_task_app,
        'form_task':form_task,
        # 'form_org_task':form_org_task,
        'page_title': page_title
    })




@login_required
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

    if request.method == 'POST':
        django_user = request.user
        current_user = User.objects.get(django_user_id=django_user)
        updated_data = request.POST.copy()
        print (updated_data)
        updated_data.update({'organizer': current_user.id})
        form = NewEventForm(data = updated_data)
        print(form)
        if form.is_valid():
            form.save()
            redirect_url = reverse('profile')
            return redirect(redirect_url)
        # may return none: bad


@login_required
def follow_event(request):
    return_dict = dict()
    data = request.POST
    result = int(data['id_event'].replace(',', '').replace(' ',''))
    event = Event.objects.get(id = result)
    user_db = User.objects.get(django_user_id = request.user)
    if int(data['add']) == 1:
        EventsSubscriber.objects.create(user = user_db, event = event)
    else:
        EventsSubscriber.objects.filter(user = user_db, event = Event.objects.get(id = result)).delete()

    return JsonResponse(return_dict)

def subscribe_event(request):
    return_dict = dict()
    data = request.POST
    result = int(data['id_event'].replace(',', '').replace(' ',''))
    user_db = User.objects.get(django_user_id = request.user)

    # if clicking participate
    if int(data['add']) == 1:
        EventsSubscriber.objects.filter(user = user_db, event = Event.objects.get(id = result)).delete()
        EventsParticipant.objects.create(user = user_db, event = Event.objects.get(id = result))
    # if clicking leave
    else:
        EventsParticipant.objects.filter(user = user_db, event = Event.objects.get(id = result)).delete()
    return JsonResponse(return_dict)


def app_task(request):
    return_dict = {}
    if request.method == 'POST':
        django_user = request.user
        current_user = User.objects.get(django_user_id=django_user)
        updated_data = request.POST.copy()
        # print (updated_data)
        updated_data.update({'user': current_user.id})
        # print(updated_data)
        form = TaskApplicationForm(data = updated_data)
        print(form)
        if form.is_valid():
            print('Hi')
            form.save()
            # 5 Волонтер бажає виконати завдання
            event = Event.objects.get(id=form.data['event'])
            recipient = event.organizer.django_user_id
            notify.send(
                django_user,
                recipient=recipient,
                verb="applied",
                target=event,
                # timestamp = datetime.datetime.now().strftime("$d %B %Y %h:%m"),
                data={'type': '5',},  # 5 Волонтер бажає виконати завдання
            )
        else:
            print("Error: subscripiton did not happen")
        redirect_url = reverse('profile')
        return redirect(redirect_url)


def type_filter(request):
    return_dict = {}
    django_user = request.user
    data = request.GET
    print(data)
    parametrs = [data['type'], data['page'], data['state'], data['task_or_event'], data['status_id']]
    types_events = EventsType.objects.all()
    curr_category = {}
    for type_e in types_events:
        img = Currency.objects.get(type_event=type_e.id).image.url
        curr_category[type_e.id] = img
    if data['type'] not in ['all', 'all_digest'] and  not Event.objects.filter(events_type=EventsType.objects.get(id=data['type'])).exists():
        return JsonResponse(return_dict)
    else:
        events, events_part, events_subs, events_quantity, events_org, events_task_app = get_events(Event, TaskApplication,  Status, User, DigestList, EventsSubscriber, EventsParticipant, EventsPhoto, django_user, events_per_page, parametrs, EventsType)
        print(events)
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
            'events_org': events_org,
            'events_task_app':events_task_app
        }
        html = render_to_string('events_result.html', cont)
        return_dict = {'html': html}
        if 'add_filter' in  data.keys():
            status_events = Status.objects.all()
            cont['status_events'] = status_events
            filter_html = render_to_string('events_filter.html', cont)
            return_dict['filter_html'] = filter_html
        return JsonResponse(return_dict)


def profile_edit(request):
    django_user = request.user
    current_user = User.objects.get(django_user_id=django_user)
    form = UserForm(request.POST or None, instance=current_user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance = current_user)
        print (form)

        # for i in types:
            # print(data[str(i)])
            # if data[str(i)] == 'true' and not DigestList.objects.filter(user = current_user, type = EventsType.objects.get(id = i)).exists():
            #     print('in')
            #     DigestList.objects.create(user = current_user, type = EventsType.objects.get(id = i))
            # elif data[str(i)] == 'false' and DigestList.objects.filter(user = current_user, type = EventsType.objects.get(id = i)).exists():
            #     print('out')
            #     DigestList.objects.filter(user=current_user, type=EventsType.objects.get(id=i)).delete()
        if form.is_valid():
            form.save()
            print('form is saved')
            redirect_url = reverse('profile')
            return redirect(redirect_url)
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
                'form':form,
                 'dict_digest':dict_digest}
        html = render_to_string('edit_profile.html', cont, request=request)
        return_dict = {'html': html}
        return JsonResponse(return_dict)

def get_achivments(request):

    if request.method == 'GET':
        django_user = request.user
        current_user = User.objects.get(django_user_id=django_user)
        leagues = League.objects.all().order_by('id')
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
                return_dict = {'error': ach.quantity - user_balance,
                               'url_currency': Currency.objects.get(id = ach.currency_id).image.url}
                return JsonResponse(return_dict)
        return_dict['curr_quant'] = {}
        for ach in achieve:
            instance = UserPoint.objects.get(user = current_user, currency = Currency.objects.get(id = ach.currency_id))
            instance.quantity -= ach.quantity
            instance.save()
            return_dict['curr_quant'][ach.currency_id] = ach.quantity
            pointslist = PointsList.objects.create(user = current_user,  currency = Currency.objects.get(id = ach.currency_id), increase = False, points_quantity = ach.quantity)
            DecreasePointsInfo.objects.create(decrease = pointslist, decrease_type = DecreasePointsType.objects.get(id = 1), achievement = Achievement.objects.get(id = data['id']))
        UserAchievement.objects.create(achievement = Achievement.objects.get(id = data['id']), user = current_user)
        legaue_achievements = list(Achievement.objects.filter(league__id =current_user.league.id).values_list('id', flat = True))
        quant = UserAchievement.objects.filter(user = current_user, achievement__id__in = legaue_achievements).count()
        if quant == League.objects.get(id = current_user.league.id).quantity_achievement:
            current_user.league =League.objects.get(id = current_user.league.id  + 1)
            current_user.save()

            # print('New league')
            # return_dict = {
            #     'new_league' : League.objects.get(id = current_user.league.id).league
            # }
            # returnь redirect(reverse('profile'))
            return_dict['new_league']  = League.objects.get(id = current_user.league.id).league
            league_new = League.objects.get(id=current_user.league.id)
            league_dict = model_to_dict(league_new)
            league_dict['league_image'] = league_new.league_image.url
            league_dict['user_frame'] = league_new.user_frame.url
            league_dict['background_image'] = league_new.background_image.url
            return_dict['all_info']  = league_dict


        achievement = Achievement.objects.get(id=data['id'])
        if achievement.league.id == current_user.league.id:
            return_dict['ach_in_current'] = 1

        cont = {
            'request': request,
            'achieve':achievement
        }
        html = render_to_string('new_achievement.html', cont)
        return_dict['html'] = html
        return_dict['success'] = True
        list_to_json = return_dict
        print (list_to_json)
        return JsonResponse(return_dict)




def just_after_scuccess_auth(request):
    # if threre is no volunteer_user user corresponding to django_user
    # create new volunteer_user
    django_user = request.user
    volunteer_user = User.objects.filter(django_user_id=django_user)

    if not volunteer_user.exists():
        volunteer = User.objects.create(django_user_id=django_user)

        if not volunteer.first_name:
            if django_user.first_name or django_user.last_name:
                volunteer.first_name = django_user.first_name
                volunteer.second_name = django_user.last_name

        volunteer.save()


    return redirect(reverse('profile'))

def dispatch_social_login(request):
    first_name = request.GET['first_name']
    second_name = request.GET['second_name']

    if 'sub_fb.x' in request.GET:
        provider = 'facebook'
    elif 'sub_gg.x' in request.GET:
        provider = 'google-oauth2'
    else:
        print('Niether fb no gg')
        return None
    return redirect(
        reverse('social:begin', args=[provider, ]) + '?first_name={}&second_name={}'.format(first_name, second_name))



def form(request, id = None):
    if id:
        event = get_object_or_404(Event, pk=id)
        event = Event.objects.get(id=id)

    form = EditeEventForm(request.POST or None, instance=event)
    if request.POST and form.is_valid():
        form.save()
        redirect_url = reverse('profile')
        return redirect(redirect_url)
    return_dict = {}
    subs = EventsSubscriber.objects.filter(event = event).count()
    part = EventsParticipant.objects.filter(event = event).count()
    cont = {
        'id': id,
        'event': event,
        'form': form,
        'subs': subs,
        'part': part,
        'request': request,
        'zero_executor':False
    }
    if event.events_or_task == True and event.status.id == 1:
        tasks = EventsOrgTask.objects.filter(event = event)
        tasks_form_list = []
        for task in tasks:
            tasks_form_list.append(EventOrgTaskForm(instance=task))
            cont['tasks_form_list'] = tasks_form_list

    if event.events_or_task == False and TaskApplication.objects.filter(event = event).exists() and not TaskApplication.objects.filter(event = event, executer = True).exists():
        zero_executor = True
        cont['zero_executor'] = zero_executor
    html = render_to_string('event_edit.html', cont, request=request)
    return_dict['html'] = html
    return JsonResponse(return_dict)


def change_org_task(request, id):
    if request.POST:
        task = EventsOrgTask.objects.get(id = id)
        form = EventOrgTaskForm(request.POST or None, instance=task)
        if form.is_valid():
            return_dict = {}
            form.save()
            return JsonResponse(return_dict)

@login_required
def notifications(request):
    unread_read = list(request.user.notifications.unread()) + list(request.user.notifications.read())

    for notification in unread_read:
        # from notification_helpers.py

        notification.description = notification_description(notification)
        notification.image = notification_image(notification)
        notification.title = notification_title(notification)

        notification.is_unread = notification.unread


        naive = notification.timestamp.replace(tzinfo=None)
        delta = datetime.now() - naive
        relative_time = format_timedelta(delta, locale='uk_UA')
        relative_time = relative_time.replace("година", "годину")
        relative_time = relative_time.replace("хвилина", "хвилину")
        relative_time = relative_time.replace("секунда", "секунду")
        relative_time = relative_time + " тому"
        notification.relative_time = relative_time

    request.user.notifications.mark_all_as_read()

    cont = {
        'request': request,
        'unread_read': unread_read,

    }
    html = render_to_string('notification.html', cont)
    return_dict = {'html': html}
    return JsonResponse(return_dict)





def cancel_task(request, id):
    return_dict = {}
    task = EventsOrgTask.objects.get(id = id)
    task.canceled = True
    task.save()
    return JsonResponse(return_dict)

def refresh_digest(request):
    if request.method == 'POST':
        return_dict = {}
        data = request.POST
        django_user = request.user
        current_user = User.objects.get(django_user_id=django_user)
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





def task_executor(request):
    if request.method == "GET":
        data = request.GET
        executors = TaskApplication.objects.filter(event__id = data['event_id'])
        print (executors)
        cont = {
            'request': request,
            'executors': executors,
            'event_id' : data['event_id']
        }
        html = render_to_string('possieble_executors.html', cont)
        return_dict = {'html': html}
        return JsonResponse(return_dict)
    elif request.method == 'POST':
        data = request.POST
        return_dict = {}
        if TaskApplication.objects.filter(event__id = data['event_id'], executer = True).count() == 0:
            executor = TaskApplication.objects.get(event__id = data['event_id'], user__id = data['user_id'])
            executor.executer = True
            executor.save()
        return JsonResponse(return_dict)


def get_event_org_tasks(request):
    if request.method == "GET":
        data = request.GET
        org_tasks = EventsOrgTask.objects.filter(event__id = data['event_id'])
        cont = {
            'request':request,
            'org_tasks':org_tasks
        }
        print(org_tasks)
        html = render_to_string('event_org_task.html', cont)
        return_dict = {'html': html}
        return JsonResponse(return_dict)
    return_dict = {}
    return JsonResponse(return_dict)

@login_required()
def notifications_count(request):
    return_dict = {'notifications_count':Notification.objects.filter(recipient=request.user, unread = True).count(),}
    return JsonResponse(return_dict)


def change_photo(request):
    print(request.FILES['userpic'])
    return_dict = {}
    return JsonResponse(return_dict)

def intropage(request):
    form = UserCreationForm()
    login_form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form':form, 'login_form':login_form})

@login_required
def map_show(request):
    cont = {
        'request': request,
    }
    html = render_to_string('map.html', cont)
    return_dict = {'html': html}
    # return JsonResponse(return_dict)
    return render(request, 'map.html')



