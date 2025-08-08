from django.urls import path
from .views import PostList, PostDetail, VoteView, PostCreate, PostUpdate, PostDelete, CommentUpdate, CommentDelete, UserProfile, UserProfileUpdate, SavedPostView, SavedPostListView 

urlpatterns = [
    path('', PostList.as_view(), name='home'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    path('edit/<slug:slug>/', PostUpdate.as_view(), name='post_edit'),
    path('delete/<slug:slug>/', PostDelete.as_view(), name='post_delete'),
    path('vote/<slug:slug>/', VoteView.as_view(), name='vote'),
    path('comment/edit/<int:pk>/', CommentUpdate.as_view(), name='comment_edit'),
    path('comment/delete/<int:pk>/', CommentDelete.as_view(), name='comment_delete'),
    path('profile/<str:username>/', UserProfile.as_view(), name='user_profile'),
    path('profile/<str:username>/edit/', UserProfileUpdate.as_view(), name='user_profile_edit'),
    path('<slug:slug>/save/', SavedPostView.as_view(), name='saved_post'),
    path('saved-posts/', SavedPostListView.as_view(), name='saved_posts_list'),
]