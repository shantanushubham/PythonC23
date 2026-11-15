import { API_URL, REQUEST_TIMEOUT_MS } from '@/config';
import { tokenStore } from '@/auth/tokenStore';

export class ApiError extends Error {
  status: number;
  /** Per-field messages from DRF validation errors, e.g. { email: "Enter a valid email." } */
  fieldErrors: Record<string, string>;

  constructor(status: number, message: string, fieldErrors: Record<string, string> = {}) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.fieldErrors = fieldErrors;
  }

  get isNetworkError() {
    return this.status === 0;
  }
}

type Query = Record<string, string | number | boolean | undefined | null>;

type RequestOptions = {
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  body?: unknown;
  query?: Query;
  /** Attach the bearer token and refresh it on 401. Defaults to true. */
  auth?: boolean;
};

let onSessionExpired: (() => void) | null = null;

/** Called when the refresh token is rejected and the user has to log in again. */
export function setSessionExpiredHandler(handler: (() => void) | null) {
  onSessionExpired = handler;
}

function buildUrl(path: string, query?: Query) {
  const url = new URL(`${API_URL}/api${path}`);
  if (query) {
    for (const [key, value] of Object.entries(query)) {
      if (value !== undefined && value !== null && value !== '') {
        url.searchParams.set(key, String(value));
      }
    }
  }
  return url.toString();
}

async function fetchWithTimeout(url: string, init: RequestInit): Promise<Response> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
  try {
    return await fetch(url, { ...init, signal: controller.signal });
  } catch {
    throw new ApiError(
      0,
      `Can't reach the server at ${API_URL}. Check that the backend is running and the address is correct.`,
    );
  } finally {
    clearTimeout(timer);
  }
}

/**
 * Exchanges the refresh token for a new access token.
 *
 * The backend rotates + blacklists refresh tokens, so two parallel refreshes with
 * the same token would make the second one fail. A single in-flight promise is
 * shared by every caller to avoid that.
 */
let refreshInFlight: Promise<string | null> | null = null;

function refreshAccessToken(): Promise<string | null> {
  if (!refreshInFlight) {
    refreshInFlight = (async () => {
      const tokens = await tokenStore.get();
      if (!tokens?.refresh) return null;

      const res = await fetchWithTimeout(buildUrl('/token/refresh/'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ refresh: tokens.refresh }),
      });

      // The refresh token itself is invalid / expired / blacklisted.
      if (res.status === 400 || res.status === 401) return null;
      if (!res.ok) throw new ApiError(res.status, 'Could not refresh your session.');

      const data = (await res.json()) as { access: string; refresh?: string };
      // ROTATE_REFRESH_TOKENS=True: a new refresh token comes back every time.
      await tokenStore.set({ access: data.access, refresh: data.refresh ?? tokens.refresh });
      return data.access;
    })().finally(() => {
      refreshInFlight = null;
    });
  }
  return refreshInFlight;
}

function describeError(status: number, data: unknown): ApiError {
  const fieldErrors: Record<string, string> = {};
  let message = `Request failed (${status}).`;

  if (data && typeof data === 'object') {
    const record = data as Record<string, unknown>;
    if (typeof record.detail === 'string') message = record.detail;
    else if (typeof record.error === 'string') message = record.error;
    else {
      for (const [field, value] of Object.entries(record)) {
        const text = Array.isArray(value) ? value.join(' ') : String(value);
        fieldErrors[field] = text;
      }
      const first = Object.values(fieldErrors)[0];
      if (first) message = first;
    }
  } else if (status >= 500) {
    message = 'The server ran into a problem. Please try again.';
  }

  return new ApiError(status, message, fieldErrors);
}

export async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { method = 'GET', body, query, auth = true } = options;
  const url = buildUrl(path, query);

  const send = async (access?: string) => {
    const headers: Record<string, string> = { Accept: 'application/json' };
    if (body !== undefined) headers['Content-Type'] = 'application/json';
    if (access) headers.Authorization = `Bearer ${access}`;
    return fetchWithTimeout(url, {
      method,
      headers,
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
  };

  const tokens = auth ? await tokenStore.get() : null;
  let res = await send(tokens?.access);

  if (res.status === 401 && auth) {
    const freshAccess = await refreshAccessToken();
    if (!freshAccess) {
      await tokenStore.clear();
      onSessionExpired?.();
      throw new ApiError(401, 'Your session has expired. Please log in again.');
    }
    res = await send(freshAccess);
  }

  if (res.status === 204) return undefined as T;

  let data: unknown = null;
  try {
    data = await res.json();
  } catch {
    // empty or non-JSON body
  }

  if (!res.ok) throw describeError(res.status, data);
  return data as T;
}
