<script setup lang="ts">
import { useInView } from '@/common/composables/useInView'

const { targetRef, isVisible } = useInView({ threshold: 0.2 })

const descricao = 'Onde o futuro vira mercado!'

const linksPrincipais = [
    { label: '[HOME]', href: '#' },
    { label: '[PRODUTOS]', href: '#' },
    { label: '[SOBRE_NOS]', href: '#' },
    { label: '[LEARN_HUB]', href: '#' },
]

const suporte = [
    { label: 'atendimento@cronomarket.com', href: '#' },
    { label: '(27) 99751-1902', href: '#' },
    { label: 'Atendimento 24 horas', href: '#' },
]

const legal = [
    { label: 'Termos de uso', href: '#' },
    { label: 'Política de privacidade', href: '#' },
    { label: 'Jogo responsável', href: '#' },
]

const redesSociais = [
    { label: 'Instagram', href: '#', icon: '/instagram.png' },
    { label: 'LinkedIn', href: '#', icon: '/linkedin.png' },
    // { label: 'Twitter', href: '#', icon: '/twitter.png' },
]
</script>

<template>
    <footer class="w-full border-t border-white/10 bg-black text-white">
        <div ref="targetRef" class="mx-auto max-w-7xl px-5 py-12 transition-all duration-700 ease-out md:py-16"
            :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'">
            <div class="grid grid-cols-1 gap-10 md:grid-cols-4">
                <div class="flex flex-col items-center text-center md:items-start md:text-left">
                    <a href="#" class="mb-5 flex w-full items-center justify-center gap-3 md:justify-start">
                        <img src="/logo.png" alt="Logo Cronomarket" class="h-10 w-10 rounded-lg bg-white object-cover">
                        <span class="text-xl font-semibold">Cronomarket</span>
                    </a>

                    <p class="max-w-sm text-sm leading-relaxed text-gray-400">
                        {{ descricao }}
                    </p>
                </div>

                <div>
                    <h2 class="mb-4 text-sm font-semibold uppercase text-white">Navegação</h2>

                    <nav class="flex flex-col gap-3">
                        <a v-for="link in linksPrincipais" :key="link.label" :href="link.href"
                            class="text-sm text-gray-400 transition-colors hover:text-white">
                            {{ link.label }}
                        </a>
                    </nav>
                </div>

                <div>
                    <h2 class="mb-4 text-sm font-semibold uppercase text-white">Suporte</h2>

                    <div class="flex flex-col gap-3">
                        <a v-for="item in suporte" :key="item.label" :href="item.href"
                            class="text-sm text-gray-400 transition-colors hover:text-white">
                            {{ item.label }}
                        </a>
                    </div>
                </div>

                <div>
                    <h2 class="mb-4 text-sm font-semibold uppercase text-white">Legal</h2>

                    <div class="flex flex-col gap-3">
                        <a v-for="item in legal" :key="item.label" :href="item.href"
                            class="text-sm text-gray-400 transition-colors hover:text-white">
                            {{ item.label }}
                        </a>
                    </div>

                    <div class="mt-6 flex flex-wrap gap-x-4 gap-y-2">

                        <a v-for="rede in redesSociais" :key="rede.label" :href="rede.href"
                            class="flex items-center gap-2 text-sm text-gray-400 transition-colors hover:text-white">
                            <img :src="rede.icon" :alt="rede.label" class="h-5 w-5 rounded p-0.5 object-contain"
                                :class="{ 'bg-white': rede.label === 'Twitter' }">
                            {{ rede.label }}
                        </a>
                    </div>
                </div>
            </div>

            <div class="mt-10 border-t border-white/10 pt-6">
                <p class="text-sm text-gray-500">
                    © 2026 Cronomarket. Todos os direitos reservados.
                </p>
            </div>
        </div>
    </footer>
</template>
