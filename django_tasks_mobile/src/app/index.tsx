import { Redirect } from 'expo-router';

import { useAuth } from '@/auth/AuthContext';

/**
 * Entry route ("/"). It is outside the protected groups so it always exists, whatever the auth
 * state is, and simply forwards to the right place.
 */
export default function Index() {
  const { status } = useAuth();

  // The splash screen is still visible while the stored session is being restored.
  if (status === 'loading') return null;

  return <Redirect href={status === 'signedIn' ? '/tasks' : '/login'} />;
}
