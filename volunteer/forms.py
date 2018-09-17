# -*- coding: utf-8 -*-
from django.forms import ModelForm
from volunteer.models import Event
from django.forms import SelectDateWidget



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