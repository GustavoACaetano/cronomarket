<script lang="ts" setup>
import { ref, computed } from 'vue';
import { getCookie } from '@/common/utils/cookie';
import { useRouter } from 'vue-router';

const router = useRouter();
const csrfToken = getCookie('csrftoken');
const logado = ref(false);

if (csrfToken) {
    logado.value = true
}

const userMenuItems = computed(() => [
  [
    {
      label: 'Meu Perfil',
      icon: 'i-lucide-id-card',
      onSelect: () => {
        void router.push({
          name: 'minhas-informacoes',
        });
      },
    },
    {
      label: 'Acessar Carteira',
      icon: 'i-lucide-wallet',
    },
    {
      label: 'Sair',
      icon: 'i-lucide-log-out',
      color: 'error',
    },
  ],
]);
</script>

<template>
    <UHeader :ui="{ container: 'm-0 justify-between w-full max-w-full'}">
        <template #title>
            <img src="/Cronomarket.png" class="w-50">
        </template>
        
        <template #right>
            <div v-if="logado">
                <UDropdownMenu
                    :items="userMenuItems"
                    size="sm"
                    :content="{ align: 'end', sideOffset: 8 }"
                    :ui="{ content: 'w-44' }"
                    >
                    <UButton
                        icon="i-lucide-user"
                        variant="ghost"
                        color="neutral"
                        class="rounded-full"
                    />
                </UDropdownMenu>
            </div>
            <div v-else>
                <UButton color="primary" variant="outline" @click="$router.push('/login')">Login</UButton>
                <UButton color="primary" @click="$router.push('/cadastro')">Cadastro</UButton>
            </div>
        </template>
    </UHeader>
</template>