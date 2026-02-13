import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'http://localhost:8000/api/v1', // Adjust the base URL as needed
    headers: {
        'Content-Type': 'application/json',
    },
});

// Example API call to get tenants
export const getTenants = async () => {
    const response = await apiClient.get('/tenants');
    return response.data;
};

// Example API call to create a tenant
export const createTenant = async (tenantData) => {
    const response = await apiClient.post('/tenants', tenantData);
    return response.data;
};

// Example API call to get users
export const getUsers = async () => {
    const response = await apiClient.get('/users');
    return response.data;
};

// Example API call to create a user
export const createUser = async (userData) => {
    const response = await apiClient.post('/users', userData);
    return response.data;
};

// Add more API functions as needed

export default apiClient;