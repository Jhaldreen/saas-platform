import React, { useEffect, useState } from 'react';
import { organizationService } from '../services/organizationService';
import { Organization } from '../types';

const OrganizationsPage: React.FC = () => {
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [name, setName] = useState('');
  const [creating, setCreating] = useState(false);

  useEffect(() => { loadOrganizations(); }, []);

  const loadOrganizations = async () => {
    try {
      const { organizations } = await organizationService.list();
      setOrganizations(organizations);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    if (!name.trim()) return;
    setCreating(true);
    try {
      await organizationService.create({ name });
      await loadOrganizations();
      setShowModal(false);
      setName('');
    } catch (err) {
      console.error(err);
    } finally {
      setCreating(false);
    }
  };

  if (loading) return <div style={s.loading}><div style={s.spinner}></div></div>;

  return (
    <div style={s.container}>
      <div style={s.header}>
        <div>
          <h1 style={s.title}>Organizations</h1>
          <p style={s.subtitle}>Manage your organizations</p>
        </div>
        <button style={s.btnPrimary} onClick={() => setShowModal(true)}>+ Create Organization</button>
      </div>

      {organizations.length === 0 ? (
        <div style={s.empty}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" style={s.emptyIcon}>
            <path d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" strokeWidth="2"/>
          </svg>
          <h3>No organizations yet</h3>
          <p style={{color: '#64748b'}}>Create your first organization to get started</p>
        </div>
      ) : (
        <div style={s.grid}>
          {organizations.map(org => (
            <div key={org.id} style={s.card}>
              <div style={s.cardIcon}>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" strokeWidth="2"/>
                </svg>
              </div>
              <h3 style={s.cardTitle}>{org.name}</h3>
              <p style={s.cardDate}>Created {new Date(org.created_at).toLocaleDateString()}</p>
            </div>
          ))}
        </div>
      )}

      {showModal && (
        <div style={s.modalOverlay} onClick={() => setShowModal(false)}>
          <div style={s.modalContent} onClick={e => e.stopPropagation()}>
            <div style={s.modalHeader}>
              <h2 style={s.modalTitle}>Create Organization</h2>
              <button style={s.modalClose} onClick={() => setShowModal(false)}>×</button>
            </div>
            <div style={s.modalBody}>
              <label style={s.label}>Organization Name</label>
              <input
                style={s.input}
                value={name}
                onChange={e => setName(e.target.value)}
                placeholder="e.g., My Company"
                autoFocus
              />
            </div>
            <div style={s.modalFooter}>
              <button style={s.btnSecondary} onClick={() => setShowModal(false)}>Cancel</button>
              <button style={s.btnPrimary} onClick={handleCreate} disabled={creating || !name.trim()}>
                {creating ? 'Creating...' : 'Create'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const s: Record<string, React.CSSProperties> = {
  container: { maxWidth: '1400px', margin: '0 auto', padding: '3rem 2rem' },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2.5rem' },
  title: { fontSize: '2.5rem', fontWeight: 700, fontFamily: 'Lexend, sans-serif', marginBottom: '0.5rem' },
  subtitle: { color: '#64748b', fontSize: '1.125rem' },
  btnPrimary: { padding: '0.75rem 1.5rem', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white', border: 'none', borderRadius: '12px', fontWeight: 600, cursor: 'pointer', fontSize: '1rem' },
  btnSecondary: { padding: '0.75rem 1.5rem', background: 'white', color: '#334155', border: '2px solid #e2e8f0', borderRadius: '12px', fontWeight: 600, cursor: 'pointer', fontSize: '1rem' },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1.5rem' },
  card: { background: 'white', borderRadius: '16px', padding: '2rem', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', transition: 'transform 0.2s', cursor: 'pointer' },
  cardIcon: { width: '48px', height: '48px', background: '#f1f5f9', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1rem', color: '#667eea' },
  cardTitle: { fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.5rem' },
  cardDate: { color: '#64748b', fontSize: '0.875rem' },
  empty: { textAlign: 'center', padding: '4rem 2rem' },
  emptyIcon: { width: '64px', height: '64px', color: '#cbd5e1', margin: '0 auto 1rem' },
  modalOverlay: { position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 },
  modalContent: { background: 'white', borderRadius: '24px', width: '90%', maxWidth: '500px', boxShadow: '0 20px 25px -5px rgba(0,0,0,0.1)' },
  modalHeader: { padding: '2rem', borderBottom: '1px solid #e2e8f0', display: 'flex', justifyContent: 'space-between', alignItems: 'center' },
  modalTitle: { fontSize: '1.5rem', fontWeight: 700 },
  modalClose: { width: '32px', height: '32px', borderRadius: '50%', border: 'none', background: '#f1f5f9', cursor: 'pointer', fontSize: '1.5rem' },
  modalBody: { padding: '2rem' },
  modalFooter: { padding: '1.5rem 2rem', borderTop: '1px solid #e2e8f0', display: 'flex', justifyContent: 'flex-end', gap: '1rem' },
  label: { display: 'block', fontWeight: 600, marginBottom: '0.5rem', color: '#334155' },
  input: { width: '100%', padding: '0.75rem 1rem', border: '2px solid #e2e8f0', borderRadius: '12px', fontSize: '1rem' },
  loading: { display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' },
  spinner: { width: '48px', height: '48px', border: '4px solid #e2e8f0', borderTopColor: '#667eea', borderRadius: '50%', animation: 'spin 0.8s linear infinite' }
};

export default OrganizationsPage;
