import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import AppRoutes from './routes/AppRoutes';
import { AuthProvider } from './contexts/AuthContext';
import useAxios from './hooks/useAxios';

// Create a wrapper component to use the hook inside Router
const AppContent = () => {
  useAxios(); // Initialize interceptors
  return <AppRoutes />;
};

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </Router>
  );
}

export default App;
