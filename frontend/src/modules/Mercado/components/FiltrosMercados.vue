<script lang="ts" setup>
import { ref } from 'vue';
import { getLocalTimeZone, today } from '@internationalized/date';
import { type FiltroSection } from '../api/types/index';

const props = defineProps<{
    filtroSection: FiltroSection
}>()

const {
    filtroSelecionado, onInput, categoriaItems
} = props.filtroSection

</script>

<template>
    <div class="grid grid-cols-6 gap-x-6">
        <UFormField label="Pesquisar" class="w-full col-span-2" :ui="{ label: 'font-light' }">
            <UInput
                placeholder="Escreva o nome de um mercado"
                color="primary"
                trailing-icon="i-lucide-search"
                class="w-full"
                size="xl"
                @input="onInput"
                v-model="filtroSelecionado.search"
            />
        </UFormField>
        <UFormField label="Encerra até" class="w-full col-span-2" :ui="{ label: 'font-light' }">
            <UInputDate v-model="filtroSelecionado.data" size="xl" :ui="{ base: 'w-full bg-muted' }">
                <template #trailing>
                    <UPopover>
                        <UButton
                            color="neutral"
                            variant="link"
                            icon="i-lucide-calendar"
                            class="px-0"
                        />

                        <template #content>
                            <UCalendar v-model="filtroSelecionado.data" />
                            <div class="border-t border-default p-2">
                                <UButton
                                    color="neutral"
                                    variant="ghost"
                                    icon="i-lucide-calendar-check"
                                    size="sm"
                                    block
                                    @click="filtroSelecionado.data = today(getLocalTimeZone())"
                                >
                                Hoje
                                </UButton>
                            </div>
                        </template>
                    </UPopover>
                </template>
            </UInputDate>
        </UFormField>
        <UFormField label="Categoria" class="w-full col-span-2" :ui="{ label: 'font-light'}">
            <USelectMenu 
                placeholder="Selecione uma categoria" 
                size="xl" 
                :items="categoriaItems"
                value-key="id"
                v-model="filtroSelecionado.categoria"
                multiple 
                :ui="{ base: 'w-full bg-muted' }"
                :search-input="{
                    placeholder: 'Categoria...',
                    icon: 'i-lucide-search'
                }"
                />
        </UFormField>
    </div>
</template>