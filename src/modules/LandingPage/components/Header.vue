<template>
    <nav
        class="px-6 py-4 flex items-center justify-between max-w-7xl mx-auto animate-fade-in-up"
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
            <a href="#" class="text-sm text-gray-700 hover:text-black transition-colors">Home</a>
            <a href="#" class="text-sm text-gray-700 hover:text-black transition-colors">Produtos</a>
            <a href="#" class="text-sm text-gray-700 hover:text-black transition-colors">Sobre nós</a>
            <a href="#" class="text-sm text-gray-700 hover:text-black transition-colors">Learn Hub</a>
        </div>

        <div
            class="flex items-center gap-4 animate-fade-in-up"
            style="opacity: 0; animation-delay: 0.3s"
        >
            <a href="#" class="text-sm text-gray-700 hover:text-black transition-colors">Login</a>
            <button
                class="bg-black text-white px-5 py-2.5 rounded-full text-sm font-medium hover:bg-gray-800 transition-colors"
            >
                Get started free
            </button>
        </div>
    </nav>
</template>