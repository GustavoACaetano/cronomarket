export const getErrorMessage = (error: any, defaultMessage = 'Ocorreu um erro inesperado.'): string => {
    if (!error) return defaultMessage;

    const apiError = error?.response?.data || error;

    if (typeof apiError === 'string') {
        return apiError;
    }

    if (Array.isArray(apiError)) {
        return getErrorMessage(apiError[0], defaultMessage);
    }

    if (typeof apiError === 'object') {
        const values = Object.values(apiError);
        if (values.length > 0) {
            return getErrorMessage(values[0], defaultMessage);
        }
    }

    return defaultMessage;
};
