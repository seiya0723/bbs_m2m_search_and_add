from django import forms
from .models import Topic





class TopicForm(forms.ModelForm):

    class Meta:
        model   = Topic
        fields  = [ "title","comment","user","tag", ]

class TopicTagForm(forms.ModelForm):

    class Meta:
        model   = Topic
        fields  = [ "tag" ]

