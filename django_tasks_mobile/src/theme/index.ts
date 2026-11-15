import { useColorScheme } from 'react-native';

const light = {
  background: '#F4F6FB',
  surface: '#FFFFFF',
  surfaceMuted: '#EEF1F8',
  text: '#141A2E',
  textMuted: '#6A7390',
  border: '#E1E5F0',
  primary: '#4F46E5',
  primaryText: '#FFFFFF',
  success: '#16A34A',
  danger: '#DC2626',
  dangerSurface: '#FDECEC',
  placeholder: '#9AA2BC',
};

const dark: typeof light = {
  background: '#0D1020',
  surface: '#171B31',
  surfaceMuted: '#20253F',
  text: '#F1F3FB',
  textMuted: '#98A0BF',
  border: '#2A3050',
  primary: '#7C7AF2',
  primaryText: '#0D1020',
  success: '#4ADE80',
  danger: '#F87171',
  dangerSurface: '#3A1D24',
  placeholder: '#6A7390',
};

export type Colors = typeof light;

export function useTheme() {
  const scheme = useColorScheme();
  return { colors: scheme === 'dark' ? dark : light, isDark: scheme === 'dark' };
}

export const spacing = { xs: 4, sm: 8, md: 12, lg: 16, xl: 24, xxl: 32 };
export const radius = { sm: 8, md: 12, lg: 16, pill: 999 };
