from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Comment, Vote, Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'content', 'featured_image', 'url')
        widgets = {
            'content': SummernoteWidget(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': SummernoteWidget()
        }

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ('vote_type',)