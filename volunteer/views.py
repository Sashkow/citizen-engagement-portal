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
from django.shortcuts import render

from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse


from volunteer.models import User, DjangoUser, Event, EventsPhoto, EventsParticipant, EventsSubscriber

from volunteer.forms import NewEventForm

from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse



# @login_required
# def home(request):
#     return render(request, 'core/home.html')

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

    events = Event.objects.all()
    events_subs = {}
    events_part = {}

    for event in events:
        try:
            subscr = EventsSubscriber.objects.get(user=User.objects.get(django_user_id=django_user), event = event)
            events_subs[event.id] = 1
        except:
            events_subs[event.id] = 0

        try:
            part = EventsParticipant.objects.get(user=User.objects.get(django_user_id=django_user), event = event)
            events_part[event.id] = 1
        except:
            events_part[event.id] = 0

        event.following = len(EventsSubscriber.objects.filter(event=event))
        event.going = len(EventsParticipant.objects.filter(event=event))
        event_photos = EventsPhoto.objects.filter(event = event, is_it_cover =True)
        if len(event_photos) == 1:
            event_photo = event_photos[0]
            event.event_photo = event_photo
        else:
            event.event_photo = None

    return render(request, 'core/profile.html', {'volunteer':volunteer, 'name':name, 'events':events, 'events_subs':events_subs, 'events_part':events_part})

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
    if request.method == "POST":
        form = NewEventForm(request.POST)
        if form.is_valid():
            print("valid")
            event = form.save(commit=False)
            event.organizer = User.objects.get_or_create(django_user_id = request.user)[0]
            event.save()
            return redirect(reverse('profile'))
        else:
            print("not valid")

    else:
        form = NewEventForm()
        return render(request, 'volunteer/new_event.html', {'form':form})


@login_required
def follow_event(request):
    return_dict = dict()
    data = request.POST
    result = int(data['id_event'].replace(',', '').replace(' ',''))
    user_db = User.objects.get(django_user_id = request.user)
    print('in')
    print(int(data['add']))
    if int(data['add']) == 1:
        print('ogo')
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
