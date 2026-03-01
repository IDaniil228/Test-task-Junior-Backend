from dataclasses import dataclass

from django.db.models import QuerySet
from rest_framework.exceptions import APIException

from posts.clients.InstagramClient import InstagramClient
from posts.models import InstagramPost, Comment
from posts.repository.PostRepository import PostRepository

@dataclass
class PostService:

    post_repository: PostRepository
    instagram_client: InstagramClient

    def update_posts(self, access_token: str) -> QuerySet[InstagramPost]:
        posts = self.instagram_client.get_posts(access_token=access_token)
        posts = self.post_repository.upsert_user_posts(posts_data=posts)
        return posts

    def get_all_posts(self) -> QuerySet[InstagramPost]:
        posts = self.post_repository.get_all_post()
        return posts

    def save_comments(self, access_token: str, post_id: int, message: str) -> Comment:
        post = self.post_repository.get_post_by_id(post_id)
        try:
            comment_id = self.instagram_client.send_comment(
                access_token=access_token,
                post_id=post.instagram_id,
                message=message
            )
            comment = self.post_repository.save_comment(post=post, message=message, instagram_id=comment_id)
            return comment

        except APIException as e:
            if e.detail["type"] == "IGApiException":
                self.post_repository.delete_post_by_id(post_id=post.id)
            raise e
