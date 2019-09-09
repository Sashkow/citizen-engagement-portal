from volunteer.models import City
from django.contrib.postgres.search import SearchVector



#return events, events_part, events_subs
def make_filter(parameters, DigestList, EventsType, User, Status, django_user):
    filter = {}
    if parameters[0] not in ['all', 'all_digest']:
        filter['events_type'] = EventsType.objects.get(id=parameters[0])
    elif parameters[0] == 'all_digest':
        digest = DigestList.objects.filter(user=User.objects.get(django_user_id=django_user)).values_list('type', flat=True)
        types_dig = EventsType.objects.filter(id__in = list(digest))
        filter['events_type__in'] = types_dig
    if parameters[3] != 'none':
        bool_value = True if parameters[3] == 'event' else False
        filter['events_or_task'] = bool_value
    if parameters[4] != 'none':
        filter['status'] = Status.objects.get(id=parameters[4])
    if parameters[5] != 'none':
        filter['city'] = City.objects.get(id=parameters[5])
    return filter


def get_events(Event, TaskApplication, Status, User, DigestList, EventsSubscriber, EventsParticipant, EventsPhoto, django_user, events_per_page, parameters, EventsType, search=None):

    from_page = events_per_page * int(parameters[1]) - events_per_page
    to_page = events_per_page * int(parameters[1])

    if search:
        search_events = Event.objects.annotate(
            search=SearchVector(
                'name',
                'organizer__first_name',
                'organizer__last_name',
                'city__city',
                'address',
                'description',
            ),
        ).filter(search__icontains=search)
    else:
        search_events = Event.objects.all()

    if parameters[2] == 'news':
        filter_event = make_filter(parameters, DigestList, EventsType, User, Status, django_user)
        events = search_events.filter(**filter_event).order_by('-publication_date')[from_page:to_page]
        events_quantity = search_events.filter(**filter_event).order_by('-publication_date').count()

    elif parameters[2] == 'volunteer':
        filter_event = make_filter(parameters, DigestList, EventsType, User, Status, django_user)
        events_many = list(EventsParticipant.objects.filter(user=User.objects.get(django_user_id=django_user)).select_related('event').values_list('event__id', flat = True))
        events = search_events.filter(**filter_event, id__in=events_many).order_by('-publication_date')[from_page:to_page]
        events_quantity = search_events.filter(**filter_event, id__in=events_many).order_by('-publication_date').count()

    else:
        filter_event = make_filter(parameters, DigestList, EventsType, User, Status, django_user)
        events = search_events.filter(**filter_event, organizer = User.objects.get(django_user_id=django_user)).order_by('-publication_date')[from_page:to_page]
        events_quantity = search_events.filter(**filter_event, organizer = User.objects.get(django_user_id=django_user)).order_by('-publication_date').count()



    events_subs = {}
    events_part = {}
    events_org = {}
    events_task_app = {}

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

        try:
            app = TaskApplication.objects.get(user=User.objects.get(django_user_id=django_user), event = event)
            events_task_app[event.id] = 1
        except:
            events_task_app[event.id] = 0

        if event.organizer.id == User.objects.get(django_user_id=django_user).id:
            events_org[event.id] = 1
        else:
            events_org[event.id] = 0

        event.following = len(EventsSubscriber.objects.filter(event=event))
        event.going = len(EventsParticipant.objects.filter(event=event))
        event_photos = EventsPhoto.objects.filter(event = event, is_it_cover =True)
        if len(event_photos) == 1:
            event_photo = event_photos[0]
            event.event_photo = event_photo
        else:
            event.event_photo = None
    return events, events_part, events_subs, events_quantity, events_org, events_task_app

#return pages
def get_pages_number(events_quantity, events_per_page, current):
    if events_quantity % events_per_page != 0 and events_quantity > events_per_page:
        pages = events_quantity// events_per_page + 1
    elif events_quantity < events_per_page:
        pages = 1
    else:
        pages = events_quantity// events_per_page

    if pages <= 10:
        pages_range = list(range(pages + 1)[1:])

    elif pages > 10:
        if int(current) > 5 and pages - int(current) > 4:
            from_page = int(current) - 2
            to_page = int(current)   + 4
            pages_range = [1 , '...'] + list(range(pages)[from_page:to_page]) + ['...', pages]
        elif int(current)<= 5:
            pages_range = [1,2,3,4,5,6,7,8,'...', pages]
        else:
            pages_range = [1, '...', pages - 7, pages -6, pages - 5, pages - 4, pages - 3, pages - 2, pages - 1, pages]
    return pages, pages_range


def check_key_in_dict(k, dict_v):
    if k in dict_v.keys():
        return dict_v[k]
    else:
       return None

def check_key_in_dict_int(k, dict_v):
    if k in dict_v.keys():
        return int(dict_v[k])
    else:
       return None