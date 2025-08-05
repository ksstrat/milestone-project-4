from django.views import View
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from .models import Post, Comment, Vote
from .forms import CommentForm

class PostList(ListView):
    """
    Displays a list of posts on the homepage.
    """
    model = Post
    template_name = "posts/index.html"
    context_object_name = 'post_list'

class PostDetail(DetailView):
    """
    Displays the details of a single post.
    """
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('-created_on')
        context['comment_form'] = CommentForm()
        context['user_vote'] = self.object.user_vote_type(self.request.user)
        return context
    
    @method_decorator(login_required, name='post')
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = self.object
            new_comment.author = request.user
            new_comment.save()

            messages.add_message(request, messages.SUCCESS, 'Your comment has been submitted and is awaiting approval.')

        return HttpResponseRedirect(reverse('post_detail', kwargs={'slug': self.object.slug}))

@method_decorator(login_required, name='dispatch')
class VoteView(View):
    """
    Handles upvote/downvote logic for a post.
    It takes a POST request with a vote type and the user,
    and then creates, updates, or deletes a Vote object.
    """
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        vote_type_str = request.POST.get('vote_type')

        if vote_type_str is None:
            return redirect('post_detail', slug=slug)

        try:
            vote_type = int(vote_type_str)
        except (ValueError, TypeError):
            return redirect('post_detail', slug=slug)

        user = request.user

        vote, created = Vote.objects.get_or_create(user=user, post=post, defaults={'vote_type': vote_type})

        if not created and vote.vote_type == vote_type:
            vote.delete()
        elif not created and vote.vote_type != vote_type:
            vote.vote_type = vote_type
            vote.save()
        else:
            vote.vote_type = vote_type
            vote.save()

        return redirect('post_detail', slug=slug)