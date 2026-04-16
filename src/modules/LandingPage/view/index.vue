<script lang="ts" setup>
import { ChevronDown, Star } from 'lucide-vue-next'
import Header from '../components/Header.vue';
import Secao1 from '../components/Secao1.vue';
import Secao2 from '../components/Secao2.vue';
import Secao3 from '../components/Secao3.vue';
</script>

<template>
    <div class="min-h-screen bg-white text-black">
        <Header />
        
        <Secao1 />

        <Secao2 />

        <Secao3 />
    </div>
</template>