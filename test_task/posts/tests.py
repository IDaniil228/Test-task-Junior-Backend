import os

from unittest.mock import patch

from django.urls import reverse
from requests import HTTPError
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.test import APITestCase

from posts.models import Comment, InstagramPost


class SendCommentViewTest(APITestCase):
    def setUp(self):
        post = InstagramPost.objects.create(
            instagram_id="123456789",
            caption="Мой первый пост в Instagram! #тест",
            likes_count=150,
            comments_count=25,
            media_url="https://instagram.com/p/123456789/media",
            permalink="https://instagram.com/p/123456789",
            published_at="2026-02-26T19:33:25+0000",
            media_type="IMAGE"
        )
        self.url = reverse('send_comment', kwargs={'post_id': post.id})

        # Данные для отправки
        self.valid_payload = {
            'message': 'Тестовый комментарий'
        }

    @patch.dict(os.environ, {"ACCESS_TOKEN": "fake_test_token"})
    @patch('posts.views.InstagramClient')
    def test_post_comment_success_creation(self, MockInstagramClient):
        before_count_comment = len(Comment.objects.all())
        mock_client_instance = MockInstagramClient.return_value
        mock_client_instance.send_comment.return_value = "111"
        response = self.client.post(self.url, self.valid_payload)
        after_count_comment = len(Comment.objects.all())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(before_count_comment, after_count_comment - 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_post_comment_dont_exist_post_by_id(self):
        self.url = reverse('send_comment', kwargs={'post_id': -1})
        response = self.client.post(self.url, self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('posts.views.InstagramClient')
    def test_comment_to_non_existent_post_returns_error(self, MockInstagramClient):
        mock_client_instance = MockInstagramClient.return_value
        mock_client_instance.send_comment.side_effect = APIException({
                    'status': 'error',
                    'detail': f'The user no longer has a post with this id',
                    'type' : 'IGApiException'
                })
        response = self.client.post(self.url, self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
