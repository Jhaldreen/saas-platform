import React, { useEffect, useState } from 'react';
import { ruleService } from '../services/ruleService';
import { organizationService } from '../services/organizationService';
import { Rule, Organization } from '../types';

const RulesPage: React.FC = () => {
  const [rules, setRules] = useState<Rule[]>([]);
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    organization_id: '',
    name: '',
    audit_type: 'cloud',
    field: '',
    operator: '>',
    threshold: '',
    severity: 'medium',
    description: ''
  });

  useEffect(() => { loadData(); }, []);

  const loadData = async () => {
    try {
      const { organizations: orgs } = await organizationService.list();
      setOrganizations(orgs);
      if (orgs.length > 0) {
        const { rules } = await ruleService.list(orgs[0].id);
        setRules(rules);
        setFormData(prev => ({ ...prev, organization_id: orgs[0].id }));
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    if (!formData.name || !formData.field || !formData.threshold) return;
    try {
      await ruleService.create({
        organization_id: formData.organization_id,
        name: formData.name,
        audit_type: formData.audit_type,
        conditions: {
          field: formData.field,
          operator: formData.operator as any,
          threshold: parseFloat(formData.threshold)
        },
        severity: formData.severity,
        description: formData.description
      });
      await loadData();
      setShowModal(false);
      resetForm();
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Delete this rule?')) return;
    try {
      await ruleService.delete(id);
      await loadData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleToggle = async (rule: Rule) => {
    try {
      await ruleService.update(rule.id, { is_active: !rule.is_active });
      await loadData();
    } catch (err) {
      console.error(err);
    }
  };

  const resetForm = () => {
    setFormData({
      organization_id: organizations[0]?.id || '',
      name: '',
      audit_type: 'cloud',
      field: '',
      operator: '>',
      threshold: '',
      severity: 'medium',
      description: ''
    });
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

  if (loading) return <div style={s.loading}><div style={s.spinner}></div></div>;

  return (
    <div style={s.container}>
      <div style={s.header}>
        <div>
          <h1 style={s.title}>Rules</h1>
          <p style={s.subtitle}>Define audit rules and criteria</p>
        </div>
        <button style={s.btnPrimary} onClick={() => setShowModal(true)}>+ Create Rule</button>
      </div>

      {rules.length === 0 ? (
        <div style={s.empty}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" style={s.emptyIcon}>
            <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" strokeWidth="2"/>
          </svg>
          <h3>No rules yet</h3>
          <p style={{color: '#64748b'}}>Create rules to automatically detect issues in audits</p>
        </div>
      ) : (
        <div style={s.tableContainer}>
          <table style={s.table}>
            <thead>
              <tr>
                <th style={s.th}>Name</th>
                <th style={s.th}>Type</th>
                <th style={s.th}>Condition</th>
                <th style={s.th}>Severity</th>
                <th style={s.th}>Status</th>
                <th style={s.th}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {rules.map(rule => (
                <tr key={rule.id} style={s.tr}>
                  <td style={s.td}><strong>{rule.name}</strong></td>
                  <td style={s.td}><span style={s.typeBadge}>{rule.audit_type}</span></td>
                  <td style={s.td}>
                    <code style={s.code}>
                      {rule.conditions.field} {rule.conditions.operator} {rule.conditions.threshold}
                    </code>
                  </td>
                  <td style={s.td}>
                    <span style={{...s.badge, background: getSeverityColor(rule.severity), color: 'white'}}>
                      {rule.severity}
                    </span>
                  </td>
                  <td style={s.td}>
                    <button
                      style={{...s.toggleBtn, background: rule.is_active ? '#10b981' : '#94a3b8'}}
                      onClick={() => handleToggle(rule)}
                    >
                      {rule.is_active ? 'Active' : 'Inactive'}
                    </button>
                  </td>
                  <td style={s.td}>
                    <button style={s.deleteBtn} onClick={() => handleDelete(rule.id)}>Delete</button>
                  </td>
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
              <h2 style={s.modalTitle}>Create Rule</h2>
              <button style={s.modalClose} onClick={() => setShowModal(false)}>×</button>
            </div>
            <div style={s.modalBody}>
              <div style={s.formGroup}>
                <label style={s.label}>Rule Name</label>
                <input
                  style={s.input}
                  value={formData.name}
                  onChange={e => setFormData({...formData, name: e.target.value})}
                  placeholder="e.g., High Cost Alert"
                />
              </div>
              <div style={s.formGroup}>
                <label style={s.label}>Audit Type</label>
                <select style={s.select} value={formData.audit_type} onChange={e => setFormData({...formData, audit_type: e.target.value})}>
                  <option value="cloud">Cloud</option>
                  <option value="hospitality">Hospitality</option>
                  <option value="business">Business</option>
                </select>
              </div>
              <div style={s.formRow}>
                <div style={s.formGroup}>
                  <label style={s.label}>Field</label>
                  <input
                    style={s.input}
                    value={formData.field}
                    onChange={e => setFormData({...formData, field: e.target.value})}
                    placeholder="cost"
                  />
                </div>
                <div style={s.formGroup}>
                  <label style={s.label}>Operator</label>
                  <select style={s.select} value={formData.operator} onChange={e => setFormData({...formData, operator: e.target.value})}>
                    <option value=">">{'>'}</option>
                    <option value="<">{'<'}</option>
                    <option value=">=">{'>='}</option>
                    <option value="<=">{'<='}</option>
                    <option value="==">{'=='}</option>
                    <option value="!=">{'!='}</option>
                  </select>
                </div>
                <div style={s.formGroup}>
                  <label style={s.label}>Threshold</label>
                  <input
                    style={s.input}
                    type="number"
                    value={formData.threshold}
                    onChange={e => setFormData({...formData, threshold: e.target.value})}
                    placeholder="1000"
                  />
                </div>
              </div>
              <div style={s.formGroup}>
                <label style={s.label}>Severity</label>
                <select style={s.select} value={formData.severity} onChange={e => setFormData({...formData, severity: e.target.value})}>
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="critical">Critical</option>
                </select>
              </div>
              <div style={s.formGroup}>
                <label style={s.label}>Description (optional)</label>
                <textarea
                  style={s.textarea}
                  value={formData.description}
                  onChange={e => setFormData({...formData, description: e.target.value})}
                  placeholder="What does this rule check?"
                  rows={3}
                />
              </div>
            </div>
            <div style={s.modalFooter}>
              <button style={s.btnSecondary} onClick={() => setShowModal(false)}>Cancel</button>
              <button style={s.btnPrimary} onClick={handleCreate}>Create</button>
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
  tr: { borderBottom: '1px solid #e2e8f0' },
  td: { padding: '1rem', color: '#334155' },
  badge: { padding: '0.25rem 0.75rem', borderRadius: '9999px', fontSize: '0.75rem', fontWeight: 600 },
  typeBadge: { padding: '0.25rem 0.75rem', background: '#f1f5f9', color: '#334155', borderRadius: '9999px', fontSize: '0.75rem', fontWeight: 600 },
  code: { background: '#f1f5f9', padding: '0.25rem 0.5rem', borderRadius: '6px', fontSize: '0.875rem', fontFamily: 'monospace' },
  toggleBtn: { padding: '0.375rem 0.875rem', color: 'white', border: 'none', borderRadius: '9999px', fontSize: '0.75rem', fontWeight: 600, cursor: 'pointer' },
  deleteBtn: { padding: '0.375rem 0.875rem', background: '#fee2e2', color: '#991b1b', border: 'none', borderRadius: '8px', fontSize: '0.75rem', fontWeight: 600, cursor: 'pointer' },
  empty: { textAlign: 'center', padding: '4rem 2rem' },
  emptyIcon: { width: '64px', height: '64px', color: '#cbd5e1', margin: '0 auto 1rem' },
  modalOverlay: { position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 },
  modalContent: { background: 'white', borderRadius: '24px', width: '90%', maxWidth: '600px', maxHeight: '90vh', overflowY: 'auto', boxShadow: '0 20px 25px -5px rgba(0,0,0,0.1)' },
  modalHeader: { padding: '2rem', borderBottom: '1px solid #e2e8f0', display: 'flex', justifyContent: 'space-between', alignItems: 'center' },
  modalTitle: { fontSize: '1.5rem', fontWeight: 700 },
  modalClose: { width: '32px', height: '32px', borderRadius: '50%', border: 'none', background: '#f1f5f9', cursor: 'pointer', fontSize: '1.5rem' },
  modalBody: { padding: '2rem' },
  modalFooter: { padding: '1.5rem 2rem', borderTop: '1px solid #e2e8f0', display: 'flex', justifyContent: 'flex-end', gap: '1rem' },
  formGroup: { marginBottom: '1.5rem' },
  formRow: { display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem' },
  label: { display: 'block', fontWeight: 600, marginBottom: '0.5rem', color: '#334155', fontSize: '0.875rem' },
  input: { width: '100%', padding: '0.75rem 1rem', border: '2px solid #e2e8f0', borderRadius: '12px', fontSize: '1rem' },
  select: { width: '100%', padding: '0.75rem 1rem', border: '2px solid #e2e8f0', borderRadius: '12px', fontSize: '1rem' },
  textarea: { width: '100%', padding: '0.75rem 1rem', border: '2px solid #e2e8f0', borderRadius: '12px', fontSize: '1rem', fontFamily: 'inherit', resize: 'vertical' },
  loading: { display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' },
  spinner: { width: '48px', height: '48px', border: '4px solid #e2e8f0', borderTopColor: '#667eea', borderRadius: '50%', animation: 'spin 0.8s linear infinite' }
};

export default RulesPage;
