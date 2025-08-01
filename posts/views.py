from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Post

class PostList(ListView):
    """
    Displays a list of posts on the homepage.
    """
    model = Post
    template_name = "posts/index.html"
    context_object_name = 'post_list'