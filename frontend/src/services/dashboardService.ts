import axios from 'axios';
import { DashboardMetrics } from '../types';

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

export const dashboardService = {
  async getMetrics(organizationId: string): Promise<DashboardMetrics> {
    const response = await axios.get(
      `${API_URL}/dashboard/metrics`,
      { ...getAuthHeaders(), params: { organization_id: organizationId } }
    );
    return response.data;
  }
};
