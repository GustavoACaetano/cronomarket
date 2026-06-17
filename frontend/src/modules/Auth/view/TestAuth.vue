<script setup lang="ts">
import { ref } from 'vue';
import { api } from '@/common/services/api';

const loading = ref(false);
const result = ref<any>(null);
const error = ref<any>(null);

const testAuth = async () => {
    loading.value = true;
    result.value = null;
    error.value = null;

    try {
        const response = await api.get('/api/mercados/');
        result.value = response.data;
    } catch (err: any) {
        error.value = {
            status: err.response?.status,
            message: err.message,
            data: err.response?.data,
        };
    } finally {
        loading.value = false;
    }
};
</script>

<template>
    <div style="background: #ffcccc; color: #330000; padding: 20px; font-family: monospace; min-h: 100vh;">
        <h1 style="color: red; border-bottom: 5px solid red; padding-bottom: 10px;">
            ⚠️ PÁGINA DE TESTE FEIONA DA AUTENTICAÇÃO ⚠️
        </h1>
        <p>Esta página faz um GET em <code>/api/mercados/</code> para ver se o cookie de sessão está funcionando.</p>

        <button 
            @click="testAuth" 
            style="background: black; color: yellow; font-size: 20px; padding: 15px; border: 3px dashed yellow; cursor: pointer; font-weight: bold;"
            :disabled="loading"
        >
            {{ loading ? 'CARREGANDO...' : 'DISPARAR REQUISIÇÃO (GET /api/mercados/)' }}
        </button>

        <div style="margin-top: 20px; background: white; color: black; padding: 15px; border: 2px solid black;">
            <h3>Resultado de Sucesso:</h3>
            <pre v-if="result" style="background: #e6ffe6; padding: 10px; border: 1px solid green; overflow: auto;">{{ JSON.stringify(result, null, 2) }}</pre>
            <span v-else style="color: gray;">(Nenhum resultado ainda)</span>
        </div>

        <div style="margin-top: 20px; background: white; color: black; padding: 15px; border: 2px solid black;">
            <h3>Resultado de Erro:</h3>
            <pre v-if="error" style="background: #ffe6e6; padding: 10px; border: 1px solid red; color: red; overflow: auto;">{{ JSON.stringify(error, null, 2) }}</pre>
            <span v-else style="color: gray;">(Nenhum erro ainda)</span>
        </div>
    </div>
</template>
