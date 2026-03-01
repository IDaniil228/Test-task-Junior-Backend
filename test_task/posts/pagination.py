from rest_framework.pagination import CursorPagination

class PostCursorPagination(CursorPagination):
    page_size = 2           # Количество постов за раз
    ordering = '-created_at' # Обязательно! Поле для сортировки (от новых к старым)
    cursor_query_param = 'cursor' # Параметр в URL