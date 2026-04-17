<script setup lang="ts">
import { ChevronLeft, ChevronRight } from 'lucide-vue-next'
import { ref } from 'vue'

const imagens = [
    '/carrossel1.png',
    '/carrossel2.png'
]
const imagensAlt = [
    'Ryan Gosling',
    'Raquel Neves'
]
const titulos = [
    "1. Escolha um mercado",
    "2. Faça suas previsões"
]
const textos = [
    "Dentre as milhares de opções, encontre um mercado que você possui conhecimento ou interesse. Pode ser sobre esportes, política, entretenimento, ciência e muito mais!",
    "Faça suas previsões escolhendo um dos lados do mercado. Você pode comprar ações de um resultado específico, como 'Time A vence' ou 'Evento X acontece'."
]

const currentIndex = ref(0)

function avancarCarrossel() {
    currentIndex.value = (currentIndex.value + 1) % titulos.length
}

function voltarCarrossel() {
    currentIndex.value = (currentIndex.value - 1 + titulos.length) % titulos.length
}
</script>

<template>
    <section class="p-6 mx-auto max-w-7xl">
        <h2 class="text-4xl md:text-5xl leading-tight tracking-tight mb-15 text-center">
            Como operar no Cronomarket?
        </h2>

        <div class="flex items-center justify-center gap-8">
            <div class="cursor-pointer">
                <ChevronLeft @click="voltarCarrossel"/>
            </div>

            <div class="flex p-10 bg-gray-100 rounded gap-8 items-center">
                <img
                    :src="imagens[currentIndex]"
                    :alt="imagensAlt[currentIndex]"
                    class="w-1/2 h-[300px] object-cover rounded-lg"
                />

                <div class="w-1/2">
                    <p class="mb-6 text-2xl font-semibold">
                        {{ titulos[currentIndex] }}
                    </p>

                    <p class="text-gray-700 leading-relaxed">
                        {{ textos[currentIndex] }}
                    </p>
                </div>
            </div>

            <div class="cursor-pointer">
                <ChevronRight @click="avancarCarrossel"/>
            </div>
        </div>

        <div class="flex items-center justify-center gap-4 mt-15">
            <p>Entendeu?</p>
            <button
                class="bg-black text-white px-8 py-3 rounded-full text-base font-medium hover:bg-gray-800 transition-colors"
            >
                Começar agora!
            </button>
        </div>
    </section>
</template>