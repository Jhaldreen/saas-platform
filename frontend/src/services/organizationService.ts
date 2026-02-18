import axios from 'axios';
import { Organization, CreateOrganizationRequest, OrganizationsListResponse } from '../types';

const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  return {
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  };
};

export const organizationService = {
  async create(data: CreateOrganizationRequest): Promise<Organization> {
    const response = await axios.post(
      `${API_URL}/organizations`,
      data,
      getAuthHeaders()
    );
    return response.data;
  },

  async list(): Promise<OrganizationsListResponse> {
    const response = await axios.get(
      `${API_URL}/organizations`,
      getAuthHeaders()
    );
    return response.data;
  },

  async getById(id: string): Promise<Organization> {
    const response = await axios.get(
      `${API_URL}/organizations/${id}`,
      getAuthHeaders()
    );
    return response.data;
  }
};
