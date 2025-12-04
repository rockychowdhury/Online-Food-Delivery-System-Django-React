import { useEffect } from 'react';
import api from '../services/api';
import authService from '../services/authService';
import { useNavigate } from 'react-router-dom';

const useAxios = () => {
    const navigate = useNavigate();

    useEffect(() => {
        const requestIntercept = api.interceptors.request.use(
            (config) => {
                // You can add headers here if needed, but cookies are handled automatically
                return config;
            },
            (error) => Promise.reject(error)
        );

        const responseIntercept = api.interceptors.response.use(
            (response) => response,
            async (error) => {
                const prevRequest = error?.config;
                if (error?.response?.status === 401 && !prevRequest?.sent) {
                    prevRequest.sent = true;
                    try {
                        await authService.refreshToken();
                        return api(prevRequest);
                    } catch (refreshError) {
                        // Refresh failed, logout user
                        // We might want to trigger a logout action in context, 
                        // but for now redirecting is a safe fallback
                        // Ideally, this hook should consume AuthContext to call logout()
                        return Promise.reject(refreshError);
                    }
                }
                return Promise.reject(error);
            }
        );

        return () => {
            api.interceptors.request.eject(requestIntercept);
            api.interceptors.response.eject(responseIntercept);
        };
    }, [navigate]);

    return api;
};

export default useAxios;
