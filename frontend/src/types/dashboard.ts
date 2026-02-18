export interface DashboardMetrics {
  total_audits: number;
  completed_audits: number;
  total_findings: number;
  avg_optimization_score?: number;
  active_rules: number;
}
