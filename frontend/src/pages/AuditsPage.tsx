import React, { useEffect, useState } from 'react';
import { auditService } from '../services/auditService';
import { organizationService } from '../services/organizationService';
import { Audit, Organization } from '../types';

const AuditsPage: React.FC = () => {
  const [audits, setAudits] = useState<Audit[]>([]);
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [selectedOrg, setSelectedOrg] = useState('');
  const [auditType, setAuditType] = useState('cloud');
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);

  useEffect(() => { loadData(); }, []);

  const loadData = async () => {
    try {
      const { organizations: orgs } = await organizationService.list();
      setOrganizations(orgs);
      if (orgs.length > 0) {
        const { audits } = await auditService.list();
        setAudits(audits);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async () => {
    if (!file || !selectedOrg) return;
    setUploading(true);
    try {
      await auditService.upload(selectedOrg, auditType, file);
      await loadData();
      setShowModal(false);
      setFile(null);
    } catch (err) {
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  const getStatusBadge = (status: string) => {
    const styles: Record<string, React.CSSProperties> = {
      completed: { background: '#d1fae5', color: '#065f46' },
      processing: { background: '#dbeafe', color: '#1e40af' },
      pending: { background: '#fef3c7', color: '#92400e' },
      failed: { background: '#fee2e2', color: '#991b1b' }
    };
    return <span style={{...s.badge, ...styles[status]}}>{status.toUpperCase()}</span>;
  };

  if (loading) return <div style={s.loading}><div style={s.spinner}></div></div>;

  return (
    <div style={s.container}>
      <div style={s.header}>
        <div>
          <h1 style={s.title}>Audits</h1>
          <p style={s.subtitle}>Upload and manage your audits</p>
        </div>
        <button style={s.btnPrimary} onClick={() => setShowModal(true)}>📤 Upload CSV</button>
      </div>

      {audits.length === 0 ? (
        <div style={s.empty}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" style={s.emptyIcon}>
            <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" strokeWidth="2"/>
          </svg>
          <h3>No audits yet</h3>
          <p style={{color: '#64748b'}}>Upload a CSV file to start auditing</p>
        </div>
      ) : (
        <div style={s.tableContainer}>
          <table style={s.table}>
            <thead>
              <tr>
                <th style={s.th}>File Name</th>
                <th style={s.th}>Type</th>
                <th style={s.th}>Status</th>
                <th style={s.th}>Score</th>
                <th style={s.th}>Created</th>
              </tr>
            </thead>
            <tbody>
              {audits.map(audit => (
                <tr key={audit.id} style={s.tr}>
                  <td style={s.td}>{audit.file_name}</td>
                  <td style={s.td}><span style={s.typeBadge}>{audit.audit_type}</span></td>
                  <td style={s.td}>{getStatusBadge(audit.status)}</td>
                  <td style={s.td}>{audit.optimization_score || 'N/A'}</td>
                  <td style={s.td}>{new Date(audit.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {showModal && (
        <div style={s.modalOverlay} onClick={() => setShowModal(false)}>
          <div style={s.modalContent} onClick={e => e.stopPropagation()}>
            <div style={s.modalHeader}>
              <h2 style={s.modalTitle}>Upload CSV Audit</h2>
              <button style={s.modalClose} onClick={() => setShowModal(false)}>×</button>
            </div>
            <div style={s.modalBody}>
              <div style={s.formGroup}>
                <label style={s.label}>Organization</label>
                <select style={s.select} value={selectedOrg} onChange={e => setSelectedOrg(e.target.value)}>
                  <option value="">Select organization</option>
                  {organizations.map(org => (
                    <option key={org.id} value={org.id}>{org.name}</option>
                  ))}
                </select>
              </div>
              <div style={s.formGroup}>
                <label style={s.label}>Audit Type</label>
                <select style={s.select} value={auditType} onChange={e => setAuditType(e.target.value)}>
                  <option value="cloud">Cloud Infrastructure</option>
                  <option value="hospitality">Hospitality</option>
                  <option value="business">Small Business</option>
                </select>
              </div>
              <div style={s.formGroup}>
                <label style={s.label}>CSV File</label>
                <input
                  type="file"
                  accept=".csv"
                  onChange={e => setFile(e.target.files?.[0] || null)}
                  style={s.fileInput}
                />
              </div>
            </div>
            <div style={s.modalFooter}>
              <button style={s.btnSecondary} onClick={() => setShowModal(false)}>Cancel</button>
              <button style={s.btnPrimary} onClick={handleUpload} disabled={uploading || !file || !selectedOrg}>
                {uploading ? 'Uploading...' : 'Upload'}
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
  btnPrimary: { padding: '0.75rem 1.5rem', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white', border: 'none', borderRadius: '12px', fontWeight: 600, cursor: 'pointer' },
  btnSecondary: { padding: '0.75rem 1.5rem', background: 'white', color: '#334155', border: '2px solid #e2e8f0', borderRadius: '12px', fontWeight: 600, cursor: 'pointer' },
  tableContainer: { background: 'white', borderRadius: '16px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', overflow: 'hidden' },
  table: { width: '100%', borderCollapse: 'collapse' },
  th: { padding: '1rem', textAlign: 'left', fontWeight: 600, color: '#64748b', fontSize: '0.875rem', textTransform: 'uppercase', background: '#f8fafc', borderBottom: '2px solid #e2e8f0' },
  tr: { borderBottom: '1px solid #e2e8f0', transition: 'background 0.2s' },
  td: { padding: '1rem', color: '#334155' },
  badge: { padding: '0.25rem 0.75rem', borderRadius: '9999px', fontSize: '0.75rem', fontWeight: 600 },
  typeBadge: { padding: '0.25rem 0.75rem', background: '#f1f5f9', color: '#334155', borderRadius: '9999px', fontSize: '0.75rem', fontWeight: 600 },
  empty: { textAlign: 'center', padding: '4rem 2rem' },
  emptyIcon: { width: '64px', height: '64px', color: '#cbd5e1', margin: '0 auto 1rem' },
  modalOverlay: { position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 },
  modalContent: { background: 'white', borderRadius: '24px', width: '90%', maxWidth: '500px', boxShadow: '0 20px 25px -5px rgba(0,0,0,0.1)' },
  modalHeader: { padding: '2rem', borderBottom: '1px solid #e2e8f0', display: 'flex', justifyContent: 'space-between', alignItems: 'center' },
  modalTitle: { fontSize: '1.5rem', fontWeight: 700 },
  modalClose: { width: '32px', height: '32px', borderRadius: '50%', border: 'none', background: '#f1f5f9', cursor: 'pointer', fontSize: '1.5rem' },
  modalBody: { padding: '2rem' },
  modalFooter: { padding: '1.5rem 2rem', borderTop: '1px solid #e2e8f0', display: 'flex', justifyContent: 'flex-end', gap: '1rem' },
  formGroup: { marginBottom: '1.5rem' },
  label: { display: 'block', fontWeight: 600, marginBottom: '0.5rem', color: '#334155' },
  select: { width: '100%', padding: '0.75rem 1rem', border: '2px solid #e2e8f0', borderRadius: '12px', fontSize: '1rem' },
  fileInput: { width: '100%', padding: '0.75rem 1rem', border: '2px solid #e2e8f0', borderRadius: '12px' },
  loading: { display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' },
  spinner: { width: '48px', height: '48px', border: '4px solid #e2e8f0', borderTopColor: '#667eea', borderRadius: '50%', animation: 'spin 0.8s linear infinite' }
};

export default AuditsPage;
