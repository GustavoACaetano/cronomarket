<template>
    <section class="bg-gray-100 w-full flex items-center justify-center">
        <div class="py-25 flex items-center flex-col md:flex-row md:justify-between px-5 md:max-w-7xl animate-fade-in-up" style="opacity: 0; animation-delay: 0.5s">
            <div class="flex flex-col text-wrap md:w-xl gap-y-6 md:text-left text-center">
                <h1 class="text-5xl">Por que operar com o Cronomarket?</h1>
                <p class="md:text-base text-sm text-left">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                </p>
            </div>
            <div class="md:grid md:grid-cols-2 gap-5 md:mt-0 mt-10 flex flex-col">
                <div v-for="i in 4" :key="i" class="bg-white border-gray-300 border rounded-2xl md:w-70  h-40 p-5 gap-2 flex flex-col">
                    <h2 class="font-bold">Mercado orientado</h2>
                    <p>Lorem ipm, provident corrupti laudanticeat ill eos incidunt delectus dolore quidem?</p>
                </div>
            </div>
        </div>
    </section>
</template>