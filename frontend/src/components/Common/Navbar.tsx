import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const Navbar: React.FC = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (!isAuthenticated) return null;

  const isActive = (path: string) => location.pathname === path;

  return (
    <nav style={styles.navbar}>
      <div style={styles.container}>
        <Link to="/" style={styles.brand}>
          <svg viewBox="0 0 24 24" fill="none" style={styles.logo}>
            <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" strokeWidth="2"/>
            <path d="M2 17L12 22L22 17" stroke="currentColor" strokeWidth="2"/>
            <path d="M2 12L12 17L22 12" stroke="currentColor" strokeWidth="2"/>
          </svg>
          <span>AI Cloud Auditor</span>
        </Link>

        <div style={styles.links}>
          <Link to="/" style={{...styles.link, ...(isActive('/') && styles.linkActive)}}>
            Dashboard
          </Link>
          <Link to="/organizations" style={{...styles.link, ...(isActive('/organizations') && styles.linkActive)}}>
            Organizations
          </Link>
          <Link to="/audits" style={{...styles.link, ...(isActive('/audits') && styles.linkActive)}}>
            Audits
          </Link>
          <Link to="/rules" style={{...styles.link, ...(isActive('/rules') && styles.linkActive)}}>
            Rules
          </Link>
          <Link to="/settings" style={{...styles.link, ...(isActive('/settings') && styles.linkActive)}}>
            Settings
          </Link>
        </div>

        <div style={styles.user}>
          <span style={styles.userEmail}>{user?.email}</span>
          <button onClick={handleLogout} style={styles.logoutBtn}>Logout</button>
        </div>
      </div>
    </nav>
  );
};

const styles: Record<string, React.CSSProperties> = {
  navbar: { background: 'white', borderBottom: '1px solid #e2e8f0', padding: '1rem 0', position: 'sticky', top: 0, zIndex: 100 },
  container: { maxWidth: '1400px', margin: '0 auto', padding: '0 2rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between' },
  brand: { display: 'flex', alignItems: 'center', gap: '0.75rem', fontFamily: 'Lexend, sans-serif', fontWeight: 700, fontSize: '1.25rem', color: '#0f172a', textDecoration: 'none' },
  logo: { width: '32px', height: '32px', color: '#667eea' },
  links: { display: 'flex', gap: '2rem' },
  link: { color: '#64748b', fontWeight: 500, textDecoration: 'none', transition: 'color 0.2s' },
  linkActive: { color: '#667eea' },
  user: { display: 'flex', alignItems: 'center', gap: '1rem' },
  userEmail: { color: '#334155', fontSize: '0.875rem' },
  logoutBtn: { padding: '0.5rem 1rem', background: '#f1f5f9', border: 'none', borderRadius: '8px', fontWeight: 500, cursor: 'pointer' }
};

export default Navbar;
