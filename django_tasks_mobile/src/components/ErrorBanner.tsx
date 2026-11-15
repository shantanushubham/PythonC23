import { StyleSheet, Text, View } from 'react-native';

import { radius, spacing, useTheme } from '@/theme';

export function ErrorBanner({ message }: { message?: string | null }) {
  const { colors } = useTheme();
  if (!message) return null;

  return (
    <View
      accessibilityRole="alert"
      style={[styles.box, { backgroundColor: colors.dangerSurface }]}>
      <Text style={[styles.text, { color: colors.danger }]}>{message}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  box: { padding: spacing.md, borderRadius: radius.md },
  text: { fontSize: 14, fontWeight: '500' },
});
