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

const userMenuItems = computed(() => {
  const items = [
    {
      label: `Olá, ${currentUser.value?.username || 'Usuário'}`,
      icon: 'i-lucide-user',
      disabled: true,
    },
    {
      label: 'Acessar Carteira',
      icon: 'i-lucide-wallet',
      onSelect: () => {
          void router.push('/mercados/carteira');
      }
    }
  ];

  // If the user profile contains usuario_id, check if they are admin from localStorage profile or state
  // Typically local storage might hold it, let's inject "Criar Mercado" if eh_admin is true
  if (currentUser.value?.eh_admin) {
      items.push({
          label: 'Criar Mercado',
          icon: 'i-lucide-plus-circle',
          onSelect: () => {
              void router.push('/mercados/criar');
          }
      } as any);
      items.push({
          label: 'Painel do Administrador',
          icon: 'i-lucide-layout-dashboard',
          onSelect: () => {
              void router.push('/mercados/admin-dashboard');
          }
      } as any);
  }

  // Sair action
  items.push({
      label: 'Sair',
      icon: 'i-lucide-log-out',
      color: 'error',
      onSelect: () => {
          localStorage.removeItem('cronomarket_user');
          document.cookie = 'sessionid=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
          window.location.href = '/login';
      }
  } as any);

  return [items];
});
</script>

<template>
    <UHeader :ui="{ container: 'm-0 justify-between w-full max-w-full'}">
        <template #title>
            <img src="/Cronomarket.png" class="w-32 md:w-50 cursor-pointer" @click="router.push('/mercados/home')">
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