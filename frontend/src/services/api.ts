import axios from 'axios';

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

// ============ ORGANIZATIONS ============

export interface Organization {
  id: string;
  name: string;
  owner_id: string;
  created_at: string;
}

export const organizationsAPI = {
  async create(name: string): Promise<Organization> {
    const response = await axios.post(
      `${API_URL}/organizations`,
      { name },
      getAuthHeaders()
    );
    return response.data;
  },

  async list(): Promise<{ organizations: Organization[]; total: number }> {
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

// ============ AUDITS ============

export interface Audit {
  id: string;
  organization_id: string;
  audit_type: string;
  file_name: string;
  status: string;
  total_cost_or_revenue?: number;
  optimization_score?: number;
  created_at: string;
  created_by: string;
  completed_at?: string;
}

export interface Finding {
  id: string;
  audit_id: string;
  title: string;
  severity: string;
  cost_impact?: number;
  description?: string;
  recommendation?: string;
  created_at: string;
}

export const auditsAPI = {
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

  async list(organizationId?: string): Promise<{ audits: Audit[]; total: number }> {
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

  async getFindings(auditId: string): Promise<{ findings: Finding[]; total: number }> {
    const response = await axios.get(
      `${API_URL}/audits/${auditId}/findings`,
      getAuthHeaders()
    );
    return response.data;
  }
};

// ============ RULES ============

export interface Rule {
  id: string;
  organization_id: string;
  name: string;
  audit_type: string;
  conditions: any;
  severity: string;
  is_active: boolean;
  description?: string;
  created_at: string;
}

export const rulesAPI = {
  async create(data: {
    organization_id: string;
    name: string;
    audit_type: string;
    conditions: any;
    severity: string;
    description?: string;
  }): Promise<Rule> {
    const response = await axios.post(
      `${API_URL}/rules`,
      data,
      getAuthHeaders()
    );
    return response.data;
  },

  async list(organizationId: string): Promise<{ rules: Rule[]; total: number }> {
    const response = await axios.get(
      `${API_URL}/rules`,
      { ...getAuthHeaders(), params: { organization_id: organizationId } }
    );
    return response.data;
  },

  async update(id: string, data: Partial<Rule>): Promise<Rule> {
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

// ============ DASHBOARD ============

export interface DashboardMetrics {
  total_audits: number;
  completed_audits: number;
  total_findings: number;
  avg_optimization_score?: number;
  active_rules: number;
}

export const dashboardAPI = {
  async getMetrics(organizationId: string): Promise<DashboardMetrics> {
    const response = await axios.get(
      `${API_URL}/dashboard/metrics`,
      { ...getAuthHeaders(), params: { organization_id: organizationId } }
    );
    return response.data;
  }
};