import type { NuxtUIOptions } from '@nuxt/ui/unplugin';

export const uiConfig: NuxtUIOptions['ui'] = {
  colors: {
    primary: 'cyan',
    secondary: 'slate',
    info: 'blue',
  },
  toast: {
    variants: {
      color: {
        success: {
          root: 'bg-green-100 dark:bg-green-800',
        },
        error: {
          root: 'bg-red-100 dark:bg-red-800',
        },
      },
    },
    defaultVariants: {
      color: 'primary',
    },
  },

  card: {
    slots: {
      body: '!p-5',
    },
    variants: {
      variant: {
        muted: {
          root: 'bg-muted',
        },
        subtle: {
          root: 'bg-primary/[5%] ring ring-primary/15',
        },

        subtleSecondary: {
          root: 'bg-primary/[3%] ring ring-primary/15',
        },

        subtleBorder: {
          root: 'bg-primary/[3%] dark:bg-elevated/50 border border-primary/20 border-l-4 border-l-primary',
        },
        solid: {
          root: 'bg-white dark:bg-secondary-800 ring ring-secondary-200 dark:ring-white/15',
        },
        outline: {
          root: 'bg-transparent ring-secondary-200 dark:ring-secondary-700',
        },
      },
    },
    defaultVariants: {
      variant: 'muted',
    },
  },

  button: {
    slots: { base: 'cursor-pointer' },
    variants: {
      variant: {
        'sidebar-item': {
          base: 'py-3 w-full gap-3 font-normal dark:text-white hover:bg-primary-500/10 justify-start',
        },
        'sidebar-item-collapsed': {
          base: 'py-3 w-full font-normal dark:text-white hover:bg-primary-500/10 justify-center px-0',
          leadingIcon: 'mx-auto',
        },
        'action-icon': {
          base: 'rounded-full',
        },
      },
    },
  },
  input: {
    slots: { root: 'w-full' },
    variants: {
      size: {
        md: 'px-4 py-2',
      },
      variant: {
        subtle: 'bg-white dark:bg-secondary-800',
        disabled: 'bg-secondary-100 outline-1 outline-secondary-300 text-[--color-text-muted] dark:bg-secondary-700 dark:outline-secondary-800',
      },
    },
    defaultVariants: {
      color: 'neutral',
      variant: 'subtle',
    },
  },
  textarea: {
    slots: { root: 'w-full' },
    variants: {
      size: {
        md: 'px-4 py-2',
      },
      variant: {
        subtle: 'bg-white dark:bg-secondary-800',
      },
    },
    defaultVariants: {
      color: 'neutral',
      variant: 'subtle',
    },
  },
  inputDate: {
    slots: { trailing: 'pr-4' },
    variants: {
      size: {
        md: 'pl-4 py-2',
      },
      variant: {
        subtle: 'bg-white dark:bg-secondary-800',
      },
    },
    defaultVariants: {
      color: 'neutral',
      variant: 'subtle',
    },
  },
  select: {
    variants: {
      size: {
        md: 'px-4 py-2',
      },
      variant: {
        subtle: 'bg-white dark:bg-secondary-800',
        disabled: 'bg-secondary-100 outline-1 outline-secondary-300 text-[var(--color-text-muted)] dark:bg-secondary-700 dark:outline-secondary-800',
      },
    },
    defaultVariants: {
      color: 'neutral',
      variant: 'subtle',
    },
  },

  formField: {
    variants: {
      required: {
        true: {
          label: 'after:text-default',
        },
      },
    },
  },

  modal: {
    variants: {
      size: {
        details: {
          content:
            'w-[calc(100vw-2rem)] max-w-xl max-h-[90vh] rounded-xl shadow-xl ring ring-default bg-elevated flex flex-col',
        },
      },
    },
  },
};