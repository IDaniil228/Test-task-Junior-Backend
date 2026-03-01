Вот готовый текст для вашего README.md. Скопируйте его целиком:

code
Markdown
download
content_copy
expand_less
# Instagram API Integration Service

Проект для работы с Instagram Graph API, упакованный в Docker-контейнер.

## 🚀 Требования
Для запуска проекта вам понадобятся:
* **Docker**
* **Docker Compose**

---

## 🛠 Установка и запуск

### 1. Настройка переменных окружения (.env)
Перед запуском необходимо создать файл `.env` в корневой директории проекта. В этом файле должны храниться ваши секретные ключи и настройки API.

**Пример содержимого файла `.env`:**
```env
# Версия API Instagram (по умолчанию v25.0)
INSTAGRAM_API_VERSION=v25.0
# Ваш Access Token от Facebook Developers
ACCESS_TOKEN=your_access_token_here

# Другие настройки (если требуются)
DEBUG=True
2. Сборка и запуск проекта

Для сборки Docker-образа и запуска всех контейнеров выполните следующую команду в терминале:

code
Bash
download
content_copy
expand_less
docker-compose up --build

Флаг --build принудительно пересоберет образы, если вы вносили изменения в код или Dockerfile.

Если вы хотите запустить проект в фоновом режиме (в консоли не будут бежать логи), используйте: docker-compose up -d --build.

🔍 Полезные команды

Остановить контейнеры:

code
Bash
download
content_copy
expand_less
docker-compose down

Просмотр логов в реальном времени:

code
Bash
download
content_copy
expand_less
docker-compose logs -f

Пересборка проекта (без запуска):

code
Bash
download
content_copy
expand_less
docker-compose build
⚠️ Решение проблем (Troubleshooting)
ConnectionError в Docker

Если при выполнении запросов к Instagram возникает ошибка ConnectionError, проверьте следующее:

VPN/Прокси: Если вы находитесь в регионе, где доступ к Instagram ограничен, убедитесь, что на вашей хост-машине запущен системный VPN, или настройте прокси внутри контейнера.

DNS: Если контейнер не может найти адрес graph.instagram.com, добавьте Google DNS в ваш docker-compose.yml:

code
Yaml
download
content_copy
expand_less
services:
  web:
    dns:
      - 8.8.8.8

Файл .env: Убедитесь, что файл .env создан и переменные в нем указаны без лишних пробелов и кавычек.

Технологический стек

Python (Requests)

Docker & Docker Compose

Instagram Graph API

code
Code
download
content_copy
expand_less