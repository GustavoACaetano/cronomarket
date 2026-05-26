<script setup lang="ts">
import { useInView } from '@/common/composables/useInView'

const { targetRef, isVisible } = useInView({ threshold: 0.3 })
</script>

<template>
    <section 
    id = "sobre"
    class="px-6 max-w-7xl mx-auto text-center"
    >
        <div class="max-w-6xl mx-auto">
            <div 
                :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'" 
                class="transition-all duration-700 ease-out"
                ref="targetRef"
            >
                <h2 class="text-4xl md:text-5xl leading-tight tracking-tight mb-10 animate-fade-in-up" style="opacity: 0; animation-delay: 1.1s">
                    Sobre nós
                </h2>
                
                <img
                src="/sobrenos.png"
                alt="Equipe Cronomarket"
                class="w-full max-w-2xl mx-auto rounded-3xl object-cover border border-gray-200 animate-fade-in-up"
                style="opacity: 0; animation-delay: 1.2s"
                />
            </div>
                
            <p
                class="mt-8 text-gray-600 text-base md:text-lg max-w-6xl mx-auto animate-fade-in-up"
                style="opacity: 0; animation-delay: 1.3s"
            >
                O Cronomarket é uma empresa capixaba, fundada por estudantes universitários do IFES Serra, 
                que nasce com o propósito de unir tecnologia, entretenimento e informação em uma única experiência. 
                Acreditamos que acompanhar acontecimentos e tendências pode ser tão envolvente quanto desafiador, 
                e por isso criamos um ambiente onde o usuário não apenas consome conteúdo, mas também interage de forma ativa com ele.
            </p>
            
            <p
                class="mt-8 text-gray-600 text-base md:text-lg max-w-6xl mx-auto animate-fade-in-up"
                style="opacity: 0; animation-delay: 1.3s"
            >
                Nosso objetivo é trazer entretenimento enquanto fomentamos a busca por conhecimento e atualidades, 
                incentivando o pensamento crítico e o interesse por temas relevantes do cenário global. 
                Queremos transformar a maneira como as pessoas se conectam com informações, 
                tornando esse processo mais dinâmico, acessível e estimulante.
            </p>

            <button
                class="mt-8 bg-black text-white px-8 py-3 rounded-full text-base font-medium hover:bg-gray-800 transition-colors animate-fade-in-up"
                style="opacity: 0; animation-delay: 1.4s"
            >
                Venha fazer parte dessa história!
            </button>
        </div>
    </section>
</template>