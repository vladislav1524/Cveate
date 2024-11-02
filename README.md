### (EN):
# Cveate ✍️

## Description of the project 📄:
The designer allows you to quickly create a resume by simply filling out your information in forms that you can add and remove at your discretion. You can also download the result in PDF format. 

## Technologies used:
- **Django Formsets**: For adding multiple forms of objects of the same model, for example, projects.
- **Redis**: For caching PDF files and managing task queues.
- **Celery**: For sending emails asynchronously, with Redis as a broker.
- **PostgreSQL**: database.
- **Django-allauth and social-django**: User authentication system through the website and social networks.
- **Docker**: For application containerization.
- **JavaScript**: For managing forms when creating a resume.
- **Bootstrap**: For the design and responsive design of the interface.
 
## How to start the project:
1. Add 'localhost' or your Ngrok domain to the 'ALLOWED_HOSTS' parameter in the file `settings.py `.
2. Create a `.env` file with your changes

An approximate view of your `.env` file (without spaces and quotes):
```
SECRET_KEY=...
DATABASE_NAME=...
DATABASE_USER=...
DATABASE_PASSWORD=...
DATABASE_HOST=db
DATABASE_PORT=...
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
SOCIAL_AUTH_VK_OAUTH2_KEY=...
SOCIAL_AUTH_VK_OAUTH2_SECRET=...
SOCIAL_AUTH_VK_OAUTH2_REDIRECT_URI=...
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=...
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=...
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI=...
SOCIAL_AUTH_DISCORD_KEY=...
SOCIAL_AUTH_DISCORD_SECRET=...
SOCIAL_AUTH_DISCORD_REDIRECT_URI=...
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=...
DEBUG=False
ALLOWED_HOSTS=...
CSRF_TRUSTED_ORIGINS=...
```
3. Run in the main directory at the `manage.py `:
``bash
docker-compose up --build
``
Then run:
```bash
docker-compose exec web python manage.py migrate
```
To create a superuser:

``bash
docker-compose exec web python manage.py createsuperuser
``
## If you want to test authentication via social networks:
1. Install Ngrok to use your computer as a server and publish the site with HTTPS [Link to Ngrok](https://ngrok.com /)

2. In the Ngrok console, run:
```bash
ngrok http 8000
```
Or get a free domain in your personal account and run:
```bash
ngrok http --hostname=<your host> 8000 
```
3. Create and configure applications to log in via social networks, add data to .env:

*Vk*: https://dev.vk.com/ru

*discord*: https://discord.com/developers/applications

*google*: https://console.cloud.google.com/cloud-resource-manager

4. Add your Ngrok domain to CSRF_TRUSTED_ORIGINS and ALLOWED_HOSTS and launch the container.
```bash
docker-compose up --build
```

----------------------------------------------------------------------------------------------------------------


### (РУ):
# Cveate ✍️

## Описание проекта 📄:
Конструктор позволяет быстро создать резюме, просто заполнив свою информацию в формы, которые можно добавлять и убирать на своё усмотрение. Также можно скачать результат в формате PDF.  

## Используемые технологии:
- **Django Formsets**: Для добавления нескольких форм объектов одной модели, например, проектов.
- **Redis**: Для кэширования PDF файлов и управления очередями задач.
- **Celery**: Для асинхронной отправки писем по электронной почте, с Redis в качестве брокера.
- **PostgreSQL**: база данных.
- **Django-allauth и social-django**: Система аутентификации пользователей через сайт и социальные сети.
- **Docker**: Для контейнеризации приложения.
- **JavaScript**: Для управления формами при создании резюме.
- **Bootstrap**: Для оформления и адаптивного дизайна интерфейса.
  
## Как запустить проект 🛠️:
1. Добавьте `localhost` или ваш домен Ngrok в параметр `ALLOWED_HOSTS` в файле `settings.py`.
2. Создайте файл `.env` с вашими переменными (добавьте его в директорию, на уровне `manage.py`).

Примерный вид вашего файла `.env` (без пробелов и кавычек):
```
SECRET_KEY=...
DATABASE_NAME=...
DATABASE_USER=...
DATABASE_PASSWORD=...
DATABASE_HOST=db
DATABASE_PORT=...
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
SOCIAL_AUTH_VK_OAUTH2_KEY=...
SOCIAL_AUTH_VK_OAUTH2_SECRET=...
SOCIAL_AUTH_VK_OAUTH2_REDIRECT_URI=...
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=...
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=...
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI=...
SOCIAL_AUTH_DISCORD_KEY=...
SOCIAL_AUTH_DISCORD_SECRET=...
SOCIAL_AUTH_DISCORD_REDIRECT_URI=...
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=...
DEBUG=False
ALLOWED_HOSTS=...
CSRF_TRUSTED_ORIGINS=...
```
3. Запустите в главной директории на уровне `manage.py`:
```bash
docker-compose up --build
```
Затем выполните миграции:
```bash
docker-compose exec web python manage.py migrate
```
Чтобы создать суперпользователя:

```bash
docker-compose exec web python manage.py createsuperuser
```
## Если хотите протестировать аутентификацию через социальные сети 🌐:
1. Установите Ngrok для использования вашего компьютера как сервера и публикации сайта с HTTPS [Ссылка на Ngrok](https://ngrok.com/)

2. В консоли Ngrok выполните:
```bash
ngrok http 8000
```
Либо получите бесплатный домен в личном кабинете и выполните:
```bash
ngrok http --hostname=<your host> 8000  
```
3. создайте и настройте приложения для входа через соц сети добавьте данные в .env:

*Vk*: https://dev.vk.com/ru

*discord*: https://discord.com/developers/applications

*google*: https://console.cloud.google.com/cloud-resource-manager

4. Добавьте ваш домен Ngrok в CSRF_TRUSTED_ORIGINS и ALLOWED_HOSTS и запустите контейнер.
```bash
docker-compose up --build
```
