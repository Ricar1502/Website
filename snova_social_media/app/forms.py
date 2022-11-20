from django.forms import ModelForm, widgets
from api.models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class DateInput(forms.DateInput):
    input_type = 'date'


class CreateNewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'link', 'pic')


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


class UpdateProfile(forms.ModelForm):
    class Meta: 
        model = Profile
        fields = ('avatar', 'email', 'bio')
        widgets = {
            'birthday':  widgets.DateInput(attrs={'type': 'date'})
        }


class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))
    email=forms.EmailField(widget=forms.TextInput(attrs={'class': 'input'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input pass-input'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input pass-input'}))
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input pass-input'}))


# class LoginForm(UserCreationForm):
#     class Meta:
#         model = Profile
#         fields = ['name', 'password']
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control', 'data-val': 'true', 'data-val-required': 'Please enter your user name'}),
#             'password': forms.TextInput(attrs={'class': 'form-control', 'data-val': 'true', 'data-val-required': 'Please enter your password'}),
#         }
