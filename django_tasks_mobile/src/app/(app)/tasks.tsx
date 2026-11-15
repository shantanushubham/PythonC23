import { Ionicons } from '@expo/vector-icons';
import { Stack, router } from 'expo-router';
import { useCallback, useEffect, useRef, useState } from 'react';
import {
  ActivityIndicator,
  Alert,
  FlatList,
  Pressable,
  RefreshControl,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { tasksApi } from '@/api/tasks';
import { ApiError } from '@/api/client';
import { useAuth } from '@/auth/AuthContext';
import { Button } from '@/components/Button';
import { EmptyState } from '@/components/EmptyState';
import { ErrorBanner } from '@/components/ErrorBanner';
import { TaskCard } from '@/components/TaskCard';
import { useDebouncedValue } from '@/hooks/useDebouncedValue';
import { useTasksInvalidation } from '@/tasks/TasksContext';
import { radius, spacing, useTheme } from '@/theme';
import type { Task, TaskFilter, TaskOrdering } from '@/types';

const FILTERS: { key: TaskFilter; label: string }[] = [
  { key: 'all', label: 'All' },
  { key: 'active', label: 'Active' },
  { key: 'completed', label: 'Done' },
];

function messageFor(e: unknown) {
  return e instanceof ApiError ? e.message : 'Something went wrong. Please try again.';
}

export default function TasksScreen() {
  const { colors } = useTheme();
  const { userId } = useAuth();
  const { version } = useTasksInvalidation();
  const insets = useSafeAreaInsets();

  const [query, setQuery] = useState('');
  const search = useDebouncedValue(query);
  const [filter, setFilter] = useState<TaskFilter>('all');
  const [ordering, setOrdering] = useState<TaskOrdering>('-created_at');

  const [tasks, setTasks] = useState<Task[]>([]);
  const [page, setPage] = useState(1);
  const [hasNext, setHasNext] = useState(false);
  const [total, setTotal] = useState(0);
  // Key of the search/filter/ordering the current `tasks` were loaded for. While it differs from
  // the key of the current inputs we're (re)loading, which is shown as a spinner.
  const [loadedKey, setLoadedKey] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const paramsKey = `${search}|${filter}|${ordering}`;
  const loading = loadedKey !== paramsKey;

  // Bumped by pull-to-refresh / retry to force a reload of page 1.
  const [reloadToken, setReloadToken] = useState(0);
  // Incremented whenever page 1 is reloaded so that a slow "load more" can't append stale rows.
  const generation = useRef(0);

  // Load page 1 when the search/filter/ordering change (spinner, see `loading`), on refresh, or when
  // a task was changed on another screen (`version`; silent, so the list doesn't flash).
  useEffect(() => {
    let cancelled = false;
    generation.current += 1;

    tasksApi
      .list({ page: 1, search, filter, ordering })
      .then((data) => {
        if (cancelled) return;
        setTasks(data.results);
        setPage(1);
        setHasNext(data.next !== null);
        setTotal(data.count);
        setError(null);
      })
      .catch((e) => {
        if (!cancelled) setError(messageFor(e));
      })
      .finally(() => {
        if (cancelled) return;
        setLoadedKey(paramsKey);
        setRefreshing(false);
      });

    return () => {
      cancelled = true;
    };
  }, [search, filter, ordering, paramsKey, version, reloadToken]);

  const onRefresh = () => {
    setRefreshing(true);
    setReloadToken((n) => n + 1);
  };

  const retry = () => {
    setLoadedKey(null);
    setReloadToken((n) => n + 1);
  };

  const onEndReached = async () => {
    if (!hasNext || loading || refreshing || loadingMore || error) return;
    const gen = generation.current;
    setLoadingMore(true);
    try {
      const data = await tasksApi.list({ page: page + 1, search, filter, ordering });
      if (gen !== generation.current) return;
      setTasks((prev) => {
        const seen = new Set(prev.map((t) => t.id));
        return [...prev, ...data.results.filter((t) => !seen.has(t.id))];
      });
      setPage(page + 1);
      setHasNext(data.next !== null);
    } catch (e) {
      if (gen === generation.current) setError(messageFor(e));
    } finally {
      setLoadingMore(false);
    }
  };

  const toggle = useCallback(
    async (task: Task) => {
      const completed = !task.completed;
      const previous = tasks;
      // Optimistic update; when a status filter is active the task no longer belongs in the list.
      setTasks((prev) =>
        filter === 'all'
          ? prev.map((t) => (t.id === task.id ? { ...t, completed } : t))
          : prev.filter((t) => t.id !== task.id),
      );
      try {
        await tasksApi.update(task.id, { completed });
        if (filter !== 'all') setTotal((n) => Math.max(0, n - 1));
      } catch (e) {
        setTasks(previous);
        Alert.alert('Could not update task', messageFor(e));
      }
    },
    [tasks, filter],
  );

  const openTask = useCallback((task: Task) => {
    router.push({ pathname: '/task/[id]', params: { id: String(task.id) } });
  }, []);

  const isFiltering = search.trim() !== '' || filter !== 'all';

  return (
    <View style={styles.flex}>
      <Stack.Screen
        options={{
          headerRight: () => (
            <Pressable
              accessibilityRole="button"
              accessibilityLabel="Profile"
              hitSlop={12}
              onPress={() => router.push('/profile')}>
              <Ionicons name="person-circle-outline" size={28} color={colors.text} />
            </Pressable>
          ),
        }}
      />

      <View style={styles.controls}>
        <View style={[styles.search, { backgroundColor: colors.surface, borderColor: colors.border }]}>
          <Ionicons name="search" size={18} color={colors.textMuted} />
          <TextInput
            accessibilityLabel="Search tasks"
            value={query}
            onChangeText={setQuery}
            placeholder="Search tasks"
            placeholderTextColor={colors.placeholder}
            returnKeyType="search"
            autoCorrect={false}
            style={[styles.searchInput, { color: colors.text }]}
          />
          {query ? (
            <Pressable accessibilityLabel="Clear search" hitSlop={10} onPress={() => setQuery('')}>
              <Ionicons name="close-circle" size={18} color={colors.textMuted} />
            </Pressable>
          ) : null}
        </View>

        <View style={styles.chipRow}>
          {FILTERS.map(({ key, label }) => {
            const selected = filter === key;
            return (
              <Pressable
                key={key}
                accessibilityRole="button"
                accessibilityState={{ selected }}
                onPress={() => setFilter(key)}
                style={[
                  styles.chip,
                  { backgroundColor: selected ? colors.primary : colors.surfaceMuted },
                ]}>
                <Text
                  style={[
                    styles.chipText,
                    { color: selected ? colors.primaryText : colors.textMuted },
                  ]}>
                  {label}
                </Text>
              </Pressable>
            );
          })}
          <View style={styles.flex} />
          <Pressable
            accessibilityRole="button"
            accessibilityLabel={ordering === '-created_at' ? 'Sorted newest first' : 'Sorted oldest first'}
            onPress={() => setOrdering((o) => (o === '-created_at' ? 'created_at' : '-created_at'))}
            style={[styles.chip, styles.sortChip, { backgroundColor: colors.surfaceMuted }]}>
            <Ionicons
              name={ordering === '-created_at' ? 'arrow-down' : 'arrow-up'}
              size={14}
              color={colors.textMuted}
            />
            <Text style={[styles.chipText, { color: colors.textMuted }]}>
              {ordering === '-created_at' ? 'Newest' : 'Oldest'}
            </Text>
          </Pressable>
        </View>
      </View>

      {loading ? (
        <View style={styles.center}>
          <ActivityIndicator size="large" color={colors.primary} />
        </View>
      ) : (
        <FlatList
          data={tasks}
          keyExtractor={(task) => String(task.id)}
          renderItem={({ item }) => (
            <TaskCard task={item} isOwner={item.user.id === userId} onPress={openTask} onToggle={toggle} />
          )}
          contentContainerStyle={[styles.list, { paddingBottom: insets.bottom + 96 }]}
          ItemSeparatorComponent={Separator}
          keyboardShouldPersistTaps="handled"
          keyboardDismissMode="on-drag"
          onEndReached={onEndReached}
          onEndReachedThreshold={0.4}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={colors.primary} />
          }
          ListHeaderComponent={
            error ? (
              <View style={styles.errorBox}>
                <ErrorBanner message={error} />
                <Button
                  title="Try again"
                  variant="secondary"
                  onPress={retry}
                />
              </View>
            ) : tasks.length > 0 ? (
              <Text style={[styles.count, { color: colors.textMuted }]}>
                {total} {total === 1 ? 'task' : 'tasks'}
              </Text>
            ) : undefined
          }
          ListEmptyComponent={
            error ? undefined : isFiltering ? (
              <EmptyState icon="search" title="No matching tasks" subtitle="Try a different search or filter." />
            ) : (
              <EmptyState
                icon="checkmark-done-circle-outline"
                title="No tasks yet"
                subtitle="Tap the + button to add your first task."
              />
            )
          }
          ListFooterComponent={
            loadingMore ? <ActivityIndicator style={styles.footer} color={colors.primary} /> : undefined
          }
        />
      )}

      <Pressable
        accessibilityRole="button"
        accessibilityLabel="New task"
        onPress={() => router.push({ pathname: '/task/[id]', params: { id: 'new' } })}
        style={({ pressed }) => [
          styles.fab,
          {
            backgroundColor: colors.primary,
            bottom: insets.bottom + spacing.xl,
            opacity: pressed ? 0.85 : 1,
          },
        ]}>
        <Ionicons name="add" size={30} color={colors.primaryText} />
      </Pressable>
    </View>
  );
}

function Separator() {
  return <View style={{ height: spacing.md }} />;
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  center: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  controls: { paddingHorizontal: spacing.lg, paddingBottom: spacing.md, gap: spacing.md },
  search: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    borderWidth: 1,
    borderRadius: radius.md,
    paddingHorizontal: spacing.md,
    minHeight: 46,
  },
  searchInput: { flex: 1, fontSize: 16, paddingVertical: spacing.sm },
  chipRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  chip: { paddingHorizontal: spacing.lg, paddingVertical: spacing.sm, borderRadius: radius.pill },
  sortChip: { flexDirection: 'row', alignItems: 'center', gap: spacing.xs },
  chipText: { fontSize: 14, fontWeight: '600' },
  list: { paddingHorizontal: spacing.lg, flexGrow: 1 },
  count: { fontSize: 13, fontWeight: '600', marginBottom: spacing.md },
  errorBox: { gap: spacing.md, marginBottom: spacing.md },
  footer: { paddingVertical: spacing.lg },
  fab: {
    position: 'absolute',
    right: spacing.xl,
    width: 60,
    height: 60,
    borderRadius: 30,
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 6,
    shadowColor: '#000',
    shadowOpacity: 0.25,
    shadowRadius: 8,
    shadowOffset: { width: 0, height: 4 },
  },
});
