import { Stack } from 'expo-router';

import { TasksProvider } from '@/tasks/TasksContext';
import { useTheme } from '@/theme';

export const unstable_settings = { anchor: 'tasks' };

export default function AppLayout() {
  const { colors } = useTheme();

  return (
    <TasksProvider>
      <Stack
        screenOptions={{
          headerStyle: { backgroundColor: colors.background },
          headerTintColor: colors.text,
          headerTitleStyle: { fontWeight: '700' },
          headerShadowVisible: false,
          contentStyle: { backgroundColor: colors.background },
        }}>
        <Stack.Screen name="tasks" options={{ title: 'Tasks' }} />
        <Stack.Screen name="task/[id]" options={{ title: 'Task' }} />
        <Stack.Screen name="profile" options={{ title: 'Profile' }} />
      </Stack>
    </TasksProvider>
  );
}
