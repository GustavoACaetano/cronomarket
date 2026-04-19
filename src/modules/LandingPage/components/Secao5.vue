<script setup lang="ts">
import { useInView } from '@/common/composables/useInView'

const { targetRef, isVisible } = useInView({ threshold: 0.3 })

const cards = [
	['/ryan.jpg', 'Ryan Gosling', 'Eu fiquei milionário usando o Cronomarket!'],
	['/raquel.jpeg', 'Raquel Neves', 'Estou divulgando Cronomarket para toda a Cariacica!'],
	['/profundo.jpeg', 'Profundo Marroque', 'Glub Glub']
]
</script>

<template>
	<section class="mx-auto flex flex-col items-center justify-between px-5 max-w-7xl">
        <div
            class="transition duration-700 ease-out"
            :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'"
            ref="targetRef"
        >
            <div class="gap-y-6 mb-10">
                <h1 class="text-center text-5xl mb-18">
                    Ouça os depoimentos dos <br> próprios usuários!
                </h1>
            </div>
            <div class="grid grid-cols-1 gap-10 md:grid-cols-3 mb-25">
                <div v-for="(card, i) in cards" :key="i" class="border-white bg-neutral-300 border-2 rounded-2xl max-w-70 p-8 gap-2 flex flex-col justify-between">
                    <div class="flex flex-col items-center gap-2">
                        <div class="mx-auto w-30 h-30 overflow-hidden rounded-full border-gray-600">
                            <img :src="card[0]" :alt="card[1]" class="h-full w-full object-cover">
                        </div>
                        <h2 class="font-bold text-center mb-5">{{ card[1] }}</h2>
                    </div>
                    <p class="text-center mb-5">{{ card[2] }}</p>
                    <img src="/aspas.svg" alt="Aspas" class="mx-auto mt-3 h-7 w-auto opacity-80">
                </div>
            </div>
        </div>
	</section>
</template>
