from django.db import transaction
from django.db.models import QuerySet
from rest_framework.generics import get_object_or_404

from posts.models import InstagramPost, Comment


class PostRepository:
    @staticmethod
    def upsert_user_posts(posts_data: list) -> list[InstagramPost]:
        incoming_ids = [p.get("id") for p in posts_data if p.get("id")]
        posts = []
        for post_data in posts_data:
            posts.append(InstagramPost(
                instagram_id=post_data.get("id"),
                caption=post_data.get("caption", ""),
                likes_count=post_data.get("likes_count", 0),
                comments_count=post_data.get("comments_count", 0),
                media_url=post_data.get("media_url", ""),
                permalink=post_data.get("permalink"),
                published_at=post_data.get("timestamp"),
                media_type=post_data.get("media_type"),
            ))

        with transaction.atomic():
            created_post = InstagramPost.objects.bulk_create(
                posts,
                update_conflicts=True,
                update_fields=["caption", "likes_count", "comments_count",
                               "media_url", "permalink", "published_at", "media_type"],
                unique_fields=["instagram_id"]
            )
            InstagramPost.objects.exclude(instagram_id__in=incoming_ids).delete()
        return created_post

    @staticmethod
    def get_all_post() -> QuerySet[InstagramPost]:
        return InstagramPost.objects.all()

    @staticmethod
    def get_post_by_id(post_id: int) -> InstagramPost:
        print(post_id)
        return get_object_or_404(InstagramPost, id=post_id)

    @staticmethod
    def delete_post_by_id(post_id: int) -> InstagramPost:
        post = get_object_or_404(InstagramPost, id=post_id)
        return post.delete()

    @staticmethod
    def save_comment(message: str, post: InstagramPost, instagram_id: str) -> Comment:
        comment = Comment.objects.create(message=message, post=post, instagram_id=instagram_id)
        post.comments_count += 1
        post.save()
        return comment

