import type { NuxtUIOptions } from '@nuxt/ui/unplugin';

export const uiConfig: NuxtUIOptions['ui'] = {
  colors: {
    primary: 'emerald',
    secondary: 'slate',
    info: 'blue',
  },
  button: {
    slots: { base: 'cursor-pointer' },
    variants: {
      color: {
        black: 'bg-black text-white hover:bg-gray-800 transition-colors',
      },
      variant: {
        'header': 'text-gray-700 hover:text-black transition-colors',
      }
    },
  },
};