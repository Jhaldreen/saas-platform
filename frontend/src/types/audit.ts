export interface Audit {
  id: string;
  organization_id: string;
  audit_type: 'cloud' | 'hospitality' | 'business';
  file_name: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  total_cost_or_revenue?: number;
  optimization_score?: number;
  error_message?: string;
  created_at: string;
  created_by: string;
  completed_at?: string;
}

export interface Finding {
  id: string;
  audit_id: string;
  rule_id?: string;
  title: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  cost_impact?: number;
  description?: string;
  evidence?: any;
  recommendation?: string;
  created_at: string;
}

export interface AuditsListResponse {
  audits: Audit[];
  total: number;
}

export interface FindingsListResponse {
  findings: Finding[];
  total: number;
}
