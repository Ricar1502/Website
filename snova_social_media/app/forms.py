from django.forms import ModelForm, widgets
from api.models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm


class DateInput(forms.DateInput):
    input_type = 'date'


class CreateNewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'link', 'pic')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Text(optional)', 'rows': '6'}),
            'link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Url'}),
        }


class CreateNewUserForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'birthday':  widgets.DateInput(attrs={'type': 'date'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Leave your comment here', 'rows': '3'}),
        }



# class LoginForm(UserCreationForm):
#     class Meta:
#         model = Profile
#         fields = ['name', 'password']
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control', 'data-val': 'true', 'data-val-required': 'Please enter your user name'}),
#             'password': forms.TextInput(attrs={'class': 'form-control', 'data-val': 'true', 'data-val-required': 'Please enter your password'}),
#         }
