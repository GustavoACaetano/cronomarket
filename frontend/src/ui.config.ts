import type { NuxtUIOptions } from '@nuxt/ui/unplugin';

export const uiConfig: NuxtUIOptions['ui'] = {
  colors: {
    primary: 'emerald',
    secondary: 'indigo',
    info: 'blue',
  },
  button: {
    slots: { base: 'cursor-pointer' },
    variants: {
      variant: {
        'header': 'text-gray-700 hover:text-black transition-colors',
      },
    },
    compoundVariants: [
      {
        color: 'black',
        variant: 'link',
        class: 'text-black transition-colors',
      },
      {
        color: 'black',
        variant: 'solid',
        class: 'bg-black text-white hover:bg-gray-800 transition-colors',
      },
      {
        color: 'accent',
        variant: 'link',
        class: 'text-accent-600 hover:text-accent-700 transition-colors',
      },
      {
        color: 'accent',
        variant: 'solid',
        class: 'bg-accent-500 text-black hover:bg-accent-600 transition-colors',
      }
    ],
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