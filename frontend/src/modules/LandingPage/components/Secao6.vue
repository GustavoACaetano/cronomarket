<script setup lang="ts">
import { useInView } from '@/common/composables/useInView';
import { ref } from 'vue';
import type { TabsItem } from '@nuxt/ui'

const { targetRef, isVisible } = useInView({ threshold: 0.3 })

const items = ref<TabsItem[]>([
  {
    label: 'Passo 1',
    content: 'Acesse sua carteira e abra a aba de resgates.'
  },
  {
    label: 'Passo 2',
    content: 'Selecione o mercado finalizado com saldo disponivel.'
  },
  {
    label: 'Passo 3',
    content: 'Confirme a transferencia para sua conta em segundos.'
  }
])
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

                <UCard variant="muted" class=" max-w-4xl rounded-2xl p-6 md:p-8">
                    <div class="flex flex-col gap-6 md:flex-row ">
                        <img
                            src="/resgate.png"
                            alt="Imagem ilustrativa"
                            class="h-56 w-full rounded-xl object-cover md:h-64 md:w-2/5"
                        />
                        <UTabs :items="items" class="w-full md:w-3/5 items-center" color="black" variant="link">
                            <template #content="{ item }">
                                <div class="flex h-25 p-10">
                                    {{ item.content }}
                                </div>
                            </template>
                        </UTabs>
                    </div>
                </UCard>

                <div class="flex justify-center">
                    <UButton 
                        color="black" 
                        size="xl" 
                        class="rounded-full mt-8 animate-fade-in-up" 
                        :ui="{ base: 'px-8 py-3'}"
                        style="opacity: 0; animation-delay: 1.4s"
                    >
                        Comece a acumular ganhos agora!
                    </UButton>
                </div>
            </div>
        </div>
    </section>
</template>