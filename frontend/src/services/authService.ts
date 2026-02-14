import axios from 'axios';

const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: {
    id: string;
    email: string;
    role: string;
    created_at: string;
  };
}

export const login = async (email: string, password: string): Promise<LoginResponse> => {
  const response = await axios.post(`${API_URL}/auth/login`, { email, password });
  return response.data;
};

export const register = async (email: string, password: string, role: string = 'member'): Promise<LoginResponse> => {
  const response = await axios.post(`${API_URL}/auth/register`, { email, password, role });
  return response.data;
};

export const getCurrentUser = async (token: string) => {
  const response = await axios.get(`${API_URL}/auth/me`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  return response.data;
};

export const logout = async () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
};
