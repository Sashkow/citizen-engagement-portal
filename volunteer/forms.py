# -*- coding: utf-8 -*-
from django.forms import ModelForm, IntegerField
from volunteer.models import Event, EventsOrgTask, User, TaskApplication, OrgTaskApplication
from django.forms import SelectDateWidget, IntegerField, TimeField, EmailField, ModelChoiceField
from django.forms.widgets import HiddenInput, TimeInput, EmailInput, NumberInput
from volunteer.widgets import SelectTimeWidget


class NewEventForm(ModelForm):
    min_part = IntegerField(required=False, min_value=1,
                            error_messages={
                                'min_value': 'Переконайтеся, що це значення більше 0',
                            },
                            label='Мінімальна кількість учасників')
    max_part = IntegerField(required=False, min_value=1,
                            error_messages={
                                'min_value': 'Переконайтеся, що це значення більше 0',
                            },
                            label='Максимальна кількість учасників')

    recommended_points = IntegerField(required=True, min_value=0,
                            error_messages={
                                'min_value': 'Переконайтеся, що це значення не менше 0',
                            },
                            label='Рекомендована кількість балів')

    time_event = TimeField(widget=SelectTimeWidget(minute_step=10, second_step=10))



    class Meta:
        model = Event
        fields = ['organizer', 'name', 'events_or_task', 'events_type', 'date_event','time_event', 'address', 'status',  'description', 'min_part', 'max_part',  'recommended_points', 'contact']
        labels = {
            'name': 'Назва',
            'date_event': 'Дата',
            'time_event': 'Час',
            'address': 'Адреса',
            'description': 'Опис',
            'status': 'Статус',
            'max_part': 'Мінімальна кількість учасників',
            'min_part': 'Максимальна кількість учасників',
            'recommended_points': 'Рекомендована кількість балів',
            'contact':'Ваш контактний e-mail',
            'events_type':'Категорія'
        }
        widgets = {
            'date_event': SelectDateWidget(),
            'time_event': TimeInput(),
        }


class TaskApplicationForm(ModelForm):
    event = ModelChoiceField(queryset=Event.objects.all(), widget=NumberInput())

    class Meta:
        model = TaskApplication
        fields = ['user', 'event', 'contact']
        labels = {
            'contact': 'Залиште Ваш телефонний номер',
            'user': 'user',
            'event': 'event'
        }


class OrgTaskApplicationForm(ModelForm):
    class Meta:
        model = OrgTaskApplication
        fields = ['user', 'task', 'contact']
        labels = {
            'contact': 'Залиште Ваш контактний e-mail',
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
            'min_part': 'Мінімальна кількість учасників',
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


