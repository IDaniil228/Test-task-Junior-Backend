import requests
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Кастомный обработчик исключений для DRF.
    Форматирует все ответы с ошибками в единый формат.
    """
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {
            "status": "error",
            "detail": response.data
        }

    elif isinstance(exc, requests.exceptions.HTTPError):
        upstream_status = exc.response.status_code

        try:
            detail = exc.response.json()
        except:
            detail = exc.response.text

        if upstream_status >= 500:
            final_status = status.HTTP_502_BAD_GATEWAY
            detail = "Сервис Instagram временно недоступен"
        else:
            final_status = upstream_status

        response = Response(
            {
                "status": "error",
                "source": "instagram",
                "detail": detail
            },
            status=final_status
        )

    else:
        response = Response(
            {
                "status": "error",
                "message": "Внутренняя ошибка нашего сервера",
                "detail": str(exc)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response