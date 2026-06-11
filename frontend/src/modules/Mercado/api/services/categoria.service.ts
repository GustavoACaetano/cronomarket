import { api } from "@/common/services/api"
import type { Categoria, ApiResponse } from "../types"

export class CategoriaService {
    public async getCategorias(): Promise<ApiResponse<Categoria>>{
        const response = await api.get('/api/categorias/');
        return response.data;
    }
}