from django.forms import ModelForm
from api.models import Post


class CreateNewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
