from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Comment, Vote

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ('vote_type',)