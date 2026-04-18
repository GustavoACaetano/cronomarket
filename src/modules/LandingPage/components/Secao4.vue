<script setup lang="ts">
import { ChevronLeft, ChevronRight } from 'lucide-vue-next'
import { ref } from 'vue'

const imagens = [
    '/carrossel1.png',
    '/carrossel2.png',
    '/carrossel1.png',
    '/carrossel1.png',
    '/carrossel1.png'
]

const imagensAlt = [
    'Escolher mercado',
    'Analisar mercado',
    'Fazer previsão',
    'Comprar ações',
    'Acompanhar resultado'
]

const titulos = [
    "1. Escolha um mercado",
    "2. Analise as probabilidades",
    "3. Faça sua previsão",
    "4. Compre ações",
    "5. Acompanhe e finalize"
]

const textos = [
    "Explore os mercados disponíveis e escolha um tema que você entende ou tem interesse. Pode ser esportes, política, tecnologia ou eventos do dia a dia.",

    "Antes de apostar, observe as probabilidades e o comportamento do mercado. Veja o que outros usuários estão fazendo e identifique boas oportunidades.",

    "Escolha o resultado que você acredita que vai acontecer. Cada mercado possui diferentes possibilidades, e você decide em qual delas confiar.",

    "Invista comprando ações no resultado escolhido. Quanto mais cedo e estratégico você for, maior pode ser o seu retorno.",

    "Acompanhe o andamento do mercado em tempo real. Ao final do evento, suas ações serão liquidadas com base no resultado final."
]

const currentIndex = ref(0)
const direction = ref('right')

function avancarCarrossel() {
    direction.value = 'right'
    currentIndex.value = (currentIndex.value + 1) % titulos.length
}

function voltarCarrossel() {
    direction.value = 'left'
    currentIndex.value = (currentIndex.value - 1 + titulos.length) % titulos.length
}
</script>

<template>
    <section class="px-6 py-10 mx-auto max-w-7xl">
        <h2 class="text-4xl md:text-5xl leading-tight tracking-tight mb-15 text-center">
            Como operar no Cronomarket?
        </h2>

        <div class="flex items-center justify-center gap-8">
            <div class="cursor-pointer">
                <ChevronLeft @click="voltarCarrossel"/>
            </div>

            <transition :name="direction === 'right' ? 'slide-right' : 'slide-left'" mode="out-in">
                <div :key="currentIndex" class="flex md:flex-row flex-col p-10 bg-gray-100 rounded gap-8 items-center h-8xl">
                    <img
                        :src="imagens[currentIndex]"
                        :alt="imagensAlt[currentIndex]"
                        class="md:w-1/2 md:h-75 object-cover rounded-lg"
                    />

                    <div class="md:w-1/2">
                        <p class="mb-6 text-2xl font-semibold">
                            {{ titulos[currentIndex] }}
                        </p>

                        <p class="text-gray-700 leading-relaxed">
                            {{ textos[currentIndex] }}
                        </p>
                    </div>
                </div>
            </transition>

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

<style>
.slide-right-enter-active,
.slide-right-leave-active {
  transition: all 0.4s ease;
}

.slide-right-enter-from {
  opacity: 0;
  transform: translateX(60px);
}

.slide-right-leave-to {
  opacity: 0;
  transform: translateX(-60px);
}

.slide-left-enter-active,
.slide-left-leave-active {
  transition: all 0.4s ease;
}

.slide-left-enter-from {
  opacity: 0;
  transform: translateX(-60px);
}

.slide-left-leave-to {
  opacity: 0;
  transform: translateX(60px);
}
</style>