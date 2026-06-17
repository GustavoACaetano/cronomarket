import { useLoginSchema } from "./useLoginSchema";
import { useForm, useField } from "vee-validate";
import { toTypedSchema } from "@vee-validate/zod";

export function useLoginForm() {
    const { loginSchema } = useLoginSchema();

    const form = useForm({
        validationSchema: toTypedSchema(loginSchema),
    })

    const fields = {
        email: useField<string>('email'),
        password: useField<string>('password'),
    }

    return {
        form,
        fields,
        errors: form.errors,
    }
}