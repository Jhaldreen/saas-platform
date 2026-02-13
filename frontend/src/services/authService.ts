import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1/auth'; // Adjust the URL as needed

export const login = async (email: string, password: string) => {
    const response = await axios.post(`${API_URL}/login`, { email, password });
    return response.data;
};

export const register = async (email: string, password: string) => {
    const response = await axios.post(`${API_URL}/register`, { email, password });
    return response.data;
};

export const logout = async () => {
    // Implement logout logic if needed
    localStorage.removeItem('token');
};