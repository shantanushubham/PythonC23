import {
  createContext,
  use,
  useCallback,
  useEffect,
  useMemo,
  useState,
  type PropsWithChildren,
} from 'react';

import { authApi, type RegisterInput } from '@/api/auth';
import { setSessionExpiredHandler } from '@/api/client';
import type { User } from '@/types';

import { tokenStore } from './tokenStore';

type Status = 'loading' | 'signedOut' | 'signedIn';

type AuthContextValue = {
  status: Status;
  /** Id of the logged-in user, read from the JWT. Available as soon as we're signed in. */
  userId: number | null;
  /** Full profile; loaded in the background after sign-in. */
  user: User | null;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (input: RegisterInput) => Promise<void>;
  signOut: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function useAuth() {
  const value = use(AuthContext);
  if (!value) throw new Error('useAuth must be used inside <AuthProvider>');
  return value;
}

/** Reads the `user_id` claim from a JWT. The signature is verified by the server, not here. */
function userIdFromJwt(token: string): number | null {
  try {
    const payload = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/');
    const padded = payload + '='.repeat((4 - (payload.length % 4)) % 4);
    const claims = JSON.parse(atob(padded)) as { user_id?: number | string };
    const id = Number(claims.user_id);
    return Number.isFinite(id) ? id : null;
  } catch {
    return null;
  }
}

export function AuthProvider({ children }: PropsWithChildren) {
  const [status, setStatus] = useState<Status>('loading');
  const [userId, setUserId] = useState<number | null>(null);
  const [user, setUser] = useState<User | null>(null);

  const loadProfile = useCallback(async (id: number) => {
    try {
      setUser(await authApi.getUser(id));
    } catch {
      // Not fatal: the app works without the profile (it only feeds the profile screen).
    }
  }, []);

  const clearSession = useCallback(() => {
    setUserId(null);
    setUser(null);
    setStatus('signedOut');
  }, []);

  // Restore the session on launch.
  useEffect(() => {
    let cancelled = false;
    (async () => {
      const tokens = await tokenStore.get();
      const id = tokens ? userIdFromJwt(tokens.refresh) : null;
      if (cancelled) return;
      if (tokens && id !== null) {
        setUserId(id);
        setStatus('signedIn');
        loadProfile(id);
      } else {
        if (tokens) await tokenStore.clear();
        setStatus('signedOut');
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [loadProfile]);

  // The API client tells us when the refresh token is no longer accepted.
  useEffect(() => {
    setSessionExpiredHandler(clearSession);
    return () => setSessionExpiredHandler(null);
  }, [clearSession]);

  const signIn = useCallback(
    async (email: string, password: string) => {
      const tokens = await authApi.login(email.trim(), password);
      const id = userIdFromJwt(tokens.access);
      if (id === null) throw new Error('The server returned an unexpected token.');
      await tokenStore.set(tokens);
      setUserId(id);
      setStatus('signedIn');
      loadProfile(id);
    },
    [loadProfile],
  );

  const signUp = useCallback(
    async (input: RegisterInput) => {
      await authApi.register({ ...input, email: input.email.trim() });
      await signIn(input.email, input.password);
    },
    [signIn],
  );

  const signOut = useCallback(async () => {
    // The backend has no logout/blacklist endpoint, so signing out is local.
    await tokenStore.clear();
    clearSession();
  }, [clearSession]);

  const value = useMemo(
    () => ({ status, userId, user, signIn, signUp, signOut }),
    [status, userId, user, signIn, signUp, signOut],
  );

  return <AuthContext value={value}>{children}</AuthContext>;
}
