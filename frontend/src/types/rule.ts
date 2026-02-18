export interface Rule {
  id: string;
  organization_id: string;
  name: string;
  audit_type: 'cloud' | 'hospitality' | 'business';
  conditions: RuleConditions;
  severity: 'low' | 'medium' | 'high' | 'critical';
  is_active: boolean;
  description?: string;
  created_at: string;
  updated_at?: string;
}

export interface RuleConditions {
  field: string;
  operator: '>' | '<' | '>=' | '<=' | '==' | '!=';
  threshold: number | string;
}

export interface CreateRuleRequest {
  organization_id: string;
  name: string;
  audit_type: string;
  conditions: RuleConditions;
  severity: string;
  description?: string;
}

export interface UpdateRuleRequest {
  name?: string;
  conditions?: RuleConditions;
  severity?: string;
  is_active?: boolean;
  description?: string;
}

export interface RulesListResponse {
  rules: Rule[];
  total: number;
}
