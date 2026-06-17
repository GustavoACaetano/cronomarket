<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useGetCategoria } from '../composables/useGetCategoria';
import { api } from '@/common/services/api';

const router = useRouter();

const currentUser = computed(() => {
    try {
        const raw = localStorage.getItem('cronomarket_user');
        return raw ? JSON.parse(raw) : null;
    } catch {
        return null;
    }
});

// Force login redirect
if (!currentUser.value) {
    router.push('/login');
}

const userBalance = ref(0.00);
const portfolio = ref<any[]>([]);
const isLoading = ref(true);

const { data: categoriasData } = useGetCategoria();

const fetchPortfolio = async () => {
    if (!currentUser.value) return;
    try {
        // Fetch current user details
        const resUser = await api.get(`/api/usuarios/${currentUser.value.usuario_id}/`);
        userBalance.value = parseFloat(resUser.data.saldo);

        // Fetch user positions
        const resAcoes = await api.get('/api/acoes/');
        const listAcoes = Array.isArray(resAcoes.data) ? resAcoes.data : resAcoes.data.results || [];
        
        // Fetch markets to display proper details
        const listWithMarkets = await Promise.all(listAcoes.map(async (acao: any) => {
            const resMarket = await api.get(`/api/mercados/${acao.mercado}/`);
            return {
                ...acao,
                marketTitle: resMarket.data.titulo,
                marketImage: resMarket.data.link_imagem,
                optionName: acao.eh_sucesso ? resMarket.data.opcao_sucesso : resMarket.data.opcao_fracasso,
                regraEncerramento: resMarket.data.regra_encerramento,
                ativo: resMarket.data.ativo
            };
        }));
        portfolio.value = listWithMarkets;
    } catch (e) {
        console.error('Erro ao carregar carteira', e);
    } finally {
        isLoading.value = false;
    }
};

onMounted(() => {
    fetchPortfolio();
});

const formatCurrency = (val: number) => {
    return val.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
};
</script>

<template>
    <div class="min-h-screen bg-gray-50/50 py-8 px-4 sm:px-6 lg:px-8">
        <div class="max-w-4xl mx-auto flex flex-col gap-y-6">
            <!-- Header Balance Panel -->
            <div class="bg-white p-6 rounded-2xl border border-gray-100 flex flex-col sm:flex-row justify-between sm:items-center gap-y-4">
                <div class="flex flex-col gap-y-1">
                    <h1 class="text-2xl font-semibold text-gray-900">Minha Carteira</h1>
                    <span class="text-xs font-light text-gray-400">Acompanhe suas posições ativas e saldo disponível.</span>
                </div>
                <div class="flex flex-col bg-primary-50/50 px-5 py-3 rounded-xl border border-primary-100 text-right sm:min-w-[180px]">
                    <span class="text-xs text-primary-600 font-light">Saldo Disponível</span>
                    <span class="text-2xl font-bold text-primary-700 mt-0.5">{{ formatCurrency(userBalance) }}</span>
                </div>
            </div>

            <!-- Portfolio Shares List -->
            <div class="bg-white rounded-2xl border border-gray-100 p-6 flex flex-col gap-y-4">
                <h2 class="text-md font-semibold text-gray-900 border-b border-gray-100 pb-3">Minhas Posições Ativas</h2>
                
                <div v-if="isLoading" class="flex flex-col items-center justify-center py-12 gap-y-3">
                    <USpinIcon class="w-8 h-8 text-primary animate-spin" />
                    <span class="text-xs text-gray-400 font-light">Buscando investimentos...</span>
                </div>

                <div v-else-if="portfolio.length === 0" class="text-center py-12 text-gray-400 font-light text-sm">
                    Você ainda não comprou nenhuma ação de previsão. Explore os mercados para começar!
                    <div class="mt-4">
                        <UButton color="primary" size="md" @click="router.push('/mercados/home')">Ver Mercados</UButton>
                    </div>
                </div>

                <div v-else class="flex flex-col gap-y-4">
                    <div 
                        v-for="item in portfolio" 
                        :key="item.id" 
                        class="p-4 border border-gray-100 rounded-xl flex items-center justify-between gap-x-4 hover:border-gray-200 transition-colors cursor-pointer"
                        @click="router.push(`/mercados/${item.mercado}`)"
                    >
                        <div class="flex items-center gap-x-4">
                            <img :src="item.marketImage" alt="" class="w-12 h-12 object-cover rounded-lg border border-gray-100" />
                            <div class="flex flex-col gap-y-1">
                                <h3 class="text-sm font-medium text-gray-800 line-clamp-1 max-w-md">{{ item.marketTitle }}</h3>
                                <div class="flex items-center gap-x-2 text-xs">
                                    <span class="text-gray-400">Escolha:</span>
                                    <span 
                                        class="px-2 py-0.5 rounded text-[10px] font-bold uppercase"
                                        :class="item.eh_sucesso ? 'bg-primary-50 text-primary-700' : 'bg-red-50 text-red-700'"
                                    >
                                        {{ item.optionName }}
                                    </span>
                                    <span class="text-gray-300">•</span>
                                    <span class="text-gray-500 font-light">Média: {{ formatCurrency(parseFloat(item.preco_medio)) }}</span>
                                </div>
                            </div>
                        </div>
                        <div class="text-right flex flex-col gap-y-0.5">
                            <span class="text-sm font-bold text-gray-900">{{ item.quantidade }} cotas</span>
                            <span class="text-xs text-gray-400 font-light">Investido: {{ formatCurrency(item.quantidade * parseFloat(item.preco_medio)) }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
