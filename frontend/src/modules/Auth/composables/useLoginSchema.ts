import { z } from 'zod';


export function useLoginSchema() {
    const loginSchema = z.object({
        email: z.string()
            .email('Insira um e-mail válido.')
            .nonempty('E-mail é obrigatório.'),
        password: z.string()
            .nonempty('A senha é obrigatória.'),
    })

    return { loginSchema }
}