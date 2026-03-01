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