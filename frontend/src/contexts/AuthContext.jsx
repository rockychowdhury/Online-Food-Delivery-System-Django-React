import React, { createContext, useState, useEffect, useContext } from 'react';
import authService from '../services/authService';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const initAuth = async () => {
            try {
                const userData = await authService.checkAuthStatus();
                setUser(userData.data); // Assuming API returns { success: true, data: user }
            } catch (error) {
                setUser(null);
            } finally {
                setLoading(false);
            }
        };

        initAuth();
    }, []);

    const login = async (credentials) => {
        const response = await authService.login(credentials);
        setUser(response.data); // Assuming login returns user data
        return response;
    };

    const register = async (userData) => {
        const response = await authService.register(userData);
        setUser(response.data);
        return response;
    };

    const logout = async () => {
        await authService.logout();
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, register, logout, loading }}>
            {!loading && children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
