import { useCadastroSchema } from "./useCadastroSchema";
import { useForm, useField } from "vee-validate";
import { toTypedSchema } from "@vee-validate/zod";

export function useCadastroForm() {
    const { cadastroSchema } = useCadastroSchema();

    const form = useForm({
        validationSchema: toTypedSchema(cadastroSchema),
    })

    const fields = {
        username: useField<string>('username'),
        email: useField<string>('email'),
        password: useField<string>('password'),
        confirmPassword: useField<string>('confirmPassword'),
    }

    return {
        form,
        fields,
        errors: form.errors,
    }
}