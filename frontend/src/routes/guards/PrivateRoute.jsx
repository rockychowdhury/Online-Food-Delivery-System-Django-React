import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const PrivateRoute = () => {
    const { user, loading } = useAuth();

    if (loading) {
        return <div>Loading...</div>; // Or a Spinner component
    }

    return user ? <Outlet /> : <Navigate to="/login" />;
};

export default PrivateRoute;
