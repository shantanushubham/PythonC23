import { createContext, use, useCallback, useMemo, useState, type PropsWithChildren } from 'react';

type TasksContextValue = {
  /** Bumped whenever a task is created / edited / deleted on another screen. */
  version: number;
  invalidate: () => void;
};

const TasksContext = createContext<TasksContextValue | null>(null);

export function useTasksInvalidation() {
  const value = use(TasksContext);
  if (!value) throw new Error('useTasksInvalidation must be used inside <TasksProvider>');
  return value;
}

export function TasksProvider({ children }: PropsWithChildren) {
  const [version, setVersion] = useState(0);
  const invalidate = useCallback(() => setVersion((v) => v + 1), []);
  const value = useMemo(() => ({ version, invalidate }), [version, invalidate]);
  return <TasksContext value={value}>{children}</TasksContext>;
}
