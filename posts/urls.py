from django.urls import path
from .views import PostList, PostDetail, VoteView

urlpatterns = [
    path('', PostList.as_view(), name='home'),
    path('<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    path('vote/<slug:slug>/', VoteView.as_view(), name='vote'),
]