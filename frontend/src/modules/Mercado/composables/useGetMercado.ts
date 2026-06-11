import { type ShallowReactive, computed } from 'vue';
import type { FiltrosMercado } from '../api/types/index';
import { useQuery } from '@tanstack/vue-query';
import { mercadoService } from '../api/factories/mercadoFactory';

const MERCADO_KEY = 'GET_MERCADO'

export function useGetMercado(filtros: ShallowReactive<FiltrosMercado>) {
  return useQuery({
    queryKey: computed(() => [
      MERCADO_KEY,
      filtros.search,
      ...filtros.categoria,
    ]),
    queryFn: async () => await mercadoService.getMercados(filtros),
  })
}