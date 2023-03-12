# praktikum_new_diplom "foodgram-project-react"


### Описание
«"foodgram-project-react"» - пользователь проекта может создавать свои рецепты, читать рецепты других пользователей, подписываться на интересных авторов, добавлять лучшие рецепты в избранное, а также создавать список покупок и загружать его в txt формате

Добавить добавить рецепт, подписаться, добавлять рецепты в избранное можно только аутентифицированным пользователям.


### Использумые технологии

[Python 3.710](https://docs.python.org/3.10/whatsnew/3.10.html)

[Django 3.2.18](https://docs.djangoproject.com/en/4.1/releases/3.2.186/)

[DjangoRestFramework 3.14.0](https://www.django-rest-framework.org/community/release-notes/)

[gunicorn 20.0.4](https://docs.gunicorn.org/en/stable/)

[Docker](https://docs.docker.com/)



[Работающий проект доступен по адресу]: (http://nadim13.hopto.org)


Статус выполнения workflow

![example workflow](https://github.com/nadim1309/foodgram-project-react/actions/workflows/foodgram.yml/badge.svg)


### КАК ЗАПУСТИТЬ ПРОЕКТ:

проект запускается в 4 контейнерах:

```
nginx:1.19.3
foodgram-backend:v1
foodgram-frontend:v1
postgres:11.4
```
контейнер foodgram-frontend:v1 после сборки завершает свою работу

клонируйте репозиторий к себе на сервер

```
git clone https://github.com/Nadim1309/foodgram-project-react.git
```
Перейдите в папку infra

```
cd foodgram-project-react/infra/

```

в папке infra создайте файл .env и заполните его дефолтными значениями
```
DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

в папке infra выполните команду

```
docker-compose up --build
```

запустите миграции
```
docker-compose exec backend python manage.py migrate 
```

наполните сайт тестовыми данными
```
docker-compose exec backend python manage.py loaddata dump.json
```
соберите статические файлы
```
docker-compose exec backend python manage.py collectstatic --no-input 
```
создайте суперпользователя
```
docker-compose exec backend python manage.py createsuperuser 
```
Авторы:


[Шакиржанов Надим](https://github.com/Nadim1309)
