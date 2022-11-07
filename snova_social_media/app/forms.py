from django.forms import ModelForm, widgets
from api.models import Post, Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm


class DateInput(forms.DateInput):
    input_type = 'date'


class CreateNewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class CreateNewUserForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'birthday':  widgets.DateInput(attrs={'type': 'date'})
        }


# class LoginForm(UserCreationForm):
#     class Meta:
#         model = Profile
#         fields = ['name', 'password']
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control', 'data-val': 'true', 'data-val-required': 'Please enter your user name'}),
#             'password': forms.TextInput(attrs={'class': 'form-control', 'data-val': 'true', 'data-val-required': 'Please enter your password'}),
#         }
