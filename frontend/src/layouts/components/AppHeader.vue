<script lang="ts" setup>
import { ref, computed } from 'vue';
import { getCookie } from '@/common/utils/cookie';
import { useRouter } from 'vue-router';
import { getAvatarColor } from '@/common/utils/avatarColorHelper';

const router = useRouter();
const csrfToken = getCookie('csrftoken');
const logado = ref(false);

if (csrfToken) {
    logado.value = true
}

const currentUser = computed(() => {
    try {
        const raw = localStorage.getItem('cronomarket_user');
        return raw ? JSON.parse(raw) : null;
    } catch {
        return null;
    }
});

const userInitials = computed(() => {
    if (!currentUser.value || !currentUser.value.username) return 'U';
    return currentUser.value.username[0].toUpperCase();
});

const userAvatarBg = computed(() => {
    if (!currentUser.value || !currentUser.value.username) return '#10b981';
    return getAvatarColor(currentUser.value.username);
});

const userMenuItems = computed(() => [
  [
    {
      label: `Olá, ${currentUser.value?.username || 'Usuário'}`,
      icon: 'i-lucide-user',
      disabled: true,
    },
    {
      label: 'Acessar Carteira',
      icon: 'i-lucide-wallet',
    },
    {
      label: 'Sair',
      icon: 'i-lucide-log-out',
      color: 'error',
      onSelect: () => {
          localStorage.removeItem('cronomarket_user');
          // Clear cookies or credentials if applicable, then refresh
          document.cookie = 'sessionid=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
          window.location.href = '/login';
      }
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
                    <div 
                        class="w-9 h-9 rounded-full flex items-center justify-center text-white font-semibold uppercase cursor-pointer hover:opacity-90 transition-opacity border border-gray-100"
                        :style="{ backgroundColor: userAvatarBg }"
                    >
                        {{ userInitials }}
                    </div>
                </UDropdownMenu>
            </div>
            <div v-else>
                <UButton color="primary" variant="outline" @click="$router.push('/login')">Login</UButton>
                <UButton color="primary" @click="$router.push('/cadastro')">Cadastro</UButton>
            </div>
        </template>
    </UHeader>
</template>