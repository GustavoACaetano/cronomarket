<script lang="ts" setup>
import { computed } from 'vue';
import type { Mercado } from '../api/types/index';
import { useRouter } from 'vue-router';
import { useGetCategoria } from '../composables/useGetCategoria';

const props = defineProps<{
    mercado: Mercado
}>();

const router = useRouter();

// Calculate percentage probabilities based on LMSR weights
const percentSucesso = computed(() => {
    const q_s = parseFloat(props.mercado.valor_total_sucesso);
    const q_f = parseFloat(props.mercado.valor_total_fracasso);
    if (q_s === 0 && q_f === 0) return 50;
    
    // Using simple probability from LMSR prices
    const b = parseFloat(props.mercado.liquidez_inicial);
    const exp_s = Math.exp(q_s / b);
    const exp_f = Math.exp(q_f / b);
    return Math.round((exp_s / (exp_s + exp_f)) * 100);
});

const percentFracasso = computed(() => {
    return 100 - percentSucesso.value;
});

const formatCurrency = (val: string) => {
    const parsed = parseFloat(val);
    return isNaN(parsed) ? 'C$ 0,00' : 'C$ ' + parsed.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
};

// Map category IDs to names using the cached categories query or a static lookup if needed.
// However, since we might want to display names, we can pass props or use the categoriesData.
const { data: categoriasData } = useGetCategoria();
const categoriasText = computed(() => {
    if (!categoriasData.value || !props.mercado.categorias) return '';
    const list = Array.isArray(categoriasData.value) 
        ? categoriasData.value 
        : (categoriasData.value as any).results || [];
    
    return list
        .filter((cat: any) => props.mercado.categorias.includes(cat.id))
        .map((cat: any) => cat.nome)
        .join(', ');
});

const goToMarket = () => {
    router.push(`/mercados/${props.mercado.id}`);
};
</script>

<template>
    <UCard 
        class="cursor-pointer hover:shadow-md transition-shadow duration-200 border border-gray-100 hover:border-gray-200 rounded-xl" 
        :ui="{ body: 'p-4', root: 'bg-white rounded-xl' }"
        @click="goToMarket"
    >
        <div class="flex flex-col h-full justify-between gap-y-4">
            <!-- Header: Image and Title -->
            <div class="flex gap-x-3 items-start">
                <img 
                    :src="mercado.link_imagem" 
                    alt="Imagem do mercado" 
                    class="w-12 h-12 object-cover rounded-lg flex-shrink-0"
                />
                <div class="flex flex-col gap-y-0.5">
                    <span class="text-xs font-light text-gray-400 uppercase tracking-wider">
                        {{ categoriasText || 'Geral' }}
                    </span>
                    <h3 class="text-sm font-medium text-gray-900 line-clamp-2 leading-tight">
                        {{ mercado.titulo }}
                    </h3>
                </div>
            </div>

            <!-- Prediction Options List (Kalshi-like grid style) -->
            <div class="flex flex-col gap-y-2 pt-1">
                <!-- Yes Option Line -->
                <div class="flex items-center text-sm">
                    <div class="flex items-center gap-x-3 justify-start">
                        <span class="font-semibold text-gray-900">{{ percentSucesso }}%</span>
                        <div class="flex items-center justify-center bg-primary-50 text-primary-700 font-medium px-3 py-1 rounded text-xs min-w-[50px] text-center border border-primary-200">
                            {{ mercado.opcao_sucesso }}
                        </div>
                    </div>
                </div>

                <!-- No Option Line -->
                <div class="flex items-center text-sm">
                    <div class="flex items-center gap-x-3 justify-start">
                        <div class="flex items-center justify-center bg-red-50 text-red-700 font-medium px-3 py-1 rounded text-xs min-w-[50px] text-center border border-red-200">
                            {{ mercado.opcao_fracasso }}
                        </div>
                        <span class="font-semibold text-gray-900">{{ percentFracasso }}%</span>
                        
                    </div>
                </div>
            </div>

            <!-- Bottom Stats: Volume / Liquidity -->
            <div class="flex items-center justify-between text-xs text-gray-400 border-t border-gray-50 pt-2">
                <span>Liquidez: {{ formatCurrency(mercado.liquidez_inicial) }}</span>
                <span class="flex items-center gap-x-1">
                    <span class="w-1.5 h-1.5 rounded-full" :class="mercado.ativo ? 'bg-green-500' : 'bg-gray-300'"></span>
                    {{ mercado.ativo ? 'Ativo' : 'Encerrado' }}
                </span>
            </div>
        </div>
    </UCard>
</template>
