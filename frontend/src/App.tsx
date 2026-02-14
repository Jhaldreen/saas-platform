import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import PrivateRoute from './components/Auth/PrivateRoute';
import Navbar from './components/Common/Navbar';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import OrganizationsPage from './pages/OrganizationsPage';
import AuditsPage from './pages/AuditsPage';
import RulesPage from './pages/RulesPage';
import SettingsPage from './pages/SettingsPage';

const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <div className="app">
          <Navbar />
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/" element={<PrivateRoute><DashboardPage /></PrivateRoute>} />
            <Route path="/organizations" element={<PrivateRoute><OrganizationsPage /></PrivateRoute>} />
            <Route path="/audits" element={<PrivateRoute><AuditsPage /></PrivateRoute>} />
            <Route path="/rules" element={<PrivateRoute><RulesPage /></PrivateRoute>} />
            <Route path="/settings" element={<PrivateRoute><SettingsPage /></PrivateRoute>} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
};

export default App;
