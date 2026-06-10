import { ref } from "vue";
import { useLoginForm } from "./useLoginForm";

export function useLogin() {
    const show = ref(false);
    const { form, fields, errors } = useLoginForm();
    
    return { show, form, fields, errors, handleSubmit: form.handleSubmit, meta: form.meta };
}