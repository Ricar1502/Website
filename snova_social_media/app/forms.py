from django.forms import ModelForm, widgets
from api.models import Post, User
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class CreateNewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class CreateNewUserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'birthday':  widgets.DateInput(attrs={'type': 'date'})
        }
