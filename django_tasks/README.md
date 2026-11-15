# Django Tasks

A task manager with a Django REST API and a React Native (Expo, TypeScript) mobile app for iOS and Android.

```
django_tasks/            Django backend (this folder)
  config/                project settings and root URLs
  tasks/                 models, serializers, views, JWT auth
django_tasks_mobile/     React Native app  ->  see its README
```

## Backend

### Requirements

- Python 3.14 and Docker (for PostgreSQL)

### Setup

```bash
cd django_tasks
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

docker compose up -d                 # PostgreSQL on :5432 (postgres/postgres)
python manage.py migrate
python manage.py createsuperuser     # optional
python manage.py runserver 0.0.0.0:8000
```

`0.0.0.0` makes the server reachable from a phone on the same Wi-Fi. `ALLOWED_HOSTS` accepts any host while `DEBUG = True`; set real hostnames before deploying with `DEBUG = False`.

### API

Base URL: `http://localhost:8000/api/`

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| POST | `/user/` | none | Register: `username`, `email`, `first_name`, `last_name`, `password` |
| POST | `/login/` | none | `{email, password}` -> `{access, refresh}` |
| POST | `/token/refresh/` | none | `{refresh}` -> new `access` and a rotated `refresh` |
| GET | `/user/{id}/` | JWT | Fetch a user profile |
| GET | `/user/tasks/` | JWT | Tasks of the logged-in user (404 when there are none) |
| GET | `/task/` | - | Paginated list. Query: `page`, `page_size` (max 50), `completed`, `search`, `ordering` (`created_at` / `-created_at`) |
| POST | `/task/` | JWT | Create a task (`title`, `description`, `completed`) |
| GET/PATCH/PUT/DELETE | `/task/{id}/` | - | Read, update or delete a task |
| GET | `/task/completed/` | - | All completed tasks, unpaginated |

Authenticate with `Authorization: Bearer <access token>`.

Access tokens live **2 minutes** and refresh tokens **7 days**. Refresh tokens rotate and the old one is blacklisted, so always store the new `refresh` returned by `/token/refresh/`.

### Known limitations

- `/task/` lists every user's tasks, and update/delete are not restricted to the task's owner. The mobile app makes other users' tasks read-only, but the API does not enforce it.
- There is no logout endpoint; clients just discard their tokens.
- `SECRET_KEY`, the JWT signing key and the database credentials in `config/settings.py` are development values.

## Mobile app

See [`django_tasks_mobile/README.md`](../django_tasks_mobile/README.md) for running it on a simulator or a physical device.

Quick start for a phone with Expo Go:

```bash
# 1. backend reachable on your network (see above)
# 2. point the app at your computer's LAN IP
cd ../django_tasks_mobile
npm install
echo "EXPO_PUBLIC_API_URL=http://<your-LAN-IP>:8000" > .env.local
npx expo start --clear
```
