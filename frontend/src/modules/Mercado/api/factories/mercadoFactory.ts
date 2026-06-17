import { CategoriaService } from "../services/categoria.service";
import { MercadoService } from "../services/mercado.service";

export class CategoriaFactory {
    private static instance: CategoriaService;

    static getService(): CategoriaService {
        if (!CategoriaFactory.instance) {
            CategoriaFactory.instance = new CategoriaService();
        }
        return CategoriaFactory.instance;
    }
}

export const categoriaService = CategoriaFactory.getService();

export class MercadoFactory {
    private static instance: MercadoService;

    static getService(): MercadoService {
        if (!MercadoFactory.instance) {
            MercadoFactory.instance = new MercadoService();
        }
        return MercadoFactory.instance;
    }
}

export const mercadoService = MercadoFactory.getService();