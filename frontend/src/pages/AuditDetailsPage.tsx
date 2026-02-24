import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { auditService } from '../services/auditService';
import { Audit, Finding } from '../types';

const AuditDetailsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [audit, setAudit] = useState<Audit | null>(null);
  const [findings, setFindings] = useState<Finding[]>([]);
  const [csvData, setCsvData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) loadData(id);
  }, [id]);

  const loadData = async (auditId: string) => {
    try {
      const auditData = await auditService.getById(auditId);
      setAudit(auditData);
      
      const { findings: findingsData } = await auditService.getFindings(auditId);
      setFindings(findingsData);
      
      // Simulamos leer el CSV parseado (en producción vendría del backend)
      // Por ahora parseamos desde evidence de findings
      if (findingsData.length > 0 && findingsData[0].evidence) {
        setCsvData([findingsData[0].evidence]); // Aquí deberías obtener todos los datos del CSV
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div style={s.loading}><div style={s.spinner}></div></div>;
  if (!audit) return <div style={s.container}><h2>Audit not found</h2></div>;

  // Análisis de datos
  const monthlyData = csvData.map(row => ({
    month: row.month,
    revenue: parseFloat(row.revenue || 0),
    expenses: parseFloat(row.expenses || 0),
    profit: parseFloat(row.revenue || 0) - parseFloat(row.expenses || 0),
    occupancy: parseFloat(row.occupancy_rate || 0)
  }));

  const expenseBreakdown = csvData.length > 0 ? [
    { name: 'Cleaning', value: parseFloat(csvData[0].cleaning_cost || 0) },
    { name: 'Maintenance', value: parseFloat(csvData[0].maintenance_cost || 0) },
    { name: 'Utilities', value: parseFloat(csvData[0].utilities_cost || 0) },
    { name: 'Marketing', value: parseFloat(csvData[0].marketing_cost || 0) },
    { name: 'Platform Fees', value: parseFloat(csvData[0].platform_fees || 0) },
    { name: 'Staff', value: parseFloat(csvData[0].staff_cost || 0) },
    { name: 'Supplies', value: parseFloat(csvData[0].supplies_cost || 0) }
  ] : [];

  const COLORS = ['#667eea', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#3b82f6', '#ec4899'];

  const bestMonth = monthlyData.reduce((max, m) => m.revenue > max.revenue ? m : max, monthlyData[0] || { month: 'N/A', revenue: 0 });
  const worstMonth = monthlyData.reduce((min, m) => m.revenue < min.revenue ? m : min, monthlyData[0] || { month: 'N/A', revenue: 0 });

  const totalRevenue = monthlyData.reduce((sum, m) => sum + m.revenue, 0);
  const totalExpenses = monthlyData.reduce((sum, m) => sum + m.expenses, 0);
  const totalProfit = totalRevenue - totalExpenses;
  const profitMargin = totalRevenue > 0 ? ((totalProfit / totalRevenue) * 100).toFixed(1) : '0';

  return (
    <div style={s.container}>
      {/* Header */}
      <div style={s.header}>
        <button style={s.backBtn} onClick={() => navigate('/audits')}>← Back to Audits</button>
        <div>
          <h1 style={s.title}>{audit.file_name}</h1>
          <p style={s.subtitle}>Uploaded {new Date(audit.created_at).toLocaleDateString()}</p>
        </div>
      </div>

      {/* KPIs */}
      <div style={s.kpiGrid}>
        <div style={{...s.kpiCard, borderLeft: '4px solid #667eea'}}>
          <p style={s.kpiLabel}>Total Revenue</p>
          <p style={s.kpiValue}>€{totalRevenue.toLocaleString()}</p>
        </div>
        <div style={{...s.kpiCard, borderLeft: '4px solid #ef4444'}}>
          <p style={s.kpiLabel}>Total Expenses</p>
          <p style={s.kpiValue}>€{totalExpenses.toLocaleString()}</p>
        </div>
        <div style={{...s.kpiCard, borderLeft: '4px solid #10b981'}}>
          <p style={s.kpiLabel}>Net Profit</p>
          <p style={s.kpiValue}>€{totalProfit.toLocaleString()}</p>
        </div>
        <div style={{...s.kpiCard, borderLeft: '4px solid #f59e0b'}}>
          <p style={s.kpiLabel}>Profit Margin</p>
          <p style={s.kpiValue}>{profitMargin}%</p>
        </div>
      </div>

      {/* Charts Row 1 */}
      <div style={s.chartsGrid}>
        <div style={s.chartCard}>
          <h3 style={s.chartTitle}>Revenue vs Expenses Over Time</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={monthlyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="revenue" stroke="#667eea" strokeWidth={2} name="Revenue" />
              <Line type="monotone" dataKey="expenses" stroke="#ef4444" strokeWidth={2} name="Expenses" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div style={s.chartCard}>
          <h3 style={s.chartTitle}>Monthly Profit</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={monthlyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="profit" fill="#10b981" name="Profit" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Charts Row 2 */}
      <div style={s.chartsGrid}>
        <div style={s.chartCard}>
          <h3 style={s.chartTitle}>Expense Breakdown</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={expenseBreakdown}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({name, percent}) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {expenseBreakdown.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div style={s.chartCard}>
          <h3 style={s.chartTitle}>Occupancy Rate Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={monthlyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="occupancy" stroke="#8b5cf6" strokeWidth={2} name="Occupancy %" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Insights */}
      <div style={s.insightsGrid}>
        <div style={s.insightCard}>
          <h4 style={s.insightTitle}>🏆 Best Month</h4>
          <p style={s.insightMonth}>{bestMonth.month}</p>
          <p style={s.insightValue}>€{bestMonth.revenue.toLocaleString()}</p>
        </div>
        <div style={s.insightCard}>
          <h4 style={s.insightTitle}>📉 Worst Month</h4>
          <p style={s.insightMonth}>{worstMonth.month}</p>
          <p style={s.insightValue}>€{worstMonth.revenue.toLocaleString()}</p>
        </div>
        <div style={s.insightCard}>
          <h4 style={s.insightTitle}>💰 Avg Monthly Revenue</h4>
          <p style={s.insightValue}>€{(totalRevenue / monthlyData.length).toLocaleString()}</p>
        </div>
        <div style={s.insightCard}>
          <h4 style={s.insightTitle}>⚠️ Total Findings</h4>
          <p style={s.insightValue}>{findings.length}</p>
        </div>
      </div>

      {/* Findings Table */}
      {findings.length > 0 && (
        <div style={s.section}>
          <h3 style={s.sectionTitle}>Issues Found ({findings.length})</h3>
          <div style={s.tableContainer}>
            <table style={s.table}>
              <thead>
                <tr>
                  <th style={s.th}>Issue</th>
                  <th style={s.th}>Severity</th>
                  <th style={s.th}>Description</th>
                  <th style={s.th}>Recommendation</th>
                </tr>
              </thead>
              <tbody>
                {findings.map(finding => (
                  <tr key={finding.id} style={s.tr}>
                    <td style={s.td}>{finding.title}</td>
                    <td style={s.td}>
                      <span style={{...s.badge, background: getSeverityColor(finding.severity)}}>
                        {finding.severity}
                      </span>
                    </td>
                    <td style={s.td}>{finding.description}</td>
                    <td style={s.td}>{finding.recommendation}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

const getSeverityColor = (severity: string) => {
  const colors: Record<string, string> = {
    low: '#10b981',
    medium: '#f59e0b',
    high: '#ef4444',
    critical: '#7c3aed'
  };
  return colors[severity] || '#64748b';
};

const s: Record<string, React.CSSProperties> = {
  container: { maxWidth: '1400px', margin: '0 auto', padding: '2rem' },
  header: { marginBottom: '2rem' },
  backBtn: { padding: '0.5rem 1rem', background: '#f1f5f9', border: 'none', borderRadius: '8px', cursor: 'pointer', marginBottom: '1rem' },
  title: { fontSize: '2rem', fontWeight: 700, marginBottom: '0.5rem' },
  subtitle: { color: '#64748b' },
  kpiGrid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem', marginBottom: '2rem' },
  kpiCard: { background: 'white', padding: '1.5rem', borderRadius: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' },
  kpiLabel: { color: '#64748b', fontSize: '0.875rem', marginBottom: '0.5rem' },
  kpiValue: { fontSize: '2rem', fontWeight: 700 },
  chartsGrid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))', gap: '1.5rem', marginBottom: '2rem' },
  chartCard: { background: 'white', padding: '1.5rem', borderRadius: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' },
  chartTitle: { fontSize: '1.125rem', fontWeight: 600, marginBottom: '1rem' },
  insightsGrid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '2rem' },
  insightCard: { background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white', padding: '1.5rem', borderRadius: '12px', textAlign: 'center' },
  insightTitle: { fontSize: '0.875rem', marginBottom: '0.5rem', opacity: 0.9 },
  insightMonth: { fontSize: '1.125rem', fontWeight: 600, marginBottom: '0.25rem' },
  insightValue: { fontSize: '1.5rem', fontWeight: 700 },
  section: { background: 'white', padding: '2rem', borderRadius: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', marginBottom: '2rem' },
  sectionTitle: { fontSize: '1.25rem', fontWeight: 600, marginBottom: '1.5rem' },
  tableContainer: { overflowX: 'auto' },
  table: { width: '100%', borderCollapse: 'collapse' },
  th: { padding: '1rem', textAlign: 'left', fontWeight: 600, color: '#64748b', fontSize: '0.875rem', borderBottom: '2px solid #e2e8f0' },
  tr: { borderBottom: '1px solid #e2e8f0' },
  td: { padding: '1rem', color: '#334155' },
  badge: { padding: '0.25rem 0.75rem', borderRadius: '9999px', fontSize: '0.75rem', fontWeight: 600, color: 'white' },
  loading: { display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' },
  spinner: { width: '48px', height: '48px', border: '4px solid #e2e8f0', borderTopColor: '#667eea', borderRadius: '50%', animation: 'spin 0.8s linear infinite' }
};

export default AuditDetailsPage;
