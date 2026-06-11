import { type Ref } from "vue";
import type { DateValue } from '@internationalized/date';

export type ApiResponse<T> = {
    count: number;
    next: string | null;
    previous: string | null;
    results: T[];
}


export type Categoria = {
    id: number;
    nome: string;
}

export type FiltroSection = {
    filtroSelecionado: FiltrosMercado;
    onInput: () => void;
    categoriaItems: Ref<{ label: string, id: number }[]>;
}

export type FiltrosMercado = {
    search: string;
    categoria: number[];
    data: DateValue | null;
}

export type Mercado = {
    id: string;
    titulo: string;
    descricao: string;
    data_encerramento: string;
    ativo: boolean;
    liquidez_inicial: string;
    valor_total_sucesso: string;
    valor_total_fracasso: string;
    regra_encerramento: string;
    opcao_sucesso: string;
    opcao_fracasso: string;
    link_imagem: string;
    categorias: number[];
}