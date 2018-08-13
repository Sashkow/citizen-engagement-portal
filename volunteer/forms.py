# -*- coding: utf-8 -*-
from django.forms import ModelForm
from volunteer.models import Event
from django.forms import SelectDateWidget



class NewEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date_event', 'events_type', 'address', 'district', 'description']
        labels = {
            'name': 'Назва',
            'date_event': 'Дата та час',
            'address': 'Адреса',
            'district': 'Район',
            'description': 'Опис',
        }
        widgets = {
            'date_event': SelectDateWidget(),
        }