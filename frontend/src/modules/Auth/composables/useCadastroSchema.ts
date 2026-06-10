import { z } from 'zod';

export function useCadastroSchema() {
    const cadastroSchema = z.object({
        username: z.string().min(3, 'O nome de usuário deve ter pelo menos 3 caracteres.')
            .nonempty('Nome de usuário é obrigatório.'),
        email: z.string().email('Insira um e-mail válido.')
            .nonempty('E-mail é obrigatório.'),
        password: z.string().min(6, 'A senha deve ter pelo menos 6 caracteres.')
            .nonempty('A senha é obrigatória.'),
        confirmPassword: z.string().nonempty('Confirme sua senha.'),
    }).refine((data) => data.password === data.confirmPassword, {
        message: 'As senhas não coincidem.',
        path: ['confirmPassword'],
    });
    
    
    return { cadastroSchema };
}

