<script lang="ts" setup>
import FiltrosMercados from '../components/FiltrosMercados.vue';
import ItemMercado from '../components/ItemMercado.vue';
import { usePaginaInicial } from '../composables/usePaginaInicial';

const { filtroSection, mercados } = usePaginaInicial();
</script>

<template>
    <div class="flex flex-col gap-y-6">
        <FiltrosMercados :filtro-section="filtroSection"/>
        <div class="grid grid-cols-4 gap-x-3 gap-y-6">
            <ItemMercado class="col-span-1" v-for="mercado in mercados" :mercado="mercado" />
        </div>
    </div>
</template>