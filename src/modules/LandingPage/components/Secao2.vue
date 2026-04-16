<template>
    <section class="mx-auto mt-25 flex items-center justify-between px-5 max-w-7xl animate-fade-in-up" style="opacity: 0; animation-delay: 0.5s">
        <div class="flex flex-col text-wrap w-xl gap-y-6">
            <h1 class="text-5xl">Por que operar o Cronomarket?</h1>
            <p class="text-base">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
            </p>
        </div>
        <div class="grid grid-cols-2 gap-5">
            <div v-for="i in 4" :key="i" class="border-gray-300 border rounded-2xl w-70 h-40 p-5 gap-2 flex flex-col">
                <h2 class="font-bold">Mercado orientado</h2>
                <p>Lorem ipm, provident corrupti laudanticeat ill eos incidunt delectus dolore quidem?</p>
            </div>
        </div>
    </section>
</template>