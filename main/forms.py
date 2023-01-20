from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from .models import Topic

class ThreadForm(forms.Form):

    topic_list = Topic.objects.all()
    topic_choices = []
    for topic in topic_list:
        topic_choices.append((topic.id, topic.topic_name.replace('"', '')))


    thread_title = forms.CharField(label="Title", max_length=50)
    thread_topic = forms.ChoiceField(choices=topic_choices, required=True)
    thread_content = forms.CharField(label="Content", max_length=500, widget=forms.Textarea())

class SignupForm(UserCreationForm):


    def clean_password(self):
        password = self.cleaned_data['password']
        try:
            password_validation.validate_password(password, self.Meta.model)
        except forms.ValidationError as error:
            self.add_error('password', error)
        return password

class AddCommentForm(forms.Form):
    comment_body = forms.CharField(label="Comment", max_length=200)
