<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useOperacoesMercado } from '../composables/useOperacoesMercado';
import { useGetCategoria } from '../composables/useGetCategoria';
import { api } from '@/common/services/api';
import { getAvatarColor } from '@/common/utils/avatarColorHelper';

const route = useRoute();
const router = useRouter();
const mercadoId = computed(() => route.params.id as string);

const {
    mercado,
    isLoadingMercado,
    comentarios,
    comprar,
    isComprando,
    vender,
    isVendendo,
    adicionarComentario,
    isEnviandoComentario,
    encerrarMercado,
    isEncerrando,
    errorMessage,
} = useOperacoesMercado(mercadoId.value);

const { data: categoriasData } = useGetCategoria();
const toast = useToast();

// Session / Local Storage Info
const currentUser = computed(() => {
    try {
        const raw = localStorage.getItem('cronomarket_user');
        return raw ? JSON.parse(raw) : null;
    } catch {
        return null;
    }
});

// Admin status and balance checks
const isAdmin = ref(false);
const userBalance = ref(0.00);
const userShares = ref({ sucesso: 0, fracasso: 0 });

const fetchUserData = async () => {
    if (!currentUser.value) return;
    try {
        // Fetch user object to get current balance and admin status
        const resUser = await api.get(`/api/usuarios/${currentUser.value.usuario_id}/`);
        isAdmin.value = resUser.data.eh_admin;
        userBalance.value = parseFloat(resUser.data.saldo);

        // Fetch user actions in this market
        const resAcoes = await api.get('/api/acoes/');
        const listAcoes = Array.isArray(resAcoes.data) ? resAcoes.data : resAcoes.data.results || [];
        
        let sucessoCount = 0;
        let fracassoCount = 0;
        listAcoes.forEach((acao: any) => {
            if (acao.mercado === parseInt(mercadoId.value)) {
                if (acao.eh_sucesso) sucessoCount += acao.quantidade;
                else fracassoCount += acao.quantidade;
            }
        });
        userShares.value = { sucesso: sucessoCount, fracasso: fracassoCount };
    } catch (e) {
        console.error('Erro ao buscar perfil do usuário', e);
    }
};

onMounted(() => {
    fetchUserData();
});

// Tabs: Comprar, Vender, Comentários, Admin
const activeTab = ref<'comprar' | 'vender'>('comprar');
const selectedOutcome = ref<boolean>(true); // true = Sim (sucesso), false = Não (fracasso)
const tradeQuantity = ref(1);
const commentText = ref('');

// LMSR helper calculations for previewing cost/revenue
const estimatePrice = computed(() => {
    if (!mercado.value) return 0.00;
    
    const q_s = parseFloat(mercado.value.valor_total_sucesso);
    const q_f = parseFloat(mercado.value.valor_total_fracasso);
    const b = parseFloat(mercado.value.liquidez_inicial);
    const qty = tradeQuantity.value || 0;

    const getCost = (qs: number, qf: number) => {
        const x = qs / b;
        const y = qf / b;
        const maxVal = Math.max(x, y);
        return b * (maxVal + Math.log(Math.exp(x - maxVal) + Math.exp(y - maxVal)));
    };

    const costBefore = getCost(q_s, q_f);

    if (activeTab.value === 'comprar') {
        const costAfter = selectedOutcome.value 
            ? getCost(q_s + qty, q_f) 
            : getCost(q_s, q_f + qty);
        return costAfter - costBefore;
    } else {
        // Vender
        const costAfter = selectedOutcome.value 
            ? getCost(Math.max(0, q_s - qty), q_f) 
            : getCost(q_s, Math.max(0, q_f - qty));
        return costBefore - costAfter; // Revenue received
    }
});

// Category Tag Mappings
const categoriasText = computed(() => {
    if (!categoriasData.value || !mercado.value || !mercado.value.categorias) return '';
    const list = Array.isArray(categoriasData.value) 
        ? categoriasData.value 
        : (categoriasData.value as any).results || [];
    return list
        .filter((cat: any) => mercado.value.categorias.includes(cat.id))
        .map((cat: any) => cat.nome)
        .join(', ');
});

// Average probability percentages for graph mock
const percentSucesso = computed(() => {
    if (!mercado.value) return 50;
    const q_s = parseFloat(mercado.value.valor_total_sucesso);
    const q_f = parseFloat(mercado.value.valor_total_fracasso);
    if (q_s === 0 && q_f === 0) return 50;
    const b = parseFloat(mercado.value.liquidez_inicial);
    const exp_s = Math.exp(q_s / b);
    const exp_f = Math.exp(q_f / b);
    return Math.round((exp_s / (exp_s + exp_f)) * 100);
});

const percentFracasso = computed(() => {
    return 100 - percentSucesso.value;
});

// Handlers
const handleTrade = async () => {
    if (!currentUser.value) {
        toast.add({ title: 'Atenção', description: 'Você precisa fazer login para negociar.', color: 'warning' });
        router.push('/login');
        return;
    }

    if (tradeQuantity.value <= 0) {
        toast.add({ title: 'Quantidade Inválida', description: 'Por favor insira um valor positivo.', color: 'error' });
        return;
    }

    try {
        if (activeTab.value === 'comprar') {
            await comprar({ eh_sucesso: selectedOutcome.value, quantidade: tradeQuantity.value });
            toast.add({ title: 'Sucesso', description: 'Compra realizada com sucesso!', color: 'success' });
        } else {
            // Check portfolio shares
            const available = selectedOutcome.value ? userShares.value.sucesso : userShares.value.fracasso;
            if (available < tradeQuantity.value) {
                toast.add({ title: 'Erro', description: 'Você não tem cotas suficientes para vender.', color: 'error' });
                return;
            }
            await vender({ eh_sucesso: selectedOutcome.value, quantidade: tradeQuantity.value });
            toast.add({ title: 'Sucesso', description: 'Venda realizada com sucesso!', color: 'success' });
        }
        tradeQuantity.value = 1;
        fetchUserData();
    } catch (e) {
        // Handled by errorMessage reatively
    }
};

const handleAddComment = async () => {
    if (!commentText.value.trim()) return;
    try {
        await adicionarComentario(commentText.value);
        commentText.value = '';
        toast.add({ title: 'Comentário enviado!', color: 'success' });
    } catch (e) {
        // Error is shown in alert
    }
};

const handleResolveMarket = async (sucesso: boolean) => {
    const optionName = sucesso ? mercado.value?.opcao_sucesso : mercado.value?.opcao_fracasso;
    const confirmacao = window.confirm(`Tem certeza de que deseja encerrar este mercado definindo o resultado vencedor como "${optionName}"? Esta ação não pode ser desfeita.`);
    if (!confirmacao) return;

    try {
        await encerrarMercado(sucesso);
        toast.add({ title: 'Sucesso', description: `Mercado resolvido como "${optionName}" com sucesso!`, color: 'success' });
        fetchUserData();
    } catch (e) {
        // Handled by query client
    }
};

const formatCurrency = (val: number) => {
    return val.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
};
</script>

<template>
    <div class="min-h-screen bg-gray-50/50 py-8 px-4 sm:px-6 lg:px-8">
        <div v-if="isLoadingMercado" class="flex flex-col items-center justify-center py-20 gap-y-4">
            <USpinIcon class="w-8 h-8 text-primary animate-spin" />
            <span class="text-sm text-gray-500 font-light">Carregando mercado...</span>
        </div>

        <div v-else-if="mercado" class="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- Left & Middle: Title, Description, Graph, Comments -->
            <div class="lg:col-span-2 flex flex-col gap-y-6">
                <!-- Market Header Info Card -->
                <div class="bg-white p-6 rounded-2xl border border-gray-100 flex gap-x-5 items-start">
                    <img 
                        :src="mercado.link_imagem" 
                        alt="Logo do mercado" 
                        class="w-16 h-16 object-cover rounded-xl border border-gray-100"
                    />
                    <div class="flex flex-col gap-y-1.5">
                        <span class="text-xs font-light text-gray-400 uppercase tracking-wider">
                            {{ categoriasText || 'Geral' }}
                        </span>
                        <h1 class="text-2xl font-semibold text-gray-900 leading-tight">
                            {{ mercado.titulo }}
                        </h1>
                        <div class="flex flex-wrap gap-x-4 gap-y-1 mt-1 text-xs text-gray-500">
                            <span>Expira em: <strong class="font-medium text-gray-700">{{ mercado.data_encerramento }}</strong></span>
                            <span>•</span>
                            <span>Liquidez inicial (b): <strong class="font-medium text-gray-700">{{ formatCurrency(parseFloat(mercado.liquidez_inicial)) }}</strong></span>
                        </div>
                    </div>
                </div>

                <!-- Graphic/Odds Mock Panel -->
                <div class="bg-white p-6 rounded-2xl border border-gray-100 flex flex-col gap-y-4">
                    <h2 class="text-md font-semibold text-gray-900">Probabilidade do Mercado</h2>
                    
                    <div class="flex items-center gap-x-4 w-full bg-gray-50 p-4 rounded-xl">
                        <div class="flex flex-col flex-1 gap-y-1 text-center border-r border-gray-200 pr-4">
                            <span class="text-xs text-gray-500 font-light">{{ mercado.opcao_sucesso }}</span>
                            <span class="text-2xl font-bold text-primary">{{ percentSucesso }}%</span>
                        </div>
                        <div class="flex flex-col flex-1 gap-y-1 text-center">
                            <span class="text-xs text-gray-500 font-light">{{ mercado.opcao_fracasso }}</span>
                            <span class="text-2xl font-bold text-red-600">{{ percentFracasso }}%</span>
                        </div>
                    </div>

                    <!-- Rule description -->
                    <div class="text-sm text-gray-600 mt-2">
                        <h4 class="font-medium text-gray-900 mb-1">Regras de Encerramento:</h4>
                        <p class="font-light text-gray-500 bg-gray-50/50 p-3 rounded-lg border border-gray-100">
                            {{ mercado.regra_encerramento }}
                        </p>
                    </div>

                    <div class="text-sm text-gray-600">
                        <h4 class="font-medium text-gray-900 mb-1">Sobre:</h4>
                        <p class="font-light text-gray-500">
                            {{ mercado.descricao }}
                        </p>
                    </div>
                </div>

                <!-- Comments Section -->
                <div class="bg-white p-6 rounded-2xl border border-gray-100 flex flex-col gap-y-6">
                    <h3 class="text-md font-semibold text-gray-900">Comentários</h3>

                    <!-- Comment input -->
                    <div v-if="currentUser" class="flex flex-col gap-y-3">
                        <UTextarea 
                            v-model="commentText" 
                            placeholder="Escreva sua opinião sobre este mercado..." 
                            size="md" 
                            rows="3"
                        />
                        <div class="flex justify-end">
                            <UButton 
                                color="primary" 
                                size="md" 
                                :loading="isEnviandoComentario" 
                                :disabled="!commentText.trim()"
                                @click="handleAddComment"
                            >
                                Enviar Comentário
                            </UButton>
                        </div>
                    </div>
                    <div v-else class="text-center py-4 bg-gray-50 rounded-xl border border-dashed border-gray-200">
                        <span class="text-sm text-gray-500">
                            Você precisa estar logado para comentar. 
                            <UButton variant="link" color="primary" size="sm" @click="router.push('/login')" class="px-0 ml-1">Entrar</UButton>
                        </span>
                    </div>

                    <!-- Comment list -->
                    <div class="flex flex-col gap-y-4 max-h-[400px] overflow-y-auto pr-2">
                        <div v-for="c in comentarios" :key="c.id" class="border-b border-gray-50 pb-4">
                            <div class="flex items-start gap-x-3">
                                <!-- Colored Avatar -->
                                <div 
                                    class="w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-semibold uppercase flex-shrink-0"
                                    :style="{ backgroundColor: getAvatarColor(c.username || 'Anonimo') }"
                                >
                                    {{ (c.username || 'A')[0] }}
                                </div>
                                <div class="flex-1">
                                    <div class="flex items-center justify-between mb-1">
                                        <span class="text-sm font-semibold text-gray-800">{{ c.username || 'Anônimo' }}</span>
                                        <span class="text-xs text-gray-400 font-light">{{ new Date(c.criado_em).toLocaleString() }}</span>
                                    </div>
                                    <p class="text-sm text-gray-600 font-light">
                                        {{ c.mensagem }}
                                    </p>
                                </div>
                            </div>
                        </div>
                        <div v-if="!comentarios || comentarios.length === 0" class="text-center text-gray-400 py-6 font-light text-sm">
                            Nenhum comentário enviado ainda. Seja o primeiro a opinar!
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right: Trading Panel -->
            <div class="flex flex-col gap-y-6">
                <!-- Balance & Positions overview -->
                <div v-if="currentUser" class="bg-white p-6 rounded-2xl border border-gray-100 flex flex-col gap-y-3">
                    <h3 class="text-sm font-medium text-gray-500 uppercase tracking-wider">Sua Carteira</h3>
                    <div class="flex justify-between items-center">
                        <span class="text-xs text-gray-400 font-light">Saldo Disponível</span>
                        <span class="text-lg font-bold text-gray-900">{{ formatCurrency(userBalance) }}</span>
                    </div>
                    <div class="border-t border-gray-50 pt-3 flex flex-col gap-y-2">
                        <div class="flex justify-between items-center text-xs text-gray-500">
                            <span>Minhas Cotas ({{ mercado.opcao_sucesso }}):</span>
                            <span class="font-semibold text-primary">{{ userShares.sucesso }} cotas</span>
                        </div>
                        <div class="flex justify-between items-center text-xs text-gray-500">
                            <span>Minhas Cotas ({{ mercado.opcao_fracasso }}):</span>
                            <span class="font-semibold text-red-600">{{ userShares.fracasso }} cotas</span>
                        </div>
                    </div>
                </div>

                <!-- Buy/Sell Form Card -->
                <div class="bg-white p-6 rounded-2xl border border-gray-100 flex flex-col gap-y-4">
                    <!-- Tab toggle (Comprar/Vender) -->
                    <div class="flex border-b border-gray-100 pb-2">
                        <button 
                            class="flex-1 text-center py-2 text-sm font-medium transition-colors border-b-2 cursor-pointer"
                            :class="activeTab === 'comprar' ? 'border-primary text-primary' : 'border-transparent text-gray-400'"
                            @click="activeTab = 'comprar'"
                        >
                            Comprar
                        </button>
                        <button 
                            class="flex-1 text-center py-2 text-sm font-medium transition-colors border-b-2 animate-duration-100 cursor-pointer"
                            :class="activeTab === 'vender' ? 'border-primary text-primary' : 'border-transparent text-gray-400'"
                            @click="activeTab = 'vender'"
                        >
                            Vender
                        </button>
                    </div>

                    <!-- Outcome Pick buttons -->
                    <div class="flex gap-x-3 mt-2">
                        <button 
                            class="flex-1 py-3 px-4 border rounded-xl text-sm font-medium transition-all text-center flex flex-col items-center gap-y-0.5 cursor-pointer"
                            :class="selectedOutcome === true ? 'bg-primary-50 border-primary text-primary-700 font-semibold' : 'bg-white border-gray-200 text-gray-600'"
                            @click="selectedOutcome = true"
                        >
                            <span>{{ mercado.opcao_sucesso }}</span>
                            <span class="text-xs opacity-80">{{ percentSucesso }}%</span>
                        </button>
                        <button 
                            class="flex-1 py-3 px-4 border rounded-xl text-sm font-medium transition-all text-center flex flex-col items-center gap-y-0.5 cursor-pointer"
                            :class="selectedOutcome === false ? 'bg-red-50 border-red-500 text-red-700 font-semibold' : 'bg-white border-gray-200 text-gray-600'"
                            @click="selectedOutcome = false"
                        >
                            <span>{{ mercado.opcao_fracasso }}</span>
                            <span class="text-xs opacity-80">{{ percentFracasso }}%</span>
                        </button>
                    </div>

                    <!-- Quantity input -->
                    <div class="flex flex-col gap-y-1.5 mt-2">
                        <label class="text-xs text-gray-500 font-light">Quantidade de cotas:</label>
                        <UInput 
                            v-model="tradeQuantity" 
                            type="number" 
                            min="1" 
                            placeholder="Ex: 10" 
                            size="lg" 
                            class="w-full"
                        />
                    </div>

                    <!-- Estimated values -->
                    <div class="bg-gray-50 p-4 rounded-xl flex flex-col gap-y-2 border border-gray-100 text-sm mt-2">
                        <div class="flex justify-between items-center text-gray-500">
                            <span>{{ activeTab === 'comprar' ? 'Custo estimado:' : 'Retorno estimado:' }}</span>
                            <span class="font-bold text-gray-900">{{ formatCurrency(estimatePrice) }}</span>
                        </div>
                        <div class="flex justify-between items-center text-xs text-gray-400 font-light border-t border-gray-200/50 pt-2">
                            <span>Preço unitário médio:</span>
                            <span>{{ formatCurrency(tradeQuantity > 0 ? (estimatePrice / tradeQuantity) : 0) }}</span>
                        </div>
                    </div>

                    <!-- Error messaging inside component -->
                    <UAlert
                        v-if="errorMessage"
                        color="error"
                        variant="subtle"
                        :title="errorMessage"
                        class="w-full mt-2"
                    />

                    <!-- Main call to action -->
                    <UButton 
                        color="primary" 
                        size="xl" 
                        class="w-full justify-center h-12 mt-2"
                        :loading="isComprando || isVendendo"
                        :disabled="!mercado.ativo || isComprando || isVendendo"
                        @click="handleTrade"
                    >
                        {{ !mercado.ativo ? 'Mercado Encerrado' : (activeTab === 'comprar' ? 'Comprar Cotas' : 'Vender Cotas') }}
                    </UButton>
                </div>

                <!-- Admin Action Card -->
                <div v-if="isAdmin && mercado.ativo" class="bg-white p-6 rounded-2xl border border-red-100 bg-red-50/10 flex flex-col gap-y-4">
                    <h3 class="text-md font-semibold text-red-800">Painel do Administrador</h3>
                    <p class="text-xs text-gray-500 font-light">
                        Como administrador, defina o resultado correto para encerrar este mercado e liquidar os dividendos dos vencedores.
                    </p>

                    <div class="flex gap-x-3">
                        <UButton 
                            color="success" 
                            class="flex-1 justify-center" 
                            size="md"
                            :loading="isEncerrando"
                            @click="handleResolveMarket(true)"
                        >
                            Resolver SIM
                        </UButton>
                        <UButton 
                            color="error" 
                            class="flex-1 justify-center" 
                            size="md"
                            :loading="isEncerrando"
                            @click="handleResolveMarket(false)"
                        >
                            Resolver NÃO
                        </UButton>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
