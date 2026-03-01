from django.contrib import admin
from django.urls import path, include

from posts.views import PostUpsertView, PostListView, SendCommentView

urlpatterns = [
    path("sync/", PostUpsertView.as_view(), name="sync"),
    path("posts/", PostListView.as_view(), name="all_posts"),
    path(f"posts/<int:post_id>/comment/", SendCommentView.as_view(), name="send_comment"),
]