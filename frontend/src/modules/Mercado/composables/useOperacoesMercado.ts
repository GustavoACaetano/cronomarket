import { useMutation, useQueryClient, useQuery } from '@tanstack/vue-query';
import { api } from '@/common/services/api';
import { getErrorMessage } from '@/common/utils/error';
import { ref } from 'vue';

const MERCADO_KEY = 'GET_MERCADO';

export function useOperacoesMercado(mercadoId: string) {
    const errorMsg = ref('');
    const queryClient = useQueryClient();

    // Fetch individual market details
    const getMercadoQuery = useQuery({
        queryKey: ['mercado-detalhe', mercadoId],
        queryFn: async () => {
            const response = await api.get(`/api/mercados/${mercadoId}/`);
            return response.data;
        },
        enabled: !!mercadoId,
    });

    // Fetch comments for the market
    const getComentariosQuery = useQuery({
        queryKey: ['mercado-comentarios', mercadoId],
        queryFn: async () => {
            const response = await api.get(`/api/comentarios/?mercado=${mercadoId}`);
            // Django REST Framework paginates comments, check for results
            return 'results' in response.data ? response.data.results : response.data;
        },
        enabled: !!mercadoId,
    });

    // Buy shares mutation
    const comprarMutation = useMutation({
        mutationFn: async ({ eh_sucesso, quantidade }: { eh_sucesso: boolean; quantidade: number }) => {
            errorMsg.value = '';
            const response = await api.post(`/api/mercados/${mercadoId}/comprar/`, {
                eh_sucesso,
                quantidade,
            });
            return response.data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['mercado-detalhe', mercadoId] });
            queryClient.invalidateQueries({ queryKey: [MERCADO_KEY] });
            queryClient.invalidateQueries({ queryKey: ['user-portfolio'] });
        },
        onError: (err: any) => {
            errorMsg.value = getErrorMessage(err, 'Falha ao processar a compra de ações.');
        },
    });

    // Sell shares mutation
    const venderMutation = useMutation({
        mutationFn: async ({ eh_sucesso, quantidade }: { eh_sucesso: boolean; quantidade: number }) => {
            errorMsg.value = '';
            const response = await api.post(`/api/mercados/${mercadoId}/vender/`, {
                eh_sucesso,
                quantidade,
            });
            return response.data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['mercado-detalhe', mercadoId] });
            queryClient.invalidateQueries({ queryKey: [MERCADO_KEY] });
            queryClient.invalidateQueries({ queryKey: ['user-portfolio'] });
        },
        onError: (err: any) => {
            errorMsg.value = getErrorMessage(err, 'Falha ao processar a venda de ações.');
        },
    });

    // Add comment mutation
    const adicionarComentarioMutation = useMutation({
        mutationFn: async (mensagem: string) => {
            errorMsg.value = '';
            const userDataRaw = localStorage.getItem('cronomarket_user');
            const user = userDataRaw ? JSON.parse(userDataRaw) : null;
            if (!user || !user.usuario_id) throw new Error('Usuário não autenticado.');

            const response = await api.post('/api/comentarios/', {
                mensagem,
                mercado: parseInt(mercadoId),
                usuario: user.usuario_id,
            });
            return response.data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['mercado-comentarios', mercadoId] });
        },
        onError: (err: any) => {
            errorMsg.value = getErrorMessage(err, 'Não foi possível enviar o comentário.');
        },
    });

    // End market mutation (Admin only)
    const encerrarMercadoMutation = useMutation({
        mutationFn: async (sucesso: boolean) => {
            errorMsg.value = '';
            const response = await api.post(`/api/mercados/${mercadoId}/encerrar/`, { sucesso });
            return response.data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['mercado-detalhe', mercadoId] });
            queryClient.invalidateQueries({ queryKey: [MERCADO_KEY] });
        },
        onError: (err: any) => {
            errorMsg.value = getErrorMessage(err, 'Erro ao encerrar o mercado de previsão.');
        },
    });

    return {
        mercado: getMercadoQuery.data,
        isLoadingMercado: getMercadoQuery.isLoading,
        comentarios: getComentariosQuery.data,
        isLoadingComentarios: getComentariosQuery.isLoading,

        comprar: comprarMutation.mutateAsync,
        isComprando: comprarMutation.isPending,

        vender: venderMutation.mutateAsync,
        isVendendo: venderMutation.isPending,

        adicionarComentario: adicionarComentarioMutation.mutateAsync,
        isEnviandoComentario: adicionarComentarioMutation.isPending,

        encerrarMercado: encerrarMercadoMutation.mutateAsync,
        isEncerrando: encerrarMercadoMutation.isPending,

        errorMessage: errorMsg,
    };
}
