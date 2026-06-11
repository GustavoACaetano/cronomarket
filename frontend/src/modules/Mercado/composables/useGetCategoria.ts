import { useQuery } from "@tanstack/vue-query";
import { categoriaService } from "../api/factories/mercadoFactory";

export function useGetCategoria() {
    return useQuery({
        queryKey: ['categorias'],
        queryFn: async () => {
            return await categoriaService.getCategorias();
        }
    })
}