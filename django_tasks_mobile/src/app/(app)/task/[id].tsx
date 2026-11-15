import { Stack, router, useLocalSearchParams } from 'expo-router';
import { useEffect, useState } from 'react';
import {
  ActivityIndicator,
  Alert,
  KeyboardAvoidingView,
  ScrollView,
  StyleSheet,
  Switch,
  Text,
  View,
} from 'react-native';

import { ApiError } from '@/api/client';
import { tasksApi } from '@/api/tasks';
import { useAuth } from '@/auth/AuthContext';
import { Button } from '@/components/Button';
import { ErrorBanner } from '@/components/ErrorBanner';
import { TextField } from '@/components/TextField';
import { useTasksInvalidation } from '@/tasks/TasksContext';
import { spacing, useTheme } from '@/theme';
import type { Task } from '@/types';

type FieldErrors = { title?: string; description?: string };

function messageFor(e: unknown) {
  return e instanceof ApiError ? e.message : 'Something went wrong. Please try again.';
}

/** Create (`/task/new`) and edit (`/task/:id`) share this screen. */
export default function TaskFormScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const isNew = id === 'new';
  const taskId = isNew ? null : Number(id);

  const { colors } = useTheme();
  const { userId } = useAuth();
  const { invalidate } = useTasksInvalidation();

  const [task, setTask] = useState<Task | null>(null);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [completed, setCompleted] = useState(false);

  const [loading, setLoading] = useState(!isNew);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});

  // Bumped by the retry button to re-run the fetch below.
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    if (taskId === null) return;
    let cancelled = false;

    tasksApi
      .get(taskId)
      .then((data) => {
        if (cancelled) return;
        setTask(data);
        setTitle(data.title);
        setDescription(data.description);
        setCompleted(data.completed);
      })
      .catch((e) => {
        if (cancelled) return;
        setLoadError(
          e instanceof ApiError && e.status === 404 ? 'This task no longer exists.' : messageFor(e),
        );
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [taskId, attempt]);

  const retry = () => {
    setLoading(true);
    setLoadError(null);
    setAttempt((n) => n + 1);
  };

  // Tasks created by other users can be read but not changed.
  const readOnly = task !== null && task.user.id !== userId;

  const save = async () => {
    if (saving) return;
    const errors: FieldErrors = {};
    if (!title.trim()) errors.title = 'Give your task a title.';
    else if (title.trim().length > 200) errors.title = 'Titles can be up to 200 characters.';
    if (!description.trim()) errors.description = 'Add a short description.';
    setFieldErrors(errors);
    setError(null);
    if (errors.title || errors.description) return;

    setSaving(true);
    try {
      const input = { title: title.trim(), description: description.trim(), completed };
      if (taskId === null) await tasksApi.create(input);
      else await tasksApi.update(taskId, input);
      invalidate();
      router.back();
    } catch (e) {
      if (e instanceof ApiError && Object.keys(e.fieldErrors).length > 0) {
        setFieldErrors({ title: e.fieldErrors.title, description: e.fieldErrors.description });
        if (!e.fieldErrors.title && !e.fieldErrors.description) setError(e.message);
      } else {
        setError(messageFor(e));
      }
      setSaving(false);
    }
  };

  const confirmDelete = () => {
    if (taskId === null) return;
    Alert.alert('Delete task?', 'This can’t be undone.', [
      { text: 'Cancel', style: 'cancel' },
      {
        text: 'Delete',
        style: 'destructive',
        onPress: async () => {
          setDeleting(true);
          try {
            await tasksApi.remove(taskId);
            invalidate();
            router.back();
          } catch (e) {
            setDeleting(false);
            setError(messageFor(e));
          }
        },
      },
    ]);
  };

  const screenTitle = isNew ? 'New task' : readOnly ? 'Task' : 'Edit task';

  if (loading) {
    return (
      <View style={styles.center}>
        <Stack.Screen options={{ title: screenTitle }} />
        <ActivityIndicator size="large" color={colors.primary} />
      </View>
    );
  }

  if (loadError) {
    return (
      <View style={[styles.center, styles.centerPadded]}>
        <Stack.Screen options={{ title: screenTitle }} />
        <ErrorBanner message={loadError} />
        <Button title="Try again" variant="secondary" onPress={retry} />
      </View>
    );
  }

  return (
    <KeyboardAvoidingView behavior="padding" style={styles.flex}>
      <Stack.Screen options={{ title: screenTitle }} />
      <ScrollView
        contentContainerStyle={styles.content}
        keyboardShouldPersistTaps="handled"
        keyboardDismissMode="interactive">
        <ErrorBanner message={error} />

        {readOnly && task ? (
          <Text style={[styles.hint, { color: colors.textMuted }]}>
            Created by {task.user.first_name || task.user.username}. You can only edit your own tasks.
          </Text>
        ) : null}

        <TextField
          label="Title"
          value={title}
          onChangeText={setTitle}
          error={fieldErrors.title}
          placeholder="What needs to be done?"
          maxLength={200}
          editable={!readOnly}
          returnKeyType="next"
          autoFocus={isNew}
        />
        <TextField
          label="Description"
          value={description}
          onChangeText={setDescription}
          error={fieldErrors.description}
          placeholder="Add some details"
          multiline
          editable={!readOnly}
        />

        <View style={[styles.switchRow, { backgroundColor: colors.surface, borderColor: colors.border }]}>
          <Text style={[styles.switchLabel, { color: colors.text }]}>Completed</Text>
          <Switch
            value={completed}
            onValueChange={setCompleted}
            disabled={readOnly}
            trackColor={{ true: colors.primary }}
          />
        </View>

        {!readOnly ? (
          <View style={styles.actions}>
            <Button title={isNew ? 'Create task' : 'Save changes'} onPress={save} loading={saving} disabled={deleting} />
            {!isNew ? (
              <Button
                title="Delete task"
                variant="danger"
                onPress={confirmDelete}
                loading={deleting}
                disabled={saving}
              />
            ) : null}
          </View>
        ) : null}
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  center: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  centerPadded: { padding: spacing.xl, gap: spacing.lg },
  content: { padding: spacing.lg, gap: spacing.lg },
  hint: { fontSize: 14 },
  switchRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    borderWidth: 1,
    borderRadius: 12,
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
  },
  switchLabel: { fontSize: 16, fontWeight: '500' },
  actions: { gap: spacing.md, marginTop: spacing.sm },
});
