# -*- coding: utf-8 -*-
from django.forms import ModelForm
from volunteer.models import Event, EventsOrgTask, User
from django.forms import SelectDateWidget
from django.forms.widgets import HiddenInput



class NewEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'events_or_task', 'events_type', 'date_event', 'address', 'status',  'description', 'max_part', 'min_part', 'recommended_points', 'contact']
        labels = {
            'name': 'Назва',
            'date_event': 'Дата та час',
            'address': 'Адреса',
            'description': 'Опис',
            'status': 'Статус',
            'max_part': 'Мінімальна кількість учасників',
            'min_part': 'Максимальна кількість учасників',
            'recommended_points': 'Рекомендована кількість болів',
            'contact':'Ваш контаактний e-mail',
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


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'photo']
        localized_fields = ('task_name', 'task_description', 'done',  'recommended_points', 'event', 'canceled')
        labels = {
            'first_name': "Ім'я",
            'last_name': 'Прізвище',
            'photo': 'Світлина'
        }