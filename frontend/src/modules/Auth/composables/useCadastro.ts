import { ref } from 'vue';
import { useCadastroForm } from './useCadastroForm';

export function useCadastro() {
    const showPassword = ref(false);
    const showConfirmPassword = ref(false);
    const { form, fields, errors } = useCadastroForm();

    return { showPassword, showConfirmPassword, form, fields, errors, handleSubmit: form.handleSubmit, meta: form.meta };
}