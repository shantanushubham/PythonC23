import { Link } from 'expo-router';
import { useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';

import { ApiError } from '@/api/client';
import { useAuth } from '@/auth/AuthContext';
import { AuthScreen } from '@/components/AuthScreen';
import { Button } from '@/components/Button';
import { ErrorBanner } from '@/components/ErrorBanner';
import { TextField } from '@/components/TextField';
import { spacing, useTheme } from '@/theme';

type Form = {
  first_name: string;
  last_name: string;
  username: string;
  email: string;
  password: string;
};

const EMPTY: Form = { first_name: '', last_name: '', username: '', email: '', password: '' };

function validate(form: Form): Partial<Record<keyof Form, string>> {
  const errors: Partial<Record<keyof Form, string>> = {};
  if (!form.first_name.trim()) errors.first_name = 'First name is required.';
  if (!form.last_name.trim()) errors.last_name = 'Last name is required.';
  if (!form.username.trim()) errors.username = 'Username is required.';
  if (!/^\S+@\S+\.\S+$/.test(form.email.trim())) errors.email = 'Enter a valid email address.';
  if (form.password.length < 8) errors.password = 'Use at least 8 characters.';
  return errors;
}

export default function RegisterScreen() {
  const { signUp } = useAuth();
  const { colors } = useTheme();

  const [form, setForm] = useState<Form>(EMPTY);
  const [fieldErrors, setFieldErrors] = useState<Partial<Record<keyof Form, string>>>({});
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const set = (key: keyof Form) => (value: string) => setForm((prev) => ({ ...prev, [key]: value }));

  const submit = async () => {
    if (submitting) return;
    const errors = validate(form);
    setFieldErrors(errors);
    setError(null);
    if (Object.keys(errors).length > 0) return;

    setSubmitting(true);
    try {
      await signUp({
        ...form,
        first_name: form.first_name.trim(),
        last_name: form.last_name.trim(),
        username: form.username.trim(),
      });
    } catch (e) {
      if (e instanceof ApiError) {
        // Server-side validation (duplicate email/username, weak password, ...)
        setFieldErrors(e.fieldErrors as Partial<Record<keyof Form, string>>);
        setError(Object.keys(e.fieldErrors).length === 0 ? e.message : null);
      } else {
        setError('Something went wrong. Please try again.');
      }
      setSubmitting(false);
    }
  };

  return (
    <AuthScreen title="Create account" subtitle="Sign up to start managing your tasks.">
      <ErrorBanner message={error} />

      <View style={styles.row}>
        <View style={styles.half}>
          <TextField
            label="First name"
            value={form.first_name}
            onChangeText={set('first_name')}
            error={fieldErrors.first_name}
            autoComplete="given-name"
            textContentType="givenName"
          />
        </View>
        <View style={styles.half}>
          <TextField
            label="Last name"
            value={form.last_name}
            onChangeText={set('last_name')}
            error={fieldErrors.last_name}
            autoComplete="family-name"
            textContentType="familyName"
          />
        </View>
      </View>

      <TextField
        label="Username"
        value={form.username}
        onChangeText={set('username')}
        error={fieldErrors.username}
        autoCapitalize="none"
        autoCorrect={false}
        autoComplete="username-new"
        textContentType="username"
      />
      <TextField
        label="Email"
        value={form.email}
        onChangeText={set('email')}
        error={fieldErrors.email}
        placeholder="you@example.com"
        autoCapitalize="none"
        autoCorrect={false}
        autoComplete="email"
        keyboardType="email-address"
        textContentType="emailAddress"
      />
      <TextField
        label="Password"
        value={form.password}
        onChangeText={set('password')}
        error={fieldErrors.password}
        placeholder="At least 8 characters"
        secureTextEntry
        autoCapitalize="none"
        autoComplete="new-password"
        textContentType="newPassword"
        returnKeyType="go"
        onSubmitEditing={submit}
      />

      <Button title="Sign up" onPress={submit} loading={submitting} style={styles.button} />

      <View style={styles.footer}>
        <Text style={{ color: colors.textMuted }}>Already have an account? </Text>
        <Link href="/login" replace style={[styles.link, { color: colors.primary }]}>
          Log in
        </Link>
      </View>
    </AuthScreen>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: 'row', gap: spacing.md },
  half: { flex: 1 },
  button: { marginTop: spacing.sm },
  footer: { flexDirection: 'row', justifyContent: 'center', marginTop: spacing.sm },
  link: { fontWeight: '600' },
});
