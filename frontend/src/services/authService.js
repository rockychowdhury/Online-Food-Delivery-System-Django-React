import api from './api';

const authService = {
    login: async (credentials) => {
        const response = await api.post('/auth/login/', credentials);
        return response.data;
    },

    register: async (userData) => {
        const response = await api.post('/auth/register/', userData);
        return response.data;
    },

    logout: async () => {
        const response = await api.post('/auth/logout/');
        return response.data;
    },

    checkAuthStatus: async () => {
        const response = await api.get('/auth/users/me/');
        return response.data;
    },

    refreshToken: async () => {
        const response = await api.post('/auth/token/refresh/');
        return response.data;
    }
};

export default authService;
