from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce

from .models import Post, Comment, Vote, Category, SavedPost, Profile
from .forms import CommentForm, PostForm, ProfileUpdateForm, ProfileForm

class PostList(ListView):
    """
    Displays a list of published posts on the homepage.
    """
    model = Post
    template_name = "posts/index.html"
    context_object_name = 'post_list'

    def get_queryset(self):
        queryset = Post.objects.filter(status=1)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(content__icontains=query))

        category = self.request.GET.get('category')
        if category and category != 'All':
            queryset = queryset.filter(category__name=category)

        queryset = queryset.annotate(votes_sum=Coalesce(Sum('votes__vote_type'), 0))

        sort = self.request.GET.get('sort')
        if sort == 'top':
            queryset = queryset.order_by('-votes_sum')
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class PostDetail(DetailView):
    """
    Displays the details of a single post.
    """
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(approved=True).order_by('-created_on')
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
        else:
            messages.add_message(request, messages.ERROR, 'Your comment could not be submitted. The comment field cannot be empty.')
            context = self.get_context_data()
            context['comment_form'] = comment_form
            return self.render_to_response(context)

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
    
@method_decorator(login_required, name='dispatch')
class PostCreate(CreateView):
    """
    Handles the creation of a new post.
    It renders a PostForm and saves the new post to the database
    with the logged-in user as the author.
    """
    model = Post
    form_class = PostForm
    template_name = 'posts/post_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
@method_decorator(login_required, name='dispatch')
class PostUpdate(UpdateView):
    """
    Handles the editing of an existing post.
    It renders a PostForm pre-filled with the existing post data
    and saves the changes to the database.
    """
    model = Post
    form_class = PostForm
    template_name = 'posts/post_edit.html'

    def get_success_url(self):
        return reverse('post_detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
@method_decorator(login_required, name='dispatch')
class PostDelete(UserPassesTestMixin, DeleteView):
    """
    Handles the deletion of an existing post.
    It renders a confirmation page and deletes the post upon confirmation.
    Only the author of the post can delete it.
    """
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
@method_decorator(login_required, name='dispatch')
class CommentUpdate(UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'posts/comment_edit.html'

    def get_success_url(self):
        return reverse('post_detail', kwargs={'slug': self.object.post.slug})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
@method_decorator(login_required, name='dispatch')
class CommentDelete(UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'posts/comment_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'slug': self.object.post.slug})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
@method_decorator(login_required, name='dispatch')
class UserProfile(DetailView):
    model = User
    template_name = 'posts/user_profile.html'
    context_object_name = 'user_profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'

@method_decorator(login_required, name='dispatch')
class UserProfileUpdate(UserPassesTestMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'posts/user_profile_edit.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_success_url(self):
        return reverse('user_profile', kwargs={'username': self.request.user.username})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, _ = Profile.objects.get_or_create(user=self.object)

        if 'user_form' not in context and 'form' in context:
            context['user_form'] = context['form']

        context.setdefault('profile_form', ProfileForm(instance=profile))
        context['user_profile'] = self.object
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        profile, _ = Profile.objects.get_or_create(user=self.object)

        user_form = self.get_form()
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated.')
            return HttpResponseRedirect(self.get_success_url())

        messages.error(request, 'Please correct the errors below.')
        context = self.get_context_data()
        context['user_form'] = user_form
        context['profile_form'] = profile_form
        return self.render_to_response(context)

    def form_invalid(self, user_form, profile_form):
        context = self.get_context_data(form=user_form, profile_form=profile_form)
        return self.render_to_response(context)

    def test_func(self):
        return self.request.user == self.get_object()
    
@method_decorator(login_required, name='dispatch')
class SavedPostView(View):
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        saved_post, created = SavedPost.objects.get_or_create(user=request.user, post=post)

        if not created:
            saved_post.delete()
            messages.add_message(request, messages.INFO, 'Post has been unsaved.')
        else:
            messages.add_message(request, messages.SUCCESS, 'Post has been saved.')

        return redirect('post_detail', slug=slug)
    
@method_decorator(login_required, name='dispatch')
class SavedPostListView(View):
    def get(self, request, *args, **kwargs):
        saved_posts = SavedPost.objects.filter(user=request.user)
        context = {
            'saved_posts': saved_posts,
        }
        return render(request, 'posts/saved_posts.html', context)