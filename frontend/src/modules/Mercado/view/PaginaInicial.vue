<script lang="ts" setup>
import FiltrosMercados from '../components/FiltrosMercados.vue';
import ItemMercado from '../components/ItemMercado.vue';
import { usePaginaInicial } from '../composables/usePaginaInicial';

const { filtroSection, mercados } = usePaginaInicial();
</script>

<template>
    <div class="flex flex-col gap-y-6">
        <FiltrosMercados :filtro-section="filtroSection"/>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            <ItemMercado v-for="mercado in mercados" :key="mercado.id" :mercado="mercado" />
        </div>
    </div>
</template>