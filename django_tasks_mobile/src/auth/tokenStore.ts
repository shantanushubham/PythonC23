import * as SecureStore from 'expo-secure-store';
import { Platform } from 'react-native';

import type { Tokens } from '@/types';

const KEY = 'auth.tokens';

// In-memory copy so every API call doesn't hit the keychain / keystore.
let cache: Tokens | null | undefined;

async function readRaw(): Promise<string | null> {
  if (Platform.OS === 'web') {
    try {
      return localStorage.getItem(KEY);
    } catch {
      return null;
    }
  }
  return SecureStore.getItemAsync(KEY);
}

async function writeRaw(value: string | null): Promise<void> {
  if (Platform.OS === 'web') {
    try {
      if (value === null) localStorage.removeItem(KEY);
      else localStorage.setItem(KEY, value);
    } catch {
      // storage unavailable - keep the in-memory copy only
    }
    return;
  }
  if (value === null) await SecureStore.deleteItemAsync(KEY);
  else await SecureStore.setItemAsync(KEY, value);
}

export const tokenStore = {
  async get(): Promise<Tokens | null> {
    if (cache !== undefined) return cache;
    try {
      const raw = await readRaw();
      cache = raw ? (JSON.parse(raw) as Tokens) : null;
    } catch {
      cache = null;
    }
    return cache;
  },

  async set(tokens: Tokens): Promise<void> {
    cache = tokens;
    await writeRaw(JSON.stringify(tokens));
  },

  async clear(): Promise<void> {
    cache = null;
    await writeRaw(null);
  },
};
