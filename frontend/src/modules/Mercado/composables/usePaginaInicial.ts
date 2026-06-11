import { useGetCategoria } from "./useGetCategoria";
import { ref, computed, shallowReactive } from "vue";
import { useDebounceFn } from "@vueuse/core";
import type { FiltroSection, FiltrosMercado } from "../api/types/index";
import { useGetMercado } from "./useGetMercado";


export function usePaginaInicial() {
    const { data: categorias } = useGetCategoria();
    
    const filtroSelecionado: FiltrosMercado = shallowReactive({
        search: '',
        categoria: [],
        data: null
    })

    const onInput = useDebounceFn(() => {
        console.log(filtroSelecionado.search);
    }, 600)

    const categoriaItems = computed(() => {
        if (!categorias.value) return []
        return categorias.value.results.map((categoria) => ({
            label: categoria.nome,
            id: categoria.id
        }))
    })


    const filtroSection: FiltroSection = {
        filtroSelecionado, onInput, categoriaItems
    }   

    const { data: mercadosData } = useGetMercado(filtroSelecionado)

    const mercados = computed(() => {
        if (!mercadosData.value) return []
        return mercadosData.value.results
    })

    return {
        filtroSection,
        mercados,
    }
}