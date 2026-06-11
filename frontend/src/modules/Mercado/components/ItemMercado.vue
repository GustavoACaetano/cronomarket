<script lang="ts" setup>
import type { Mercado } from '../api/types/index';

const props = defineProps<{
    mercado: Mercado
}>()
</script>

<template>
    <UCard class="h-52 cursor-pointer" variant="subtle" :ui="{ body: 'h-full', root: 'rounded-2xl'}">
        <div class="flex flex-col gap-y-5 justify-between h-full">
            <span class="line-clamp-2">{{ mercado.titulo }}</span>
            <div class="grid grid-cols-2 items-center gap-x-2">
                <img :src="mercado.link_imagem" alt="" class="col-span-1">
                <!-- <div class="flex items-center gap-x-4 col-span-1 ml-14 mb-4">
                    <div class="flex flex-col text-success items-center">
                        <UButton 
                            color="success"
                            :label="mercado.opcao_sucesso"
                            size="lg"
                        />
                        <span>45%</span>
                    </div>
                    <USeparator icon="i-lucide-x" orientation="vertical" size="md"/>
                    <div class="flex flex-col text-error items-center">
                        <UButton 
                            color="error"
                            :label="mercado.opcao_fracasso"
                            size="lg"
                        />
                        <span>55%</span>
                    </div>
                </div> -->
                <div class="flex items-center gap-x-4 col-span-1 ">
                    <div class="flex flex-col text-success items-center">
                        <UButton 
                            color="success"
                            size="lg"
                            :ui="{ base: 'px-6'}"
                        >
                            <template #default>
                                <div class="flex flex-col text-white items-center">
                                    <span>{{ mercado.opcao_sucesso }}</span>
                                    <span>45%</span>
                                </div>
                            </template>
                        </UButton>
                    </div>
                    <USeparator icon="i-lucide-x" orientation="vertical" size="md"/>
                    <div class="flex flex-col text-error items-center">
                        <UButton 
                            color="error"
                            size="lg"
                            :ui="{ base: 'px-6'}"
                        >
                            <template #default>
                                <div class="flex flex-col text-white items-center">
                                    <span>{{ mercado.opcao_fracasso }}</span>
                                    <span>55%</span>
                                </div>
                            </template>
                        </UButton>
                    </div>
                </div>
            </div>
        </div>
    </UCard>
</template>