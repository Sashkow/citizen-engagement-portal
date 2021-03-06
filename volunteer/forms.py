# -*- coding: utf-8 -*-
from django.forms import ModelForm, IntegerField
from volunteer.models import Event, EventsOrgTask, User, TaskApplication, OrgTaskApplication
from django.forms import SelectDateWidget, IntegerField, TimeField, EmailField, ModelChoiceField, CharField

from django.forms.widgets import HiddenInput, TimeInput, EmailInput, NumberInput, TextInput, Select
from volunteer.widgets import SelectTimeWidget
from volunteer.models import City, DjangoUser
from osm_field.fields import OSMWidget



class NewEventForm(ModelForm):
    # min_part = IntegerField(required=False, min_value=1,
    #                         error_messages={
    #                             'min_value': 'Переконайтеся, що це значення більше 0',
    #                         },
    #                         label='Мінімальна кількість учасників')
    # max_part = IntegerField(required=False, min_value=1,
    #                         error_messages={
    #                             'min_value': 'Переконайтеся, що це значення більше 0',
    #                         },
    #                         label='Максимальна кількість учасників')

    recommended_points = IntegerField(required=True, min_value=0,
                            error_messages={
                                'min_value': 'Переконайтеся, що це значення не менше 0',
                            },
                            label='Рекомендована кількість балів')

    time_event = TimeField(required=False, widget=SelectTimeWidget(minute_step=10, second_step=10),label='Час події')
    city = ModelChoiceField(required=True, queryset=City.objects.order_by('city'), label="Область", initial=City.objects.all()[0])



    class Meta:
        model = Event

        fields = ['organizer', 'name', 'events_or_task', 'events_type', 'date_event','time_event', 'city', \
                  'status',  'description',  'recommended_points', 'contact','location', 'latitude', 'longitude', \
                  'fb_page']
        labels = {
            'name': 'Назва',
            'date_event': 'Дата',
            'time_event': 'Час',
            # 'address': 'Адреса',
            'location': 'Адреса',
            'description': 'Опис',
            'status': 'Статус',
            'fb_page': 'Facebook-сторінка',
            # 'max_part': 'Мінімальна кількість учасників',
            # 'min_part': 'Максимальна кількість учасників',
            'recommended_points': 'Рекомендована кількість балів',
            'contact':'Ваш контактний e-mail',
            'events_type':'Категорія',

            'city': 'Область'



        }
        widgets = {
            'date_event': SelectDateWidget(),
            'time_event': TimeInput(),
            #'location': OSMWidget(lat_field='latitude', lon_field='longitude'),
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


class EditEventForm(ModelForm):
    time_event = TimeField(required=False, widget=SelectTimeWidget(minute_step=10, second_step=10),
                           label='Час')
    #city = ModelChoiceField(required=True, queryset=City.objects.all(), label="Область", initial=City.objects.all()[0])

    class Meta:
        model = Event
        fields = ['name', 'date_event', 'time_event','location', 'city', 'status', 'contact', 'fb_page', 'description']
        localized_fields = ('name', 'date_event', 'time_event', 'location', 'city', 'status', 'contact', 'description')
        labels = {
            'name': 'Назва',
            'date_event': 'Дата',
            'time_event': 'Час',
            'location': 'Адреса',
            'status': 'Статус',
            'city': 'Область',
            'fb_page': 'Facebook-сторінка',

            # 'max_part' : 'Максимальна кількість учасників',
            # 'min_part': 'Мінімальна кількість учасників',
            'description': 'Опис',
        }
        widgets = {
            'date_event': SelectDateWidget(),
            'time_event': TimeInput(),



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

    city=ModelChoiceField(required=True, queryset=City.objects.order_by('city'), label="Область",
                              initial=City.objects.all()[0])



    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'photo', 'city']
        localized_fields = ('task_name', 'task_description', 'done',  'recommended_points', 'event', 'canceled')
        labels = {
            'first_name': "Ім'я",
            'last_name': 'Прізвище',
            'photo': 'Світлина',
            'city': 'Область'
        }


class ProfileCreationForm(ModelForm):
    """
    Form for user profile used together with auth.UserCreationForm
    """
    first_name = CharField(label="Ім'я", widget=TextInput(attrs={
        'placeholder': "Ім'я",
        'class': 'input-reg'
    }))
    last_name = CharField(label='Прізвище', widget=TextInput(attrs={
        'placeholder': "Прізвище",
        'class': 'input-reg'
    }))
    city = ModelChoiceField(
        queryset=City.objects.order_by('city'),
        label='Область', widget=Select(attrs={
            'placeholder': "Область",
            'class': 'input-reg'
        }),
        empty_label='Обери область'
    )


    class Meta:
        model = DjangoUser
        fields = ('city','first_name', 'last_name')
        field_classes = {'city': City,}






