from django.urls import path, include, reverse
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    SignUp,
    Contact
)

from .views import *


urlpatterns = [
    path('', PostListView.as_view(), name='forum-index'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('drafts/', DraftListView.as_view(), name='post_draft_list'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', about, name='forum-about'),
    path('signup/', SignUp, name='signup'),
    path('success/', Success, name='success'),
    path('contact/', Contact, name='contact'),
    path('post/<int:pk>/comment/', add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', comment_remove, name='comment_remove'),
]
