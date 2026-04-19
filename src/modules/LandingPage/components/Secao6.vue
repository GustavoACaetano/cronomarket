<script setup lang="ts">
import { useInView } from '@/common/composables/useInView';

const { targetRef, isVisible } = useInView({ threshold: 0.3 })
</script>

<template>
    <section class="bg-gray-100 w-full flex items-center justify-center" id="resgate">
        <div 
            class="mx-auto py-24 flex flex-col items-center justify-between px-5 max-w-7xl transition-all duration-700 ease-out" 
            :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'"
            ref="targetRef"
        >
            <div class="gap-y-6 mb-10">
                <h2 class="text-center text-5xl mb-18">
                    Como resgatar seus ganhos?
                </h2>            

                <div class="mx-auto w-full max-w-4xl rounded-2xl bg-gray-300 p-6 md:p-8">
                    <div class="flex flex-col gap-6 md:flex-row ">
                        <img
                            src="/resgate.png"
                            alt="Imagem ilustrativa"
                            class="h-56 w-full rounded-xl object-cover md:h-64 md:w-2/5"
                        />

                        <div class="tabs tabs-border w-full md:w-3/5  [--tab-border-color:black] ">
                            <input type="radio" name="my_tabs_2" class="tab text-black " aria-label="Passo 1" :checked="true" />
                            <div class="tab-content p-10 h-25 ">Acesse sua carteira e abra a aba de resgates.</div>

                            <input type="radio" name="my_tabs_2" class="tab text-black " aria-label="Passo 2"  />
                            <div class="tab-content p-10 h-25">Selecione o mercado finalizado com saldo disponivel.</div>

                            <input type="radio" name="my_tabs_2" class="tab text-black " aria-label="Passo 3" />
                            <div class="tab-content p-10 h-25">Confirme a transferencia para sua conta em segundos.</div>
                        </div>
                    </div>
                </div>

                <div class="flex justify-center">
                    <button
                        class="mt-8 bg-black text-white px-8 py-3 rounded-full text-base font-medium hover:bg-gray-800 transition-colors animate-fade-in-up"
                        style="opacity: 0; animation-delay: 1.4s"
                    >
                        Comece a acumular ganhos agora!
                    </button>
                </div>
            </div>
        </div>
    </section>
</template>