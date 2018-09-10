#return events, events_part, events_subs
def get_events(Event, User, DigestList, EventsSubscriber, EventsParticipant, EventsPhoto, django_user, events_per_page, parameters, EventsType):

    from_page = events_per_page * int(parameters[1]) - events_per_page
    to_page = events_per_page * int(parameters[1])

    print(parameters[0])
    if parameters[2] == 'news':
        if parameters[0] == 'all':
            events = Event.objects.all().order_by('-publication_date')[from_page:to_page]
            events_quantity = Event.objects.all().order_by('-publication_date').count()

        elif parameters[0] == 'all_digest':
            digest = DigestList.objects.filter(user=User.objects.get(django_user_id=django_user)).values_list('type', flat=True)
            types_dig = EventsType.objects.filter(id__in=list(digest))
            events = Event.objects.filter(events_type__in=types_dig)[from_page:to_page]
            events_quantity = Event.objects.filter(events_type__in=types_dig).count()

        else:
            events = Event.objects.filter(events_type=EventsType.objects.get(id=parameters[0]))[from_page:to_page]
            events_quantity = Event.objects.filter(events_type=EventsType.objects.get(id=parameters[0])).count()

    elif parameters[2] == 'volunteer':
        if parameters[0] == 'all' or parameters[0] == 'all_digest':
            events_many = list(EventsParticipant.objects.filter(user=User.objects.get(django_user_id=django_user)).select_related('event').values_list('event__id', flat = True))
            events = Event.objects.filter(id__in=events_many)[from_page:to_page]
            events_quantity = Event.objects.filter(id__in=events_many).count()
        else:
            events_many = list(EventsParticipant.objects.filter(user=User.objects.get(django_user_id=django_user)).select_related('event').values_list('event__id', flat = True))
            events = Event.objects.filter(id__in=events_many, events_type=EventsType.objects.get(id=parameters[0]))[from_page:to_page]
            events_quantity = Event.objects.filter(id__in=events_many, events_type=EventsType.objects.get(id=parameters[0])).count()
    else:
        if parameters[0] == 'all' or parameters[0] == 'all_digest':
            events = Event.objects.filter(organizer = User.objects.get(django_user_id=django_user))[from_page:to_page]
            events_quantity = Event.objects.filter(organizer = User.objects.get(django_user_id=django_user)).count()
        else:
            events = Event.objects.filter(organizer=User.objects.get(django_user_id=django_user), events_type=EventsType.objects.get(id=parameters[0]))[from_page:to_page]
            events_quantity = Event.objects.filter(organizer=User.objects.get(django_user_id=django_user), events_type=EventsType.objects.get(id=parameters[0])).count()


    events_subs = {}
    events_part = {}
    events_org = {}

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
    print(events_org)
    return events, events_part, events_subs, events_quantity, events_org

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