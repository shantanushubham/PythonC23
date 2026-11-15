# Django Tasks Mobile

React Native (Expo, TypeScript) client for the Django Tasks API in [`../django_tasks`](../django_tasks). One codebase for iOS and Android.

## Features

- Register, log in and log out (JWT)
- Silent access-token refresh. The backend's access token lives only 2 minutes and refresh tokens rotate, so the API client shares a single in-flight refresh and retries the failed request.
- Tokens are stored in the iOS Keychain / Android Keystore via `expo-secure-store`
- Task list with infinite scroll, pull to refresh, debounced search, All / Active / Done filter and newest/oldest sorting
- Create, edit, complete (optimistic) and delete tasks
- Profile screen, light/dark mode

## Run it

```bash
# 1. Backend: listen on all interfaces so devices can reach it
cd ../django_tasks
python manage.py runserver 0.0.0.0:8000

# 2. App
cd ../django_tasks_mobile
npm install
cp .env.example .env.local     # then set EXPO_PUBLIC_API_URL (see below)
npx expo start --clear
```

Scan the QR code with **Expo Go** (Android) or the Camera app (iOS). Your phone and computer must be on the same Wi-Fi. To use a simulator instead, press `i` (iOS) or `a` (Android) in the Expo terminal, or run `npm run ios` / `npm run android`.

### Pointing the app at the backend

Set `EXPO_PUBLIC_API_URL` in `.env.local`:

| Where the app runs | `EXPO_PUBLIC_API_URL` | Extra steps |
| --- | --- | --- |
| Physical device (Expo Go) | `http://<computer-LAN-IP>:8000` | find the IP with `ipconfig getifaddr en0` |
| iOS simulator | `http://localhost:8000` | none |
| Android emulator | `http://localhost:8000` | `adb reverse tcp:8000 tcp:8000` (needs Android SDK platform-tools) |

The Django settings accept any `Host` header while `DEBUG = True`, so no `ALLOWED_HOSTS` change is needed in development.

`EXPO_PUBLIC_*` values are inlined at bundle time. After changing `.env.local`, restart with `npx expo start --clear`.

### Troubleshooting

- **"Can't reach the server at ..."**: the backend isn't running on `0.0.0.0:8000`, the IP in `.env.local` is stale (it changes when you switch Wi-Fi), or the macOS firewall is blocking Python.
- **`spawn adb ENOENT`**: Android Studio / platform-tools aren't installed. Use Expo Go on a phone, or install Android Studio and add `$ANDROID_HOME/platform-tools` to your `PATH`.
- **Expo Go says the SDK is incompatible**: this project uses Expo SDK 58; update Expo Go.

## Project layout

```
src/
  app/              Expo Router screens
    index.tsx       entry route: redirects to /login or /tasks
    (auth)/         login, register          (only reachable when signed out)
    (app)/          tasks, task/[id], profile (only reachable when signed in)
  api/              fetch client (auth + refresh) and endpoint wrappers
  auth/             AuthContext and secure token storage
  components/       shared UI
  tasks/            cross-screen "task changed" invalidation
  theme/            colours, spacing, dark mode
```

`task/[id]` handles both creating (`/task/new`) and editing (`/task/42`).

## Scripts

```bash
npx tsc --noEmit   # typecheck
npx expo lint      # lint
npx expo-doctor    # dependency / config check
```

## Backend notes

- `GET /api/task/` returns every user's tasks. The app labels other users' tasks and makes them read-only, but the API itself does not enforce ownership on update/delete.
- There is no logout endpoint, so "Log out" only clears the tokens on the device.
- On web (`react-native-web` is installed for debugging only), the browser blocks API calls because the backend sends no CORS headers, and confirmation dialogs (`Alert`) do nothing. The app targets iOS and Android.
