import os

import requests
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, HTTPError
from rest_framework import status
from rest_framework.exceptions import APIException

load_dotenv()


class InstagramClient:
    @staticmethod
    def get_posts(access_token: str) -> list:
        try:
            version_api = os.environ.get('INSTAGRAM_API_VERSION', 'v25.0')
            params = {
                "access_token": access_token,
                "fields": "id,caption,media_url,permalink,timestamp,media_type,like_count,comments_count",
                "limit": 2
            }
            url = f"https://graph.instagram.com/{version_api}/me/media"
            response = requests.get(url=url, params=params)
            response.raise_for_status()
            data = response.json().get("data")
            posts = []
            while data:
                posts.extend(data)
                paging = response.json().get("paging", {})
                cursors = paging.get("cursors", {})
                after_cursor = cursors.get("after")
                if not after_cursor:
                    break

                params["after"] = after_cursor
                response = requests.get(url=url, params=params)
                response.raise_for_status()
                data = response.json()["data"]
            return posts

        except ConnectionError:
            error = APIException({
                'status': 'error',
                'detail': 'Не удалось подключиться к Instagram'
            })
            error.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            raise error

    @staticmethod
    def send_comment(access_token: str, post_id: str, message: str) -> str:
        try:
            url = f"https://graph.instagram.com/{post_id}/comments"
            params = {
                "access_token": access_token,
                "message" : message,
            }
            response = requests.post(url=url, params=params)
            response.raise_for_status()
            return response.json()["id"]

        except HTTPError as e:
            if e.response.json()["error"]["type"] == "IGApiException":
                error = APIException({
                    'status': 'error',
                    'detail': f'The user no longer has a post with this id {post_id}',
                    'type' : 'IGApiException'
                })
                error.status_code = status.HTTP_400_BAD_REQUEST
                raise error
            raise e

