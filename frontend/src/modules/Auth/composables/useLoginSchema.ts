import { z } from 'zod';


export function useLoginSchema() {
    const loginSchema = z.object({
        email: z.string()
            .nonempty('Usuário ou E-mail é obrigatório.'),
        password: z.string()
            .nonempty('A senha é obrigatória.'),
    })

    return { loginSchema }
}