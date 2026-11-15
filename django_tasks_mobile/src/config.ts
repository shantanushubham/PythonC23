/**
 * Base URL of the Django backend, without a trailing slash and without `/api`.
 * Override with EXPO_PUBLIC_API_URL (see .env.example).
 */
export const API_URL = (process.env.EXPO_PUBLIC_API_URL ?? 'http://localhost:8000').replace(
  /\/+$/,
  '',
);

export const PAGE_SIZE = 20;
export const REQUEST_TIMEOUT_MS = 15000;
