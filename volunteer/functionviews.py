#return events, events_part, events_subs
def get_events(Event, User, EventsSubscriber, EventsParticipant, EventsPhoto, django_user, events_per_page, parameters, EventsType):

    from_page = events_per_page * int(parameters[1]) - events_per_page
    to_page = events_per_page * int(parameters[1])

    print(parameters[0])
    if parameters[0] == 'all':
        events = Event.objects.all().order_by('-publication_date')[from_page:to_page]
        events_quantity = Event.objects.all().order_by('-publication_date').count()

    else:
        events = Event.objects.filter(events_type=EventsType.objects.get(id=parameters[0]))[from_page:to_page]
        events_quantity = Event.objects.filter(events_type=EventsType.objects.get(id=parameters[0])).count()

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

    return events, events_part, events_subs, events_quantity

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