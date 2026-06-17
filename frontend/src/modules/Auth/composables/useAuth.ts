import { useMutation } from '@tanstack/vue-query';
import { api } from '@/common/services/api';
import { getErrorMessage } from '@/common/utils/error';
import { ref } from 'vue';

export function useAuth() {
    const errorMsg = ref('');

    const ensureCsrfToken = async () => {
        await api.get('/api/csrf/');
    };

    const registerMutation = useMutation({
        mutationFn: async (dados: any) => {
            errorMsg.value = '';
            await ensureCsrfToken();
            const response = await api.post('/api/usuarios/', {
                dados_usuario: dados,
            });
            return response.data;
        },
        onError: (err: any) => {
            errorMsg.value = getErrorMessage(err, 'Não foi possível criar sua conta.');
        },
    });

    const loginMutation = useMutation({
        mutationFn: async (credentials: any) => {
            errorMsg.value = '';
            const response = await api.post('/api/login/', credentials);
            return response.data;
        },
        onError: (err: any) => {
            errorMsg.value = getErrorMessage(err, 'Email ou senha inválidos.');
        },
    });

    return {
        register: registerMutation.mutateAsync,
        isRegistering: registerMutation.isPending,
        isRegisterSuccess: registerMutation.isSuccess,
        
        login: loginMutation.mutateAsync,
        isLoggingIn: loginMutation.isPending,
        
        errorMessage: errorMsg,
    };
}
