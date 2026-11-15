import { Ionicons } from '@expo/vector-icons';
import { memo } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';

import { radius, spacing, useTheme } from '@/theme';
import type { Task } from '@/types';

type Props = {
  task: Task;
  isOwner: boolean;
  onPress: (task: Task) => void;
  onToggle: (task: Task) => void;
};

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString(undefined, {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
}

function ownerName(task: Task) {
  const full = `${task.user.first_name} ${task.user.last_name}`.trim();
  return full || task.user.username || task.user.email;
}

export const TaskCard = memo(function TaskCard({ task, isOwner, onPress, onToggle }: Props) {
  const { colors } = useTheme();

  return (
    <Pressable
      accessibilityRole="button"
      accessibilityLabel={`${task.title}, ${task.completed ? 'completed' : 'not completed'}`}
      onPress={() => onPress(task)}
      style={({ pressed }) => [
        styles.card,
        { backgroundColor: colors.surface, borderColor: colors.border, opacity: pressed ? 0.9 : 1 },
      ]}>
      <Pressable
        accessibilityRole="checkbox"
        accessibilityState={{ checked: task.completed, disabled: !isOwner }}
        accessibilityLabel="Mark as completed"
        disabled={!isOwner}
        hitSlop={10}
        onPress={() => onToggle(task)}>
        <Ionicons
          name={task.completed ? 'checkmark-circle' : 'ellipse-outline'}
          size={28}
          color={task.completed ? colors.success : colors.textMuted}
        />
      </Pressable>

      <View style={styles.body}>
        <Text
          numberOfLines={2}
          style={[
            styles.title,
            { color: task.completed ? colors.textMuted : colors.text },
            task.completed && styles.strike,
          ]}>
          {task.title}
        </Text>
        {task.description ? (
          <Text numberOfLines={2} style={[styles.description, { color: colors.textMuted }]}>
            {task.description}
          </Text>
        ) : null}
        <Text style={[styles.meta, { color: colors.textMuted }]}>
          {isOwner ? 'You' : ownerName(task)} · {formatDate(task.created_at)}
        </Text>
      </View>
    </Pressable>
  );
});

const styles = StyleSheet.create({
  card: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: spacing.md,
    padding: spacing.lg,
    borderRadius: radius.lg,
    borderWidth: StyleSheet.hairlineWidth,
  },
  body: { flex: 1, gap: spacing.xs },
  title: { fontSize: 16, fontWeight: '600' },
  strike: { textDecorationLine: 'line-through' },
  description: { fontSize: 14, lineHeight: 20 },
  meta: { fontSize: 12, marginTop: spacing.xs },
});
