<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'

const valorPremio = ref(0)
const valorFinal = 300
const duracaoMs = 1800
const isVisible = ref(false)
const sectionRef = ref<HTMLElement | null>(null)

let frameId: number | null = null
let observer: IntersectionObserver | null = null
let started = false

const iniciarContagem = () => {
    if (started) return
    started = true

    const inicio = performance.now()

    const animar = (agora: number) => {
        const progresso = Math.min((agora - inicio) / duracaoMs, 1)
        valorPremio.value = Math.floor(progresso * valorFinal)

        if (progresso < 1) {
            frameId = requestAnimationFrame(animar)
            return
        }

        valorPremio.value = valorFinal
    }

    frameId = requestAnimationFrame(animar)
}

onMounted(() => {
    observer = new IntersectionObserver(
        (entries) => {
            const entry = entries[0]
            if (!entry?.isIntersecting) return

            isVisible.value = true
            iniciarContagem()
            observer?.disconnect()
            observer = null
        },
        {
            threshold: 0.35,
        }
    )

    if (sectionRef.value) {
        observer.observe(sectionRef.value)
    }
})

onBeforeUnmount(() => {
    if (frameId !== null) {
        cancelAnimationFrame(frameId)
    }

    observer?.disconnect()
    observer = null
})
</script>

<template>
    <section
        ref="sectionRef"
        class="mx-auto flex max-w-7xl flex-col items-center justify-between px-5 transition-all duration-700 ease-out"
        :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'"
    >
        <div class="mb-10 gap-y-6 transition-all duration-700 delay-150" :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0'">
            <h1 class="text-center mb-18 text-7xl font-extrabold text-transparent bg-clip-text bg-linear-to-r from-red-500 via-yellow-500 to-red-500 scale-y-125 -skew-y-6 scale-x-150 transform">
                R${{ valorPremio }}!
            </h1>
            <p class="text-center text-3xl font-bold">
                Faça seu primeiro depósito agora e iremos dobrar a quantidade depositada!
            </p>
            <p class="text-center text-xs text-gray-500 mt-2">Válido até R$300,00</p>
        </div>
        <div class="mb-24 pt-10 transition-all duration-700 delay-300" :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0'">
            <button class="mt-4 bg-black text-white px-8 py-3 rounded-full text-base font-medium hover:bg-gray-800 transition-colors cursor-pointer inline-flex items-center gap-4">
                <svg class="h-6 w-6 relative -top-0.5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                    <path d="M20 12V22H4V12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M22 7H2V12H22V7Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M12 22V7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M12 7H7.5C6.67 7 6 6.33 6 5.5C6 4.67 6.67 4 7.5 4C9.5 4 12 7 12 7Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M12 7H16.5C17.33 7 18 6.33 18 5.5C18 4.67 17.33 4 16.5 4C14.5 4 12 7 12 7Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Depositar e ganhar agora!
            </button>
            <p class="text-center text-xs text-gray-500 mt-2">sem taxa</p>
        </div>
    </section>
</template>