from django.db import models

class InstagramPost(models.Model):
    id = models.AutoField(
        primary_key=True,
        verbose_name="Внутренний ID"
    )
    instagram_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name="ID поста в Instagram"
    )
    caption = models.TextField(
        blank=True,
        verbose_name="Текст поста (описание)"
    )
    likes_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество лайков"
    )
    comments_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество комментариев"
    )
    media_url = models.URLField(
        max_length=1000,
        verbose_name="Ссылка на медиафайл (CDN)"
    )
    permalink = models.URLField(
        max_length=1000,
        verbose_name="Постоянная ссылка"
    )
    published_at = models.DateTimeField(
        db_index=True,
        verbose_name="Дата публикации в Instagram"
    )
    media_type = models.CharField(
        max_length=50,
        verbose_name="Тип медиа"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата загрузки в базу"
    )

class Comment(models.Model):
    post = models.ForeignKey(
        InstagramPost,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Пост"
    )
    message = models.TextField(
        null=False,
        blank=False,
        verbose_name="Текст комментария"
    )
    instagram_id = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        unique=True,
        verbose_name="ID комментария в Instagram"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )