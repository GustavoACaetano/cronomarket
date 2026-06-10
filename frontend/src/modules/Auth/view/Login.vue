<script setup lang="ts">
import { useRouter } from 'vue-router';
import { useAuth } from '../composables/useAuth';
import { useLogin } from '../composables/useLogin';

const toast = useToast();

const router = useRouter();
const { login, isLoggingIn, errorMessage } = useAuth();
const { show, fields, errors, meta, handleSubmit } = useLogin();

const handleLogin = handleSubmit(async (values) => {
    try {
        const data = await login({
            email: values.email,
            password: values.password,
        });
        localStorage.setItem('cronomarket_user', JSON.stringify(data.user));
        toast.add({
            title: 'Login bem-sucedido',
            color: 'success',
            duration: 5000,
        })
        router.push('/landing-page');
    } catch {
        // O erro é tratado reativamente pelo useAuth
    }
});

const onSubmit = () => {
    handleLogin();
};
</script>

<template>
    <div class="min-h-screen w-screen bg-white px-4 py-6 flex flex-col">
        <div class="flex justify-center">
            <img src="/Cronomarket.png" class="w-50">
        </div>
        <div class="flex flex-1 items-center justify-center">
            <div class="flex flex-col gap-y-6 w-full max-w-md">
                <div class="flex flex-col gap-y-2">
                    <h1 class="text-4xl text-left">Login</h1>
                    <span class="font-light text-left text-gray-600">Bem vindo de volta!</span>
                </div>
                <UForm class="flex flex-col gap-y-4 items-center" @submit="onSubmit">
                    <UFormField label="Email" class="w-full" :ui="{ label: 'font-light' }" :error="errors.email">
                        <UInput 
                            v-model="fields.email.value.value" 
                            placeholder="Seu email" 
                            color="primary" 
                            trailing-icon="i-lucide-at-sign" 
                            class="w-full" 
                            size="xl"
                        />
                    </UFormField>
                    <UFormField label="Senha" class="w-full" :ui="{ label: 'font-light' }" :error="errors.password">
                        <UInput
                            v-model="fields.password.value.value"
                            placeholder="Sua senha"
                            color="primary"
                            :type="show ? 'text' : 'password'"
                            :ui="{ trailing: 'pe-1' }"
                            size="xl"
                            class="w-full"
                        >
                            <template #trailing>
                                <UButton
                                    color="black"
                                    variant="link"
                                    size="lg"
                                    :icon="show ? 'i-lucide-eye-off' : 'i-lucide-eye'"
                                    :aria-label="show ? 'Hide password' : 'Show password'"
                                    :aria-pressed="show"
                                    aria-controls="password"
                                    @click="show = !show"
                                />
                            </template>
                        </UInput>
                    </UFormField>
                    <span class="text-sm text-center font-light">
                        Não tem conta? 
                        <UButton color="primary" variant="link" @click="router.push('/cadastro')" :ui="{ base: 'px-0 py-0 font-light' }">
                            Cadastre-se
                        </UButton>
                    </span>
                    <UAlert
                        v-if="errorMessage"
                        color="error"
                        variant="subtle"
                        :title="errorMessage"
                        class="w-full"
                    />
                    <div class="flex justify-center w-full">
                        <UButton
                            type="submit"
                            color="primary"
                            class="w-full"
                            size="xl"
                            :loading="isLoggingIn"
                            :disabled="isLoggingIn || !meta.valid"
                            :ui="{ base: 'flex justify-center h-13'}"
                        >
                            Entrar
                        </UButton>
                    </div>
                </UForm>
            </div>
        </div>
    </div>
</template>
