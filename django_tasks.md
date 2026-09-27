# How to create the Django Tasks application

These are the steps used to create the `django_tasks` project: a Django project named `config`, a `tasks` app, and Django REST framework, all inside a virtual environment.

From the `PythonC23` folder:

## 1. Create the project folder

```bash
mkdir django_tasks
cd django_tasks
```

## 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows
```

The prompt should show `(.venv)` once the environment is active. Install packages only after activating it, so they stay inside this project.

## 3. Install Django and Django REST framework

```bash
pip install django
pip install djangorestframework
```

This project was created with:

- Django 6.1.1
- Django REST framework 3.18.1

## 4. Start the Django project

The trailing `.` puts `manage.py` in the current folder and names the settings package `config` (instead of a nested folder with the same name as the project).

```bash
django-admin startproject config .
```

That creates:

```text
django_tasks/
├── .venv/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```

`config/settings.py` holds project settings. `config/urls.py` holds the root URL routes. `manage.py` is the command-line entry point and points at `config.settings`.

## 5. Create the tasks app

An app is one feature inside the project. This command creates the `tasks` app in the current folder:

```bash
python manage.py startapp tasks
```

That adds:

```text
django_tasks/
├── .venv/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tasks/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
└── manage.py
```

`tasks/models.py` is where the app’s database models go. `tasks/views.py` is where its views go. `tasks/admin.py` registers models with the admin site.

## 6. Register the app and Django REST framework

`pip install` only puts Django REST framework in the virtual environment, and `startapp` only creates the `tasks` folder. Django loads both after they are listed in `INSTALLED_APPS` in `config/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'tasks',
]
```

## 7. Apply migrations and run the server

```bash
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/. The admin site is at http://127.0.0.1:8000/admin/.

Stop the server with `Ctrl+C`. Leave the virtual environment with `deactivate`.
