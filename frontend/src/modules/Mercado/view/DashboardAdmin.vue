<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
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

// Force admin check
if (!currentUser.value || !currentUser.value.eh_admin) {
    router.push('/mercados/home');
}

const stats = ref({
    total_usuarios: 0,
    total_mercados_ativos: 0,
    total_mercados_encerrados: 0,
    lucro_total_taxas: 0.00,
    volume_total: 0.00
});
const isLoading = ref(true);

const fetchDashboardStats = async () => {
    try {
        const response = await api.get('/api/admin-dashboard/');
        stats.value = response.data;
    } catch (e) {
        console.error('Erro ao buscar dados do painel do administrador', e);
        router.push('/mercados/home');
    } finally {
        isLoading.value = false;
    }
};

onMounted(() => {
    fetchDashboardStats();
});

const formatCurrency = (val: number) => {
    return 'C$ ' + val.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
};
</script>

<template>
    <div class="min-h-screen bg-gray-50/50 py-8 px-4 sm:px-6 lg:px-8">
        <div class="max-w-4xl mx-auto flex flex-col gap-y-6">
            <!-- Header Panel -->
            <div class="bg-white p-6 rounded-2xl border border-gray-100 flex flex-col justify-between gap-y-2">
                <h1 class="text-2xl font-bold text-red-700 flex items-center gap-x-2">
                    <span class="w-2.5 h-2.5 bg-red-500 rounded-full animate-ping"></span>
                    Painel do Administrador
                </h1>
                <span class="text-xs font-light text-gray-400">Dashboard financeiro e controle geral de volume e taxas do sistema Cronomarket.</span>
            </div>

            <div v-if="isLoading" class="flex flex-col items-center justify-center py-20 gap-y-4">
                <USpinIcon class="w-8 h-8 text-primary animate-spin" />
                <span class="text-xs text-gray-400 font-light">Carregando painel de estatísticas...</span>
            </div>

            <!-- Stats Grid -->
            <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                <!-- Lucro Total Card -->
                <div class="bg-white p-6 rounded-2xl border border-green-100 bg-green-50/5 flex flex-col justify-between min-h-[120px]">
                    <span class="text-xs font-light text-green-600 uppercase tracking-wider">Lucro das Taxas (0.3%)</span>
                    <span class="text-3xl font-extrabold text-green-700 mt-2">
                        {{ formatCurrency(stats.lucro_total_taxas) }}
                    </span>
                </div>

                <!-- Volume Total Card -->
                <div class="bg-white p-6 rounded-2xl border border-gray-100 flex flex-col justify-between min-h-[120px]">
                    <span class="text-xs font-light text-gray-400 uppercase tracking-wider">Volume Total Negociado</span>
                    <span class="text-3xl font-extrabold text-gray-950 mt-2">
                        {{ formatCurrency(stats.volume_total) }}
                    </span>
                </div>

                <!-- Usuários Cadastrados Card -->
                <div class="bg-white p-6 rounded-2xl border border-gray-100 flex flex-col justify-between min-h-[120px]">
                    <span class="text-xs font-light text-gray-400 uppercase tracking-wider">Usuários Cadastrados</span>
                    <span class="text-3xl font-bold text-gray-950 mt-2">
                        {{ stats.total_usuarios }}
                    </span>
                </div>

                <!-- Mercados Ativos Card -->
                <div class="bg-white p-6 rounded-2xl border border-gray-100 flex flex-col justify-between min-h-[120px]">
                    <span class="text-xs font-light text-gray-400 uppercase tracking-wider">Mercados Ativos</span>
                    <span class="text-3xl font-bold text-primary mt-2">
                        {{ stats.total_mercados_ativos }}
                    </span>
                </div>

                <!-- Mercados Encerrados Card -->
                <div class="bg-white p-6 rounded-2xl border border-gray-100 flex flex-col justify-between min-h-[120px]">
                    <span class="text-xs font-light text-gray-400 uppercase tracking-wider">Mercados Resolvidos</span>
                    <span class="text-3xl font-bold text-gray-500 mt-2">
                        {{ stats.total_mercados_encerrados }}
                    </span>
                </div>
            </div>

            <!-- Main CTA buttons -->
            <div class="flex gap-x-4 mt-2">
                <UButton 
                    color="primary" 
                    size="lg" 
                    class="flex-1 justify-center" 
                    @click="router.push('/mercados/criar')"
                >
                    Criar Novo Mercado
                </UButton>
                <UButton 
                    color="gray" 
                    variant="outline" 
                    size="lg" 
                    class="flex-1 justify-center" 
                    @click="router.push('/mercados/home')"
                >
                    Ver Painel Geral de Previsões
                </UButton>
            </div>
        </div>
    </div>
</template>
