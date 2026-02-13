import api from './api';
import { User } from '../types/User';

const userService = {
    getUsers: async (): Promise<User[]> => {
        const response = await api.get('/users');
        return response.data;
    },

    getUserById: async (userId: string): Promise<User> => {
        const response = await api.get(`/users/${userId}`);
        return response.data;
    },

    createUser: async (userData: Omit<User, 'id'>): Promise<User> => {
        const response = await api.post('/users', userData);
        return response.data;
    },

    updateUser: async (userId: string, userData: Partial<User>): Promise<User> => {
        const response = await api.put(`/users/${userId}`, userData);
        return response.data;
    },

    deleteUser: async (userId: string): Promise<void> => {
        await api.delete(`/users/${userId}`);
    }
};

export default userService;