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
  card: {
    slots: {
      body: '!p-5',
    },
    variants: {
      variant: {
        muted: {
          root: 'bg-gray-300',
        },
      },
    },
    defaultVariants: {
      variant: 'muted',
    },
  },
  tabs: {
    slots: {
      trigger: 'cursor-pointer',
    },
    variants: {
      variant: {
        link: {
          trigger: 'text-gray-500 hover:text-black transition-colors',
          list: 'border-gray-500',
        },
      },
      color: {
        black: {
          trigger: 'text-black',
          indicator: 'bg-black',
        }
      }
    }
  },
  textarea: {
    slots: {
      base: 'bg-white text-black',
    }
  }
};