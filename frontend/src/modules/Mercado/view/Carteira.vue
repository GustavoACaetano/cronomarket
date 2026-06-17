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
const portfolioAtivo = ref<any[]>([]);
const portfolioEncerrado = ref<any[]>([]);
const isLoading = ref(true);

const { data: categoriasData } = useGetCategoria();

const fetchPortfolio = async () => {
    if (!currentUser.value) return;
    try {
        // Fetch current user details
        const resUser = await api.get(`/api/usuarios/${currentUser.value.usuario_id}/`);
        userBalance.value = parseFloat(resUser.data.saldo);

        // Fetch user positions (Acao)
        const resAcoes = await api.get('/api/acoes/');
        const listAcoes = Array.isArray(resAcoes.data) ? resAcoes.data : resAcoes.data.results || [];
        
        // Fetch operations (to compute investment for resolved positions)
        const resOps = await api.get('/api/operacoes/');
        const listOps = Array.isArray(resOps.data) ? resOps.data : resOps.data.results || [];

        const activeList: any[] = [];
        const resolvedList: any[] = [];

        await Promise.all(listAcoes.map(async (acao: any) => {
            const resMarket = await api.get(`/api/mercados/${acao.mercado}/`);
            const market = resMarket.data;
            const optionName = acao.eh_sucesso ? market.opcao_sucesso : market.opcao_fracasso;

            if (market.ativo) {
                if (acao.quantidade > 0) {
                    activeList.push({
                        ...acao,
                        marketTitle: market.titulo,
                        marketImage: market.link_imagem,
                        optionName,
                        ativo: true
                    });
                }
            } else {
                // Resolved market: Acao quantity is set to 0 by backend
                // Find total shares user accumulated before resolution by summing up net operations
                const marketOps = listOps.filter((o: any) => o.mercado === acao.mercado && o.usuario === currentUser.value.usuario_id);
                let totalShares = 0;
                let totalInvested = 0;

                marketOps.forEach((op: any) => {
                    if (op.tipo === 1) { // COMPRA
                        totalShares += op.quantidade;
                        totalInvested += parseFloat(op.valor_total);
                    } else if (op.tipo === 2) { // VENDA
                        // Standard reduction
                        const avg = totalShares > 0 ? (totalInvested / totalShares) : 0;
                        const qty = Math.min(totalShares, op.quantidade);
                        totalShares -= qty;
                        totalInvested -= (qty * avg);
                    }
                });

                if (totalShares > 0) {
                    // Find if the user won: get resolved Resultado object
                    let won = false;
                    try {
                        const resResult = await api.get(`/api/resultados/?mercado=${acao.mercado}`);
                        const resultList = Array.isArray(resResult.data) ? resResult.data : resResult.data.results || [];
                        if (resultList.length > 0) {
                            const outcome = resultList[0].sucesso;
                            won = (outcome === acao.eh_sucesso);
                        }
                    } catch (e) {
                        console.error('Erro ao buscar resultado do mercado', e);
                    }

                    const avgPrice = totalInvested / totalShares;
                    const finalValue = won ? (totalShares * 1.00) : 0;
                    const profitLoss = finalValue - totalInvested;

                    resolvedList.push({
                        ...acao,
                        marketTitle: market.titulo,
                        marketImage: market.link_imagem,
                        optionName,
                        quantidadeOriginal: totalShares,
                        totalInvestido: totalInvested,
                        precoMedioCalculado: avgPrice,
                        finalValue,
                        profitLoss,
                        won,
                        ativo: false
                    });
                }
            }
        }));

        portfolioAtivo.value = activeList;
        portfolioEncerrado.value = resolvedList;
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
    return 'C$ ' + val.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
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

            <!-- Portfolio Shares List (Active) -->
            <div class="bg-white rounded-2xl border border-gray-100 p-6 flex flex-col gap-y-4">
                <h2 class="text-md font-semibold text-gray-900 border-b border-gray-100 pb-3">Minhas Posições Ativas</h2>
                
                <div v-if="isLoading" class="flex flex-col items-center justify-center py-12 gap-y-3">
                    <USpinIcon class="w-8 h-8 text-primary animate-spin" />
                    <span class="text-xs text-gray-400 font-light">Buscando investimentos...</span>
                </div>

                <div v-else-if="portfolioAtivo.length === 0" class="text-center py-12 text-gray-400 font-light text-sm">
                    Você ainda não possui nenhuma ação ativa de previsão. Explore os mercados para começar!
                    <div class="mt-4">
                        <UButton color="primary" size="md" @click="router.push('/mercados/home')">Ver Mercados</UButton>
                    </div>
                </div>

                <div v-else class="flex flex-col gap-y-4">
                    <div 
                        v-for="item in portfolioAtivo" 
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

            <!-- Portfolio Shares List (Resolved / Closed) -->
            <div class="bg-white rounded-2xl border border-gray-100 p-6 flex flex-col gap-y-4">
                <h2 class="text-md font-semibold text-gray-900 border-b border-gray-100 pb-3">Minhas Posições Encerradas</h2>

                <div v-if="isLoading" class="flex flex-col items-center justify-center py-12 gap-y-3">
                    <USpinIcon class="w-8 h-8 text-primary animate-spin" />
                    <span class="text-xs text-gray-400 font-light">Carregando histórico...</span>
                </div>

                <div v-else-if="portfolioEncerrado.length === 0" class="text-center py-12 text-gray-400 font-light text-sm">
                    Nenhum investimento resolvido até o momento.
                </div>

                <div v-else class="flex flex-col gap-y-4">
                    <div 
                        v-for="item in portfolioEncerrado" 
                        :key="'resolved-' + item.id" 
                        class="p-4 border border-gray-100 rounded-xl flex items-center justify-between gap-x-4 hover:border-gray-200 transition-colors cursor-pointer"
                        @click="router.push(`/mercados/${item.mercado}`)"
                    >
                        <div class="flex items-center gap-x-4">
                            <img :src="item.marketImage" alt="" class="w-12 h-12 object-cover rounded-lg border border-gray-100 filter grayscale opacity-75" />
                            <div class="flex flex-col gap-y-1">
                                <h3 class="text-sm font-medium text-gray-500 line-clamp-1 max-w-md">{{ item.marketTitle }}</h3>
                                <div class="flex items-center gap-x-2 text-xs">
                                    <span class="text-gray-400">Sua aposta:</span>
                                    <span 
                                        class="px-2 py-0.5 rounded text-[10px] font-bold uppercase"
                                        :class="item.eh_sucesso ? 'bg-primary-50 text-primary-700' : 'bg-red-50 text-red-700'"
                                    >
                                        {{ item.optionName }}
                                    </span>
                                    <span class="text-gray-300">•</span>
                                    <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase" :class="item.won ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-700'">
                                        {{ item.won ? 'Acertou' : 'Errou' }}
                                    </span>
                                </div>
                            </div>
                        </div>
                        <div class="text-right flex flex-col gap-y-0.5">
                            <span class="text-sm font-bold text-gray-500">{{ item.quantidadeOriginal }} cotas</span>
                            <span 
                                class="text-xs font-semibold"
                                :class="item.profitLoss >= 0 ? 'text-green-600' : 'text-red-500'"
                            >
                                {{ item.profitLoss >= 0 ? '+' : '' }}{{ formatCurrency(item.profitLoss) }}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
