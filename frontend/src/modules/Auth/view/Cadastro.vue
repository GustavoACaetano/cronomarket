<script setup lang="ts">
import { useRouter } from 'vue-router';
import { useAuth } from '../composables/useAuth';
import { useCadastro } from '../composables/useCadastro';

const router = useRouter();
const { register, isRegistering, isRegisterSuccess, errorMessage } = useAuth();
const { showPassword, showConfirmPassword, meta, fields, errors, handleSubmit } = useCadastro();


const handleCadastro = handleSubmit(async (values) => {
    try {
        await register({
            username: values.username,
            email: values.email,
            password: values.password,
        });
        setTimeout(() => router.push('/login'), 700);
    } catch {
        // O erro é tratado reativamente pelo useAuth
    }
});

const onSubmit = () => {
    handleCadastro();
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
                    <h1 class="text-4xl text-left">Cadastro</h1>
                    <span class="font-light text-left text-gray-600">Crie sua conta para começar.</span>
                </div>
                <UForm class="flex flex-col gap-y-4 items-center" @submit="onSubmit">
                    <UFormField label="Nome de usuário" class="w-full" :ui="{ label: 'font-light' }" :error="errors.username">
                        <UInput
                            v-model="fields.username.value.value"
                            placeholder="Seu usuário"
                            color="primary"
                            trailing-icon="i-lucide-user"
                            class="w-full"
                            size="xl"
                        />
                    </UFormField>
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
                    <UFormField label="Confirmar senha" class="w-full" :ui="{ label: 'font-light' }" :error="errors.confirmPassword">
                        <UInput
                            v-model="fields.confirmPassword.value.value"
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
                        v-if="errorMessage"
                        color="error"
                        variant="subtle"
                        :title="errorMessage"
                        class="w-full"
                    />
                    <UAlert
                        v-if="isRegisterSuccess"
                        color="success"
                        variant="subtle"
                        title="Conta criada com sucesso."
                        class="w-full"
                    />
                    <span class="text-sm text-center font-light">
                        Já tem conta?
                        <UButton color="primary" variant="link" @click="router.push('/login')" :ui="{ base: 'px-0 py-0 font-light' }">
                            Entrar
                        </UButton>
                    </span>
                    <div class="flex justify-center w-full">
                        <UButton
                            type="submit"
                            color="primary"
                            class="w-full"
                            size="xl"
                            :loading="isRegistering"
                            :disabled="isRegistering || !meta.valid"
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
