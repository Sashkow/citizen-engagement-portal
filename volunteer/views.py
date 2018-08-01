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

from volunteer.models import User, DjangoUser, Event, EventsPhoto

from volunteer.forms import NewEventForm



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
    for event in events:
        event_photos = EventsPhoto.objects.filter(event = event, is_it_cover =True)
        if len(event_photos) == 1:
            event_photo = event_photos[0]
            event.event_photo = event_photo
        else:
            event.event_photo = None

    return render(request, 'core/profile.html', {'volunteer':volunteer, 'name':name, 'events':events})


def event(request):
    return render(request, 'event.html')

def new_event(request):
    if request.method == "POST":
        form = NewEventForm(request.POST)
        if form.is_valid():
            print("valid")
            event = form.save(commit=False)
            event.organizer = User.objects.get_or_create(djang_user = request.user)
            event.save()
            return redirect(reverse('profile'))
        else:
            print("not valid")

    else:
        form = NewEventForm()
        return render(request, 'volunteer/new_event.html', {'form':form})