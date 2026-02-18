import axios from 'axios';
import { Rule, CreateRuleRequest, UpdateRuleRequest, RulesListResponse } from '../types';

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

export const ruleService = {
  async create(data: CreateRuleRequest): Promise<Rule> {
    const response = await axios.post(
      `${API_URL}/rules`,
      data,
      getAuthHeaders()
    );
    return response.data;
  },

  async list(organizationId: string): Promise<RulesListResponse> {
    const response = await axios.get(
      `${API_URL}/rules`,
      { ...getAuthHeaders(), params: { organization_id: organizationId } }
    );
    return response.data;
  },

  async update(id: string, data: UpdateRuleRequest): Promise<Rule> {
    const response = await axios.put(
      `${API_URL}/rules/${id}`,
      data,
      getAuthHeaders()
    );
    return response.data;
  },

  async delete(id: string): Promise<void> {
    await axios.delete(
      `${API_URL}/rules/${id}`,
      getAuthHeaders()
    );
  }
};
