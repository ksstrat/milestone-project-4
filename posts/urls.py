from django.urls import path
from .views import PostList, PostDetail, VoteView, PostCreate, PostUpdate, PostDelete

urlpatterns = [
    path('', PostList.as_view(), name='home'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    path('edit/<slug:slug>/', PostUpdate.as_view(), name='post_edit'),
    path('delete/<slug:slug>/', PostDelete.as_view(), name='post_delete'),
    path('vote/<slug:slug>/', VoteView.as_view(), name='vote'),
]