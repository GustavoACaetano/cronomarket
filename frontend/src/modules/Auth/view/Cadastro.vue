<script setup lang="ts">
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const navigateTo = (path: string) => {
    router.push(path);
};

const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const showPassword = ref(false);
const showConfirmPassword = ref(false);
const submitted = ref(false);
const loading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const passwordsDoNotMatch = computed(() => {
    return confirmPassword.value.length > 0 && password.value !== confirmPassword.value;
});

const isFormInvalid = computed(() => {
    return !username.value || !email.value || !password.value || !confirmPassword.value || passwordsDoNotMatch.value;
});

const getErrorMessage = (error: unknown): string => {
    if (typeof error === 'string') {
        return error;
    }

    if (Array.isArray(error)) {
        return getErrorMessage(error[0]);
    }

    if (error && typeof error === 'object') {
        const firstValue = Object.values(error)[0];
        return getErrorMessage(firstValue);
    }

    return 'Não foi possível criar sua conta.';
};

const getCookie = (name: string) => {
    const cookie = document.cookie
        .split('; ')
        .find((row) => row.startsWith(`${name}=`));

    return cookie ? decodeURIComponent(cookie.split('=')[1]) : '';
};

const handleCadastro = async () => {
    submitted.value = true;
    errorMessage.value = '';
    successMessage.value = '';

    if (isFormInvalid.value) {
        return;
    }

    loading.value = true;

    try {
        await fetch('/api/csrf/', {
            credentials: 'include',
        });

        const csrfToken = getCookie('csrftoken');

        const response = await fetch('/usuarios/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            credentials: 'include',
            body: JSON.stringify({
                dados_usuario: {
                    username: username.value,
                    email: email.value,
                    password: password.value,
                },
            }),
        });

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            errorMessage.value = getErrorMessage(data);
            return;
        }

        successMessage.value = 'Conta criada com sucesso.';
        setTimeout(() => navigateTo('/login'), 700);
    } catch {
        errorMessage.value = 'Não foi possível conectar ao servidor.';
    } finally {
        loading.value = false;
    }
};
</script>

<template>
    <div class="min-h-screen w-screen bg-white px-4 py-6 flex flex-col">
        <div class="flex justify-center">
            <img src="../../../../public/Cronomarket.png" class="w-50">
        </div>
        <div class="flex flex-1 items-center justify-center">
            <div class="flex flex-col gap-y-6 w-full max-w-md">
                <div class="flex flex-col gap-y-2">
                    <h1 class="text-4xl text-left">Cadastro</h1>
                    <span class="font-light text-left text-gray-600">Crie sua conta para começar.</span>
                </div>
                <UForm class="flex flex-col gap-y-4 items-center" @submit.prevent="handleCadastro">
                    <UFormField label="Nome de usuário" class="w-full" :ui="{ label: 'font-light' }">
                        <UInput
                            v-model="username"
                            placeholder="Seu usuário"
                            color="primary"
                            trailing-icon="i-lucide-user"
                            class="w-full"
                            size="xl"
                        />
                    </UFormField>
                    <UFormField label="Email" class="w-full" :ui="{ label: 'font-light' }">
                        <UInput
                            v-model="email"
                            placeholder="Seu email"
                            color="primary"
                            trailing-icon="i-lucide-at-sign"
                            class="w-full"
                            size="xl"
                        />
                    </UFormField>
                    <UFormField label="Senha" class="w-full" :ui="{ label: 'font-light' }">
                        <UInput
                            v-model="password"
                            placeholder="Sua senha"
                            color="primary"
                            :type="showPassword ? 'text' : 'password'"
                            :ui="{ trailing: 'pe-1' }"
                            size="xl"
                            class="w-full"
                        >
                            <template #trailing>
                                <UButton
                                    color="black"
                                    variant="link"
                                    size="lg"
                                    :icon="showPassword ? 'i-lucide-eye-off' : 'i-lucide-eye'"
                                    :aria-label="showPassword ? 'Ocultar senha' : 'Mostrar senha'"
                                    :aria-pressed="showPassword"
                                    aria-controls="password"
                                    @click="showPassword = !showPassword"
                                />
                            </template>
                        </UInput>
                    </UFormField>
                    <UFormField label="Confirmar senha" class="w-full" :ui="{ label: 'font-light' }">
                        <UInput
                            v-model="confirmPassword"
                            placeholder="Confirme sua senha"
                            color="primary"
                            :type="showConfirmPassword ? 'text' : 'password'"
                            :ui="{ trailing: 'pe-1' }"
                            size="xl"
                            class="w-full"
                        >
                            <template #trailing>
                                <UButton
                                    color="black"
                                    variant="link"
                                    size="lg"
                                    :icon="showConfirmPassword ? 'i-lucide-eye-off' : 'i-lucide-eye'"
                                    :aria-label="showConfirmPassword ? 'Ocultar confirmação de senha' : 'Mostrar confirmação de senha'"
                                    :aria-pressed="showConfirmPassword"
                                    aria-controls="confirm-password"
                                    @click="showConfirmPassword = !showConfirmPassword"
                                />
                            </template>
                        </UInput>
                    </UFormField>
                    <UAlert
                        v-if="passwordsDoNotMatch || (submitted && isFormInvalid)"
                        color="error"
                        variant="subtle"
                        :title="passwordsDoNotMatch ? 'As senhas não coincidem.' : 'Preencha todos os campos.'"
                        class="w-full"
                    />
                    <UAlert
                        v-if="errorMessage"
                        color="error"
                        variant="subtle"
                        :title="errorMessage"
                        class="w-full"
                    />
                    <UAlert
                        v-if="successMessage"
                        color="success"
                        variant="subtle"
                        :title="successMessage"
                        class="w-full"
                    />
                    <span class="text-sm text-center font-light">
                        Já tem conta?
                        <UButton color="primary" variant="link" @click="navigateTo('/login')" :ui="{ base: 'px-0 py-0 font-light' }">
                            Entrar
                        </UButton>
                    </span>
                    <div class="flex justify-center w-full">
                        <UButton
                            type="submit"
                            color="primary"
                            class="w-full"
                            size="xl"
                            :loading="loading"
                            :disabled="loading || isFormInvalid"
                            :ui="{ base: 'flex justify-center h-13'}"
                        >
                            Cadastrar
                        </UButton>
                    </div>
                </UForm>
            </div>
        </div>
    </div>
</template>
