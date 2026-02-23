import React from 'react';
import { useAuth } from '../context/AuthContext';

const SettingsPage: React.FC = () => {
  const { user } = useAuth();

  return (
    <div style={s.container}>
      <div style={s.header}>
        <h1 style={s.title}>Settings</h1>
        <p style={s.subtitle}>Manage your account settings</p>
      </div>

      <div style={s.grid}>
        <div style={s.card}>
          <div style={s.cardHeader}>
            <h3 style={s.cardTitle}>Profile Information</h3>
          </div>
          <div style={s.cardBody}>
            <div style={s.field}>
              <label style={s.label}>Email</label>
              <p style={s.value}>{user?.email}</p>
            </div>
            <div style={s.field}>
              <label style={s.label}>Role</label>
              <p style={s.value}><span style={s.roleBadge}>{user?.role}</span></p>
            </div>
            <div style={s.field}>
              <label style={s.label}>Member Since</label>
              <p style={s.value}>{user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}</p>
            </div>
          </div>
        </div>

        <div style={s.card}>
          <div style={s.cardHeader}>
            <h3 style={s.cardTitle}>Security</h3>
          </div>
          <div style={s.cardBody}>
            <button style={s.btnSecondary}>Change Password</button>
            <p style={{color: '#64748b', fontSize: '0.875rem', marginTop: '1rem'}}>
              Update your password to keep your account secure
            </p>
          </div>
        </div>

        <div style={s.card}>
          <div style={s.cardHeader}>
            <h3 style={s.cardTitle}>Preferences</h3>
          </div>
          <div style={s.cardBody}>
            <div style={s.preference}>
              <div>
                <p style={{fontWeight: 600}}>Email Notifications</p>
                <p style={{color: '#64748b', fontSize: '0.875rem'}}>Receive email about audit completions</p>
              </div>
              <label style={s.switch}>
                <input type="checkbox" defaultChecked />
                <span style={s.slider}></span>
              </label>
            </div>
            <div style={s.preference}>
              <div>
                <p style={{fontWeight: 600}}>Weekly Reports</p>
                <p style={{color: '#64748b', fontSize: '0.875rem'}}>Get weekly summary of your audits</p>
              </div>
              <label style={s.switch}>
                <input type="checkbox" />
                <span style={s.slider}></span>
              </label>
            </div>
          </div>
        </div>

        <div style={s.card}>
          <div style={s.cardHeader}>
            <h3 style={s.cardTitle}>Danger Zone</h3>
          </div>
          <div style={s.cardBody}>
            <button style={s.btnDanger}>Delete Account</button>
            <p style={{color: '#64748b', fontSize: '0.875rem', marginTop: '1rem'}}>
              Once you delete your account, there is no going back
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

const s: Record<string, React.CSSProperties> = {
  container: { maxWidth: '1000px', margin: '0 auto', padding: '3rem 2rem' },
  header: { marginBottom: '2.5rem' },
  title: { fontSize: '2.5rem', fontWeight: 700, fontFamily: 'Lexend, sans-serif', marginBottom: '0.5rem' },
  subtitle: { color: '#64748b', fontSize: '1.125rem' },
  grid: { display: 'flex', flexDirection: 'column', gap: '1.5rem' },
  card: { background: 'white', borderRadius: '16px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' },
  cardHeader: { padding: '1.5rem', borderBottom: '1px solid #e2e8f0' },
  cardTitle: { fontSize: '1.125rem', fontWeight: 600 },
  cardBody: { padding: '1.5rem' },
  field: { marginBottom: '1.5rem' },
  label: { display: 'block', fontSize: '0.875rem', fontWeight: 600, color: '#64748b', marginBottom: '0.25rem' },
  value: { fontSize: '1rem', color: '#334155' },
  roleBadge: { padding: '0.25rem 0.75rem', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white', borderRadius: '9999px', fontSize: '0.75rem', fontWeight: 600, textTransform: 'uppercase' },
  btnSecondary: { padding: '0.75rem 1.5rem', background: 'white', color: '#334155', border: '2px solid #e2e8f0', borderRadius: '12px', fontWeight: 600, cursor: 'pointer', fontSize: '1rem' },
  btnDanger: { padding: '0.75rem 1.5rem', background: '#fee2e2', color: '#991b1b', border: 'none', borderRadius: '12px', fontWeight: 600, cursor: 'pointer', fontSize: '1rem' },
  preference: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem 0', borderBottom: '1px solid #e2e8f0' },
  switch: { position: 'relative', display: 'inline-block', width: '52px', height: '28px' },
  slider: { position: 'absolute', cursor: 'pointer', inset: 0, background: '#cbd5e1', borderRadius: '28px', transition: '0.4s' }
};

export default SettingsPage;
