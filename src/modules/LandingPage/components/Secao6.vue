<script setup lang="ts">
import { useInView } from '@/common/composables/useInView';

const { targetRef, isVisible } = useInView({ threshold: 0.3 })
</script>

<template>
    <section class="bg-gray-100 w-full flex items-center justify-center">
        <div 
        class="mx-auto py-24 flex flex-col items-center justify-between px-5 max-w-7xl transition-all duration-700 ease-out" 
        :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'"
        ref="targetRef"
        >
            <div class="gap-y-6 mb-10">
                <h1 class="text-center text-5xl mb-18">
                    Como resgatar seus ganhos?
                </h1>            

                <div class="mx-auto w-full max-w-4xl rounded-2xl bg-gray-300 p-6 md:p-8">
                    <div class="flex flex-col gap-6 md:flex-row md:items-center">
                        <img
                            src="/img1.png"
                            alt="Imagem ilustrativa"
                            class="h-56 w-full rounded-xl object-cover md:h-64 md:w-2/5"
                        />

                        <div class="md:w-3/5">
                            <h2 class="mb-4 text-2xl font-semibold md:text-3xl">Resgate em poucos passos</h2>

                            <ul class="list-disc space-y-2 pl-5 text-base leading-relaxed">
                                <li>Acesse sua carteira e abra a aba de resgates.</li>
                                <li>Selecione o mercado finalizado com saldo disponivel.</li>
                                <li>Confirme a transferencia para sua conta em segundos.</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>