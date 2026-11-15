import type { Tokens, User } from '@/types';

import { request } from './client';

export type RegisterInput = {
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  password: string;
};

export const authApi = {
  login: (email: string, password: string) =>
    request<Tokens>('/login/', { method: 'POST', body: { email, password }, auth: false }),

  register: (input: RegisterInput) =>
    request<User>('/user/', { method: 'POST', body: input, auth: false }),

  getUser: (id: number) => request<User>(`/user/${id}/`),
};
