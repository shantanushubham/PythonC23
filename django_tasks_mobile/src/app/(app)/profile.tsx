import { ScrollView, StyleSheet, Text, View } from 'react-native';

import { API_URL } from '@/config';
import { useAuth } from '@/auth/AuthContext';
import { Button } from '@/components/Button';
import { radius, spacing, useTheme } from '@/theme';

export default function ProfileScreen() {
  const { user, signOut } = useAuth();
  const { colors } = useTheme();

  const fullName = user ? `${user.first_name} ${user.last_name}`.trim() : '';
  const initials = user
    ? `${user.first_name[0] ?? ''}${user.last_name[0] ?? ''}`.toUpperCase() ||
      user.username[0]?.toUpperCase() ||
      '?'
    : '…';

  return (
    <ScrollView contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <View style={[styles.avatar, { backgroundColor: colors.primary }]}>
          <Text style={[styles.avatarText, { color: colors.primaryText }]}>{initials}</Text>
        </View>
        <Text style={[styles.name, { color: colors.text }]}>{fullName || user?.username || 'Loading…'}</Text>
        {user ? <Text style={{ color: colors.textMuted }}>{user.email}</Text> : null}
      </View>

      {user ? (
        <View style={[styles.card, { backgroundColor: colors.surface, borderColor: colors.border }]}>
          <Row label="Username" value={user.username} />
          <Row label="Member since" value={new Date(user.created_at).toLocaleDateString()} />
          <Row label="Server" value={API_URL} />
        </View>
      ) : null}

      <Button title="Log out" variant="danger" onPress={signOut} />
    </ScrollView>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  const { colors } = useTheme();
  return (
    <View style={styles.row}>
      <Text style={[styles.rowLabel, { color: colors.textMuted }]}>{label}</Text>
      <Text style={[styles.rowValue, { color: colors.text }]} numberOfLines={1}>
        {value}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  content: { padding: spacing.xl, gap: spacing.xl },
  header: { alignItems: 'center', gap: spacing.xs },
  avatar: {
    width: 88,
    height: 88,
    borderRadius: 44,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: spacing.sm,
  },
  avatarText: { fontSize: 32, fontWeight: '700' },
  name: { fontSize: 22, fontWeight: '700' },
  card: { borderWidth: 1, borderRadius: radius.lg, paddingHorizontal: spacing.lg },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: spacing.lg,
    paddingVertical: spacing.md,
  },
  rowLabel: { fontSize: 14 },
  rowValue: { fontSize: 14, fontWeight: '500', flexShrink: 1 },
});
