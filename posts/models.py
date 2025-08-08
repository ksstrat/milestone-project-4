from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.db.models import F, Sum
from cloudinary.models import CloudinaryField


# Model for categories
class Category(models.Model):
    """
    Model representing a category for posts.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        """
        Auto-generates a slug from the category name.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

# Model for posts
class Post(models.Model):
    """
    Model representing a user-created post on PixelPulse.
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=True)
    url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=((0, 'Draft'), (1, 'Published')), default=0)
    featured_image = CloudinaryField('image', default='placeholder')

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    @property
    def total_votes(self):
        return self.votes.aggregate(total_votes=Sum('vote_type'))['total_votes'] or 0
    
    @property
    def approved_comments_count(self):
        return self.comments.filter(approved=True).count()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Automatically generates a slug from the title if it's not set.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def user_vote_type(self, user):
        if user.is_authenticated:
            try:
                vote = Vote.objects.get(post=self, user=user)
                return vote.vote_type
            except Vote.DoesNotExist:
                return 0
        return 0

# Model for comments
class Comment(models.Model):
    """
    Model representing a user comment on a post.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body[:50]} by {self.author}"
    
# Model for upvotes and downvotes on posts 
class Vote(models.Model):
    """
    Model representing an upvote or downvote on a post.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="votes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="votes")
    vote_type = models.SmallIntegerField()

    class Meta:
        unique_together = ('user', 'post')

# Model for saved posts
class SavedPost(models.Model):
    """
    Model representing a saved post (bookmark) by a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saved_by_users')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} saved {self.post.title}"

# Model for user profiles    
class Profile(models.Model):
    """
    Model that holds additional user information (profile picture).
    It extends Django's built-in User model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = CloudinaryField('image', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Profile of {self.user.username}'