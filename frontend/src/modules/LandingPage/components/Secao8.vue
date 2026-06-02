<script setup lang="ts">
import { useInView } from '@/common/composables/useInView';
import { ref } from 'vue';
import type { AccordionItem } from '@nuxt/ui'

const { targetRef, isVisible } = useInView({ threshold: 0.3 })

const items = ref<AccordionItem[]>([
    {
        label: 'Como eu faço uma aposta em uma previsão?',
        content: 'Você escolhe um evento disponível (por exemplo: “Vai cair a energia do IFES Serra nesse mês?”), analisa as probabilidades e decide se quer apostar a favor (SIM) ou contra (NÃO). Depois, insere o valor que deseja apostar e confirma a transação.'
    },
    {
        label: 'Como funcionam as probabilidades nesse tipo de site?',
        content: 'As probabilidades são baseadas na opinião coletiva dos usuários e variam conforme mais pessoas apostam. Se muita gente acredita que algo vai acontecer, a chance (e o preço da aposta) sobe. Funciona como um “mercado”, onde oferta e demanda influenciam os valores.'
    },
    {
        label: 'Quando e como eu recebo o dinheiro se eu ganhar?',
        content: 'Após o evento ser resolvido (ou seja, quando já se sabe o resultado real), o sistema distribui automaticamente os ganhos para quem acertou a previsão. O valor é creditado na sua conta dentro da plataforma.'
    },
    {
        label: 'Posso retirar meu dinheiro a qualquer momento?',
        content: 'Você pode retirar o saldo disponível (não comprometido em apostas ativas) seguindo as regras de saque do site, que podem incluir taxas ou prazos de processamento.'
    }
])
</script>

<template>
    <section id="faq" class="bg-gray-100 w-full flex items-center justify-center">
        <div 
            class="flex items-center flex-col pb-24 md:w-7xl px-5 pt-10 transition-all duration-700 ease-out" 
            :class="isVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'"
            ref="targetRef"
        >
            <h2 class="text-5xl mb-18 text-center">
                Perguntas frequentes
            </h2>            

            <UAccordion type="multiple" :items="items" :ui="{ content: 'text-muted'}"/>
            
            <div class="flex flex-col md:flex-row gap-y-4 items-center mt-10 gap-x-2 ">
                <p>Deseja enviar uma pergunta personalizada?</p>
                <UTextarea placeholder="Pergunta personalizada" color="neutral" :highlight="false" :ui="{ base: 'bg-white text-black'}" />
                <UButton color="black" size="md" class="rounded-full ml-2 " :ui="{ base: 'px-8 py-3'}">
                    Enviar
                </UButton>
            </div>
        </div>
    </section>
</template>