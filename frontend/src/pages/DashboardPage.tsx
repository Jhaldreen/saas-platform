import React, { useEffect, useState } from 'react';
import { dashboardService } from '../services/dashboardService';
import { organizationService } from '../services/organizationService';
import { DashboardMetrics } from '../types';

const DashboardPage: React.FC = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const { organizations } = await organizationService.list();
      if (organizations.length > 0) {
        const data = await dashboardService.getMetrics(organizations[0].id);
        setMetrics(data);
      } else {
        setError('No organizations found. Create one first!');
      }
    } catch (err: any) {
      setError(err.message || 'Failed to load dashboard');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div style={s.loading}><div style={s.spinner}></div><p>Loading...</p></div>;
  if (error) return <div style={s.container}><div style={s.error}><h3>{error}</h3></div></div>;
  if (!metrics) return null;

  const cards = [
    { label: 'Total Audits', value: metrics.total_audits, color: '#667eea', icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2' },
    { label: 'Completed', value: metrics.completed_audits, color: '#10b981', icon: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' },
    { label: 'Findings', value: metrics.total_findings, color: '#f59e0b', icon: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z' },
    { label: 'Avg Score', value: metrics.avg_optimization_score?.toFixed(1) || 'N/A', color: '#3b82f6', icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z' }
  ];

  return (
    <div style={s.container}>
      <div style={s.header}>
        <h1 style={s.title}>Dashboard</h1>
        <p style={s.subtitle}>Overview of your cloud cost auditing</p>
      </div>
      <div style={s.grid}>
        {cards.map((card, i) => (
          <div key={i} style={{...s.card, borderLeft: `4px solid ${card.color}`}}>
            <div style={{...s.cardIcon, background: card.color}}>
              <svg viewBox="0 0 24 24" fill="none" stroke="white" style={s.icon}>
                <path d={card.icon} strokeWidth="2"/>
              </svg>
            </div>
            <div>
              <p style={s.cardLabel}>{card.label}</p>
              <p style={s.cardValue}>{card.value}</p>
            </div>
          </div>
        ))}
      </div>
      <div style={s.bottomCard}>
        <h3>Active Rules: {metrics.active_rules}</h3>
        <p style={{color: '#64748b', marginTop: '0.5rem'}}>Rules are automatically applied to every audit</p>
      </div>
    </div>
  );
};

const s: Record<string, React.CSSProperties> = {
  container: { maxWidth: '1400px', margin: '0 auto', padding: '3rem 2rem' },
  header: { marginBottom: '2.5rem' },
  title: { fontSize: '2.5rem', fontWeight: 700, fontFamily: 'Lexend, sans-serif', marginBottom: '0.5rem' },
  subtitle: { color: '#64748b', fontSize: '1.125rem' },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem', marginBottom: '2rem' },
  card: { background: 'white', borderRadius: '16px', padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1.5rem', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', transition: 'transform 0.2s', cursor: 'pointer' },
  cardIcon: { width: '64px', height: '64px', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 },
  icon: { width: '32px', height: '32px' },
  cardLabel: { color: '#64748b', fontSize: '0.875rem', fontWeight: 500, marginBottom: '0.25rem' },
  cardValue: { fontSize: '2rem', fontWeight: 700, color: '#0f172a' },
  bottomCard: { background: 'white', borderRadius: '16px', padding: '2rem', textAlign: 'center', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' },
  loading: { display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '60vh', color: '#64748b' },
  spinner: { width: '48px', height: '48px', border: '4px solid #e2e8f0', borderTopColor: '#667eea', borderRadius: '50%', animation: 'spin 0.8s linear infinite' },
  error: { textAlign: 'center', padding: '4rem 2rem', color: '#ef4444' }
};

export default DashboardPage;
