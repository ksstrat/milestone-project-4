from django.contrib import admin
from .models import Category, Post, Comment, Vote, Profile
from django_summernote.admin import SummernoteModelAdmin
from django.utils.html import format_html

class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_at')
    search_fields = ['title', 'content']
    list_filter = ('status', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

@admin.register(Comment)
class CommentAdmin(SummernoteModelAdmin):
    list_display = ('author', 'display_body_formatted', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('author__username', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

    def display_body_formatted(self, obj):
        """ 
        Formats the comment body as HTML and truncates it for a cleaner admin overview.
        """
        return format_html(obj.body[:150] + '...' if len(obj.body) > 150 else obj.body)
    
    display_body_formatted.short_description = 'Comment'

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'vote_type')
    list_filter = ('vote_type',)
    search_fields = ('user__username', 'post__title')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username', 'user__email')

admin.site.register(Category)
admin.site.register(Post, PostAdmin)