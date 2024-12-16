from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from user.models import Profile, Message
from django.forms import ModelForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'phone_number', 'email', 'username', 
        'password1', 'password2']
        labels = {
            'first_name': 'Имя и фамилия',
            'email': 'Email', 
            'phone_number': 'Номер телефона',
            'username':'Логин', 
            'password1':'Пароль', 
            'password2': 'Подтверждение пароля'

        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control input-box form-ensurance-header-control'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'phone_number', 'email', 'username']
        labels = {
            'name': 'Имя и фамилия',
            'email': 'Email', 
            'phone_number': 'Номер телефона',
            'username':'Логин'
        }
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control input-box form-ensurance-header-control'})

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']
        labels = {'name': 'Имя и фамилия',
            'email': 'Email', 
            'subject':'Тема сообщения',
            'body':'Текст сообщения'
        }

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control input-box form-ensurance-header-control'})
