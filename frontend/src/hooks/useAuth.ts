import { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { login, logout, register } from '../services/authService';

const useAuth = () => {
    const { setAuthData } = useContext(AuthContext);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const checkAuthStatus = async () => {
            try {
                // Check if user is authenticated (implement your logic here)
                const userData = await fetchUserData();
                setAuthData(userData);
            } catch (err) {
                setError(err);
            } finally {
                setLoading(false);
            }
        };

        checkAuthStatus();
    }, [setAuthData]);

    const handleLogin = async (email, password) => {
        setLoading(true);
        try {
            const userData = await login(email, password);
            setAuthData(userData);
        } catch (err) {
            setError(err);
        } finally {
            setLoading(false);
        }
    };

    const handleRegister = async (email, password) => {
        setLoading(true);
        try {
            const userData = await register(email, password);
            setAuthData(userData);
        } catch (err) {
            setError(err);
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = async () => {
        setLoading(true);
        try {
            await logout();
            setAuthData(null);
        } catch (err) {
            setError(err);
        } finally {
            setLoading(false);
        }
    };

    return {
        loading,
        error,
        handleLogin,
        handleRegister,
        handleLogout,
    };
};

export default useAuth;