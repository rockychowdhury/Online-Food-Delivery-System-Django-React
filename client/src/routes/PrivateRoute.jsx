import React from 'react';
import { Navigate, Outlet } from "react-router-dom";
// import useAuth from "../hooks/useAuth";
const PrivateRoute = () => {
    // const { isAuthenticated } = useAuth();
    const isloggedIn = localStorage.getItem("isLoggedIn");
    return isloggedIn ? <Outlet /> : <Navigate to="/login" />;
};

export default PrivateRoute;


