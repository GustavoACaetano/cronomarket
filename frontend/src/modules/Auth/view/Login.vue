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
                <UForm class="flex flex-col gap-y-4 items-center">
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
                    <div class="flex justify-center w-full">
                        <UButton color="primary" class="w-full" size="xl" :ui="{ base: 'flex justify-center h-13'}">Entrar</UButton>
                    </div>
                </UForm>
            </div>
        </div>
    </div>
</template>