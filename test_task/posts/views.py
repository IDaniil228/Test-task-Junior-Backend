import os

from dotenv import load_dotenv
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.clients.InstagramClient import InstagramClient
from posts.pagination import PostCursorPagination
from posts.repository.PostRepository import PostRepository
from posts.serializers import PostSerializer
from posts.serializers.comment import CommentCreateSerializer, CommentSerializer
from posts.service.PostService import PostService


load_dotenv()

class PostUpsertView(APIView):

    def setup(self, request, *args, **kwargs):
        """
        Инициализирует зависимости для работы представления.
        Создает экземпляр PostService, передавая ему репозиторий и клиент Instagram.
        """
        super().setup(request, *args, **kwargs)
        self.post_service = PostService(
            post_repository=PostRepository(),
            instagram_client=InstagramClient()
        )

    def post(self, request):
        """
        Обрабатывает POST-запрос на обновление и сохранение постов из Instagram.
        Получает токен доступа из переменных окружения и инициирует процесс
        синхронизации данных в базе данных через сервисный слой.
        """
        access_token = os.environ.get("ACCESS_TOKEN")
        queryset = self.post_service.update_posts(access_token=access_token)
        return Response(
            {
                "status": "success",
                "message": f"Успешно обработано {len(queryset)} постов",
            },
            status=status.HTTP_201_CREATED
            )


class PostListView(APIView):

    pagination_class = PostCursorPagination

    def setup(self, request, *args, **kwargs):
        """
        Подготавливает зависимости перед выполнением запроса.
        Настраивает сервисный слой для работы с постами.
        """
        super().setup(request, *args, **kwargs)
        self.post_service = PostService(
            post_repository=PostRepository(),
            instagram_client=InstagramClient()
        )

    def get(self, request):
        """
        Обрабатывает GET-запрос для получения списка всех сохраненных постов.
        Поддерживает курсорную пагинацию (PostCursorPagination) для эффективного
        листания больших списков данных.
        """
        queryset = self.post_service.get_all_posts()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)

        if page is not None:
            serializer = PostSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)


class SendCommentView(APIView):

    def setup(self, request, *args, **kwargs):
        """
        Инициализирует сервисы, необходимые для отправки комментариев.
        """
        super().setup(request, *args, **kwargs)
        self.post_service = PostService(
            post_repository=PostRepository(),
            instagram_client=InstagramClient()
        )

    def post(self, request, post_id):
        """
        Обрабатывает POST-запрос для отправки нового комментария к посту.
        Проверяет входящие данные на валидность, отправляет сообщение в Instagram
        и сохраняет созданный комментарий в локальную базу данных.
        """
        access_token = os.environ.get("ACCESS_TOKEN")
        serializer = CommentCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "status": "error",
                    "detail": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        comment = self.post_service.save_comments(
            access_token=access_token,
            message=serializer.data['message'],
            post_id=post_id
        )
        serializer = CommentSerializer(comment)
        return Response(
            {
                "status": "success",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
