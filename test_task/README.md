### Инструкция по запуску проекта
## 1. Создание файла переменных окружения
В корневой директории проекта (test_task) создайте файл с названием .env. Добавьте в него следующие строки:
````
ACCESS_TOKEN=ваш_токен_инстаграм

DB_NAME=test_task
DB_USER=postgres
DB_PASSWORD=postgres
DB_PORT=5432
DB_HOST=db

#Версия API
INSTAGRAM_API_VERSION=v25.0
````
## 2. Запуск проекта
После завершения сборки запустите контейнеры командой:
``bash
docker-compose up --build
``
## Решение ошибки ConnectionError
Если при работе внутри Docker возникает ошибка ConnectionError при обращении к Instagram:
Убедитесь, что на вашем компьютере включен системный VPN (не только в браузере), так как instagram заблокирован в России