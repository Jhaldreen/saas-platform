import axios from 'axios';
import { Audit, AuditsListResponse, FindingsListResponse } from '../types';

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

export const auditService = {
  async upload(
    organizationId: string,
    auditType: string,
    file: File
  ): Promise<Audit> {
    const formData = new FormData();
    formData.append('organization_id', organizationId);
    formData.append('audit_type', auditType);
    formData.append('file', file);

    const token = localStorage.getItem('access_token');
    const response = await axios.post(
      `${API_URL}/audits/upload`,
      formData,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      }
    );
    return response.data;
  },

  async list(organizationId?: string): Promise<AuditsListResponse> {
    const params = organizationId ? { organization_id: organizationId } : {};
    const response = await axios.get(
      `${API_URL}/audits`,
      { ...getAuthHeaders(), params }
    );
    return response.data;
  },

  async getById(id: string): Promise<Audit> {
    const response = await axios.get(
      `${API_URL}/audits/${id}`,
      getAuthHeaders()
    );
    return response.data;
  },

  async getFindings(auditId: string): Promise<FindingsListResponse> {
    const response = await axios.get(
      `${API_URL}/audits/${auditId}/findings`,
      getAuthHeaders()
    );
    return response.data;
  }
};
