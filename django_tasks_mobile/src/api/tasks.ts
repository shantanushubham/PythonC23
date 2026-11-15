import { PAGE_SIZE } from '@/config';
import type { Paginated, Task, TaskFilter, TaskOrdering } from '@/types';

import { request } from './client';

export type ListTasksParams = {
  page: number;
  search?: string;
  filter?: TaskFilter;
  ordering?: TaskOrdering;
};

export type TaskInput = {
  title: string;
  description: string;
  completed?: boolean;
};

export const tasksApi = {
  list: ({ page, search, filter = 'all', ordering = '-created_at' }: ListTasksParams) =>
    request<Paginated<Task>>('/task/', {
      query: {
        page,
        page_size: PAGE_SIZE,
        search: search?.trim(),
        ordering,
        completed: filter === 'all' ? undefined : filter === 'completed',
      },
    }),

  get: (id: number) => request<Task>(`/task/${id}/`),

  create: (input: TaskInput) => request<Task>('/task/', { method: 'POST', body: input }),

  update: (id: number, input: Partial<TaskInput>) =>
    request<Task>(`/task/${id}/`, { method: 'PATCH', body: input }),

  remove: (id: number) => request<void>(`/task/${id}/`, { method: 'DELETE' }),
};
