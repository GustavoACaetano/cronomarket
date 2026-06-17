<script setup lang="ts">
import { useRouter } from 'vue-router';
const router = useRouter();

const handleGetStarted = () => {
    const storedUser = localStorage.getItem('cronomarket_user');
    if (storedUser) {
        router.push('/mercados/home');
    } else {
        router.push('/login');
    }
};
</script>

<template>
    <section id="home" class="mx-auto text-center animate-fade-in-up" style="opacity: 0; animation-delay: 0.2s">
        <div class="flex flex-col items-center gap-2">
            <h1 class="md:text-7xl text-4xl text-black">Cronomarket</h1>
            <p class="md:text-5xl text-3xl text-transparent bg-clip-text bg-linear-to-r from-black via-gray-500 to-gray-400">onde o futuro vira mercado</p>
 
            <h2 class="md:text-6xl text-3xl mt-8 text-gray-900">O mercado perfeito para testar seus conhecimentos!</h2>
 
            <UButton color="black" class="rounded-full mt-8 cursor-pointer" size="xl" :ui="{ base: 'px-8 py-3'}" @click="handleGetStarted">
                Jogar agora!
            </UButton>
        </div>
 
        <video autoplay loop muted class="mx-auto mt-8 rounded-lg md:w-full w-3/4 md:max-w-4xl">
            <source src="/landingvideo.mp4" type="video/mp4">
            Seu navegador não suporta a tag de vídeo.
        </video>
    </section>
</template>
