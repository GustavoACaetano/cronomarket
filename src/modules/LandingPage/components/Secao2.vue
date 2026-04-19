<script setup lang="ts">
import { useInView } from '@/common/composables/useInView'

const { targetRef, isVisible } = useInView({ threshold: 0.3 })

const titulos = [
    "Mercado orientado a eventos",
    "Aprenda enquanto participa",
    "Dados em tempo real",
    "Decisões estratégicas"
]
const textos = [
    "Opere com base em eventos reais do mundo, transformando informação em oportunidade dentro da plataforma.",
    "Mais do que entretenimento, o Cronomarket incentiva o aprendizado contínuo sobre atualidades.",
    "Acompanhe o andamento dos eventos do mercado com atualizações rápidas e precisas.",
    "Planeje suas ações com estratégia e visão, analisando cenários e aumentando seu potencial de retorno."
]
</script>

<template>
    <section class="bg-gray-100 w-full flex items-center justify-center">
        <div
            class="py-25 flex items-center flex-col md:flex-row md:justify-between px-5 md:max-w-7xl transition-all duration-700 ease-out"
            :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'"
            ref="targetRef"
        >
            <div class="flex flex-col text-wrap md:w-xl gap-y-6 md:text-left text-center">
                <h1 class="text-5xl">Por que operar com o Cronomarket?</h1>
                <p class="md:text-base text-sm text-left">
                    O melhor e mais confiável mercado de previsões do mundo!<br>
                    Entender o nosso diferencial é essencial para aproveitar ao máximo a experiência no Cronomarket. <br>
                    Esteja por dentro dos motivos para fazer suas previsões conosco.
                </p>
                <button class="mt-4 self-center bg-black text-white px-8 py-3 rounded-full text-base font-medium hover:bg-gray-800 transition-colors">Cadastre-se já!</button>
            </div>
            <div class="md:grid md:grid-cols-2 gap-5 md:mt-0 mt-10 flex flex-col">
                <div 
                    v-for="(titulo, index) in titulos" 
                    :key="index" 
                    class="bg-white border-gray-300 border rounded-2xl md:w-70 h-40 p-5 gap-2 flex flex-col"
                >
                    <h2 class="font-bold">{{ titulo }}</h2>
                    <p>{{ textos[index] }}</p>
                </div>
            </div>
        </div>
    </section>
</template>