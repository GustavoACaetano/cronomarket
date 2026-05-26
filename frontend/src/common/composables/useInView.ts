import { onBeforeUnmount, onMounted, ref } from 'vue'

type UseInViewOptions = {
    threshold?: number
    rootMargin?: string
    once?: boolean
}

export function useInView(options: UseInViewOptions = {}) {
    const {
        threshold = 0.2,
        rootMargin = '0px',
        once = true,
    } = options

    const targetRef = ref<HTMLElement | null>(null)
    const isVisible = ref(false)

    let observer: IntersectionObserver | null = null

    onMounted(() => {
        observer = new IntersectionObserver(
            (entries) => {
                const entry = entries[0]
                if (!entry) return

                if (entry.isIntersecting) {
                    isVisible.value = true

                    if (once) {
                        observer?.disconnect()
                        observer = null
                    }

                    return
                }

                if (!once) {
                    isVisible.value = false
                }
            },
            {
                threshold,
                rootMargin,
            }
        )

        if (targetRef.value) {
            observer.observe(targetRef.value)
        }
    })

    onBeforeUnmount(() => {
        observer?.disconnect()
        observer = null
    })

    return {
        targetRef,
        isVisible,
    }
}
