<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useCreateMercado } from '../composables/useCreateMercado';
import { useGetCategoria } from '../composables/useGetCategoria';

const router = useRouter();

// Retrieve logged in user to check permissions
const currentUser = computed(() => {
    try {
        const raw = localStorage.getItem('cronomarket_user');
        return raw ? JSON.parse(raw) : null;
    } catch {
        return null;
    }
});

// If the user isn't logged in, redirect to login
if (!currentUser.value) {
    router.push('/login');
}

const toast = useToast();
const { data: categoriasData } = useGetCategoria();
const { createMercado, isCreating, errorMessage } = useCreateMercado();

// Form Fields
const form = ref({
    titulo: '',
    descricao: '',
    data_encerramento: '',
    regra_encerramento: '',
    opcao_sucesso: 'Sim',
    opcao_fracasso: 'Não',
    link_imagem: '',
    liquidez_inicial: '100.00',
    categorias: [] as number[],
});

// Category items options formatted for USelectMenu or checkbox groups
const categoriaOptions = computed(() => {
    if (!categoriasData.value) return [];
    // If the API returns the Django pagination envelope (count, next, previous, results)
    if ('results' in categoriasData.value) {
        return (categoriasData.value as any).results;
    }
    return categoriasData.value;
});

const formErrors = ref<Record<string, string>>({});

const validateForm = () => {
    const errors: Record<string, string> = {};
    if (!form.value.titulo.trim()) errors.titulo = 'O título é obrigatório.';
    if (!form.value.descricao.trim()) errors.descricao = 'A descrição é obrigatória.';
    if (!form.value.data_encerramento) errors.data_encerramento = 'A data de encerramento é obrigatória.';
    if (!form.value.regra_encerramento.trim()) errors.regra_encerramento = 'A regra de encerramento é obrigatória.';
    if (!form.value.opcao_sucesso.trim()) errors.opcao_sucesso = 'O texto da opção de sucesso é obrigatório.';
    if (!form.value.opcao_fracasso.trim()) errors.opcao_fracasso = 'O texto da opção de fracasso é obrigatório.';
    if (!form.value.link_imagem.trim()) errors.link_imagem = 'O link da imagem é obrigatório.';
    if (!form.value.liquidez_inicial || parseFloat(form.value.liquidez_inicial) <= 0) {
        errors.liquidez_inicial = 'A liquidez deve ser maior que zero.';
    }
    if (form.value.categorias.length === 0) {
        errors.categorias = 'Selecione pelo menos uma categoria.';
    }
    formErrors.value = errors;
    return Object.keys(errors).length === 0;
};

const onSubmit = async () => {
    if (!validateForm()) return;

    try {
        await createMercado({
            titulo: form.value.titulo,
            descricao: form.value.descricao,
            data_encerramento: form.value.data_encerramento,
            regra_encerramento: form.value.regra_encerramento,
            opcao_sucesso: form.value.opcao_sucesso,
            opcao_fracasso: form.value.opcao_fracasso,
            link_imagem: form.value.link_imagem,
            liquidez_inicial: parseFloat(form.value.liquidez_inicial),
            categorias: form.value.categorias,
        });

        toast.add({
            title: 'Mercado cadastrado com sucesso!',
            color: 'success',
            duration: 5000,
        });
        router.push('/mercados/home');
    } catch (error) {
        // Handled by errorMessage reatively from useCreateMercado
    }
};
</script>

<template>
    <div class="min-h-screen w-screen bg-white px-4 py-8 flex flex-col items-center justify-center">
        <div class="flex flex-col gap-y-6 w-full max-w-lg">
            <div class="flex flex-col gap-y-2">
                <h1 class="text-4xl text-left font-semibold">Cadastrar Mercado</h1>
                <span class="font-light text-left text-gray-600">Disponibilize um novo mercado de previsão.</span>
            </div>

            <UForm class="flex flex-col gap-y-4" @submit="onSubmit">
                <UFormField label="Título do Mercado" class="w-full" :ui="{ label: 'font-light' }" :error="formErrors.titulo">
                    <UInput
                        v-model="form.titulo"
                        placeholder="Ex: O Brasil será campeão da Copa de 2026?"
                        color="primary"
                        class="w-full"
                        size="xl"
                    />
                </UFormField>

                <UFormField label="Descrição" class="w-full" :ui="{ label: 'font-light' }" :error="formErrors.descricao">
                    <UTextarea
                        v-model="form.descricao"
                        placeholder="Descreva as condições deste mercado de previsão."
                        color="primary"
                        class="w-full"
                        size="xl"
                    />
                </UFormField>

                <div class="grid grid-cols-2 gap-x-4">
                    <UFormField label="Data de Encerramento" class="w-full" :ui="{ label: 'font-light' }" :error="formErrors.data_encerramento">
                        <UInput
                            v-model="form.data_encerramento"
                            type="date"
                            color="primary"
                            class="w-full"
                            size="xl"
                        />
                    </UFormField>

                    <UFormField label="Liquidez Inicial (b)" class="w-full" :ui="{ label: 'font-light' }" :error="formErrors.liquidez_inicial">
                        <UInput
                            v-model="form.liquidez_inicial"
                            type="number"
                            step="0.01"
                            placeholder="100.00"
                            color="primary"
                            class="w-full"
                            size="xl"
                        />
                    </UFormField>
                </div>

                <UFormField label="Regra de Encerramento" class="w-full" :ui="{ label: 'font-light' }" :error="formErrors.regra_encerramento">
                    <UInput
                        v-model="form.regra_encerramento"
                        placeholder="Ex: Verificação oficial do resultado no site da FIFA"
                        color="primary"
                        class="w-full"
                        size="xl"
                    />
                </UFormField>

                <div class="grid grid-cols-2 gap-x-4">
                    <UFormField label="Texto Opção Sucesso" class="w-full" :ui="{ label: 'font-light' }" :error="formErrors.opcao_sucesso">
                        <UInput
                            v-model="form.opcao_sucesso"
                            placeholder="Ex: Sim"
                            color="primary"
                            class="w-full"
                            size="xl"
                        />
                    </UFormField>

                    <UFormField label="Texto Opção Fracasso" class="w-full" :ui="{ label: 'font-light' }" :error="formErrors.opcao_fracasso">
                        <UInput
                            v-model="form.opcao_fracasso"
                            placeholder="Ex: Não"
                            color="primary"
                            class="w-full"
                            size="xl"
                        />
                    </UFormField>
                </div>

                <UFormField label="Link da Imagem" class="w-full" :ui="{ label: 'font-light' }" :error="formErrors.link_imagem">
                    <UInput
                        v-model="form.link_imagem"
                        placeholder="https://exemplo.com/imagem.png"
                        color="primary"
                        class="w-full"
                        size="xl"
                    />
                </UFormField>

                <UFormField label="Categorias" class="w-full" :ui="{ label: 'font-light' }" :error="formErrors.categorias">
                    <div class="flex flex-wrap gap-3 mt-1">
                        <label
                            v-for="cat in categoriaOptions"
                            :key="cat.id"
                            class="flex items-center gap-x-2 px-3 py-1.5 border rounded-lg text-sm cursor-pointer select-none"
                            :class="form.categorias.includes(cat.id) ? 'bg-primary-50 border-primary text-primary-700' : 'bg-white border-gray-200 text-gray-700'"
                        >
                            <input
                                type="checkbox"
                                :value="cat.id"
                                v-model="form.categorias"
                                class="hidden"
                            />
                            {{ cat.nome }}
                        </label>
                    </div>
                </UFormField>

                <UAlert
                    v-if="errorMessage"
                    color="error"
                    variant="subtle"
                    :title="errorMessage"
                    class="w-full"
                />

                <div class="flex justify-between w-full gap-x-4 mt-4">
                    <UButton
                        color="gray"
                        variant="ghost"
                        class="w-1/2 justify-center h-13"
                        size="xl"
                        @click="router.push('/mercados/home')"
                    >
                        Cancelar
                    </UButton>
                    <UButton
                        type="submit"
                        color="primary"
                        class="w-1/2 justify-center h-13"
                        size="xl"
                        :loading="isCreating"
                        :disabled="isCreating"
                    >
                        Cadastrar
                    </UButton>
                </div>
            </UForm>
        </div>
    </div>
</template>
