# -*- coding: utf-8 -*-
from django.forms import ModelForm
from volunteer.models import Event, EventsOrgTask
from django.forms import SelectDateWidget
from django.forms.widgets import HiddenInput



class NewEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date_event', 'events_type', 'address',  'description']
        labels = {
            'name': 'Назва',
            'date_event': 'Дата та час',
            'address': 'Адреса',
            'description': 'Опис',
        }
        widgets = {
            'date_event': SelectDateWidget(),
        }

class EditeEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date_event', 'address', 'status', 'max_part', 'min_part', 'contact', 'description']
        localized_fields = ('name', 'date_event', 'address', 'status', 'max_part', 'min_part', 'contact', 'description')
        labels = {
            'name': 'Назва',
            'date_event': 'Дата та час',
            'address': 'Адреса',
            'status': 'Статус',
            'max_part' : 'Максимальна кількість учасників',
            'min_part': 'Мінімальнв кількість учасників',
            'description': 'Опис',
        }
        widgets = {
            'date_event': SelectDateWidget(),
        }


class EventOrgTaskForm(ModelForm):
    class Meta:
        model = EventsOrgTask
        fields = ['task_name', 'task_description', 'done',  'recommended_points', 'event', 'canceled']
        localized_fields = ('task_name', 'task_description', 'done',  'recommended_points', 'event', 'canceled')
        labels = {
            'task_name': 'Назва організаційного завдання',
            'task_description': 'Опис',
            'done': 'Виконано'
        }
    def __init__(self, *args, **kwargs):
        super(EventOrgTaskForm, self).__init__(*args, **kwargs)
        self.fields['event'].widget = HiddenInput()
        self.fields['canceled'].widget = HiddenInput()