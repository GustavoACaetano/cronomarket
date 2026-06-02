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
</script>

<template>
    <div class="h-screen w-screen flex items-center justify-center bg-linear-to-r to-primary from-secondary">
        <div class="flex flex-col gap-y-6 py-5 items-center rounded-md w-md bg-white/25 backdrop-blur-3xl shadow-lg shadow-white/40">
            <h1 class="text-2xl">Login</h1>
            <UForm class="flex flex-col gap-y-4">
                <UFormField label="Email">
                    <UInput placeholder="Seu email" color="secondary" trailing-icon="i-lucide-at-sign" v-model="email" />
                </UFormField>
                <UFormField label="Senha">
                    <UInput
                        v-model="password"
                        placeholder="Password"
                        color="secondary"
                        :type="show ? 'text' : 'password'"
                        :ui="{ trailing: 'pe-1' }"
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
                <span class="text-sm text-right">
                    Não tem conta? 
                    <UButton color="secondary" variant="link" @click="navigateTo('/cadastro')" :ui="{ base: 'px-0 py-0'}">
                        Cadastra-se
                    </UButton>
                </span>
                <div class="flex justify-end">
                    <UButton color="secondary">Entrar</UButton>
                </div>
            </UForm>
        </div>
    </div>
</template>