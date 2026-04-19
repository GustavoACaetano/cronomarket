<template>
    <div class="w-full bg-white text-black pb-12">
        <nav
            class="px-6 py-4 flex items-center justify-between max-w-7xl mx-auto animate-fade-in-up "
            style="opacity: 0; animation-delay: 0.1s"
        >
            <a href="#" class="flex items-center gap-2">
                <Star class="w-5 h-5 fill-black" />
                <span class="text-lg font-semibold">Cronomarket</span>
            </a>

            <div
                class="hidden md:flex items-center gap-8 animate-fade-in-up"
                style="opacity: 0; animation-delay: 0.2s"
            >
                <a href="#home" class="text-sm text-gray-700 hover:text-black transition-colors">Home</a>
                <a href="#por-que" class="text-sm text-gray-700 hover:text-black transition-colors">Por que?</a>
                <a href="#sobre" class="text-sm text-gray-700 hover:text-black transition-colors">Sobre nós</a>
                <a href="#como-operar" class="text-sm text-gray-700 hover:text-black transition-colors">Como operar?</a>
                <a href="#depoimentos" class="text-sm text-gray-700 hover:text-black transition-colors">Depoimentos</a>
                <a href="#resgate" class="text-sm text-gray-700 hover:text-black transition-colors">Resgate</a>
                <a href="#faq" class="text-sm text-gray-700 hover:text-black transition-colors">FAQ</a>
            </div>

            <div
                class="flex items-center gap-2 animate-fade-in-up md:gap-4"
                style="opacity: 0; animation-delay: 0.3s"
            >
                <a href="#" class="text-sm text-gray-700 hover:text-black transition-colors">Entrar</a>
                <button
                    class="bg-black text-white px-5 py-2.5 rounded-full text-sm font-medium hover:bg-gray-800 transition-colors"
                >
                    Inscrever-se
                </button>
            </div>
        </nav>
    </div>
</template>