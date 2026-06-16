import type { FiltrosMercado, ApiResponse, Mercado } from "../types/index";
import { api } from "@/common/services/api";

export class MercadoService {

    public async getMercados(filters: FiltrosMercado): Promise<ApiResponse<Mercado>> {
        const response = await api.get('/api/mercados/', { params: buildPrestacaoQueryParams(filters) });
        return response.data
    }

    public async createMercado(payload: Partial<Mercado>): Promise<Mercado> {
        const response = await api.post('/api/mercados/', payload);
        return response.data;
    }
}

function buildPrestacaoQueryParams(filters: FiltrosMercado) {
    const params = new URLSearchParams()

    // if (filters.data) {
    //     params.append('data', filters.projetoId)
    // }

    if (filters.search) {
        params.append('search', filters.search)
    }

    if (Array.isArray(filters.categoria)) {
        filters.categoria.forEach((categoria) => {
            params.append('categoria', categoria.toString())
        })
    } 

    return params as unknown as Record<string, unknown>
}