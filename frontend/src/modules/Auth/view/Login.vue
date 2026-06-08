<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const navigateTo = (path: string) => {
    router.push(path);
};

const email = ref('');
const show = ref(false)
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')

const handleLogin = async () => {
    errorMessage.value = ''

    if (!email.value || !password.value) {
        errorMessage.value = 'Preencha email e senha.'
        return
    }

    loading.value = true

    try {
        const response = await fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({
                email: email.value,
                password: password.value,
            }),
        })

        const data = await response.json().catch(() => ({}))

        if (!response.ok) {
            errorMessage.value = data?.non_field_errors?.[0] || data?.detail || 'Email ou senha inválidos.'
            return
        }

        localStorage.setItem('cronomarket_user', JSON.stringify(data.user))
        router.push('/landing-page')
    } catch {
        errorMessage.value = 'Não foi possível conectar ao servidor.'
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="min-h-screen w-screen bg-white px-4 py-6 flex flex-col">
        <div class="flex justify-center">
            <img src="../../../../public/Cronomarket.png" class="w-50">
        </div>
        <div class="flex flex-1 items-center justify-center">
            <div class="flex flex-col gap-y-6 w-full max-w-md">
                <div class="flex flex-col gap-y-2">
                    <h1 class="text-4xl text-left">Login</h1>
                    <span class="font-light text-left text-gray-600">Bem vindo de volta!</span>
                </div>
                <UForm class="flex flex-col gap-y-4 items-center" @submit.prevent="handleLogin">
                    <UFormField label="Email" class="w-full" :ui="{ label: 'font-light' }">
                        <UInput 
                            placeholder="Seu email" 
                            color="primary" 
                            trailing-icon="i-lucide-at-sign" 
                            class="w-full" 
                            v-model="email" 
                            size="xl"
                            />
                    </UFormField>
                    <UFormField label="Senha" class="w-full" :ui="{ label: 'font-light' }">
                        <UInput
                            v-model="password"
                            placeholder="Password"
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
                        <UButton color="primary" variant="link" @click="navigateTo('/cadastro')" :ui="{ base: 'px-0 py-0 font-light' }">
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
                            :loading="loading"
                            :disabled="loading || !email || !password"
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
