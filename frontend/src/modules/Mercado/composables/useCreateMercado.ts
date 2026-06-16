import { useMutation, useQueryClient } from '@tanstack/vue-query';
import { mercadoService } from '../api/factories/mercadoFactory';
import { getErrorMessage } from '@/common/utils/error';
import { ref } from 'vue';

export function useCreateMercado() {
    const errorMsg = ref('');
    const queryClient = useQueryClient();

    const createMercadoMutation = useMutation({
        mutationFn: async (payload: any) => {
            errorMsg.value = '';
            return await mercadoService.createMercado(payload);
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['mercados'] });
        },
        onError: (err: any) => {
            errorMsg.value = getErrorMessage(err, 'Não foi possível cadastrar o mercado de previsão.');
        }
    });

    return {
        createMercado: createMercadoMutation.mutateAsync,
        isCreating: createMercadoMutation.isPending,
        errorMessage: errorMsg,
    };
}
