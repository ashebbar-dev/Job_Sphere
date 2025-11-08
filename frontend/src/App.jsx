import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './components/LandingPage';
import Login from './components/Login';
import Register from './components/Register';
import StudentDashboard from './components/student/StudentDashboard';
import TPODashboard from './components/tpo/TPODashboard';
import HODDashboard from './components/hod/HODDashboard';

// Protected Route Component
const ProtectedRoute = ({ children, allowedRoles }) => {
  const token = localStorage.getItem('token');
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected Routes - Student */}
        <Route
          path="/student/dashboard"
          element={
            <ProtectedRoute allowedRoles={['student']}>
              <StudentDashboard />
            </ProtectedRoute>
          }
        />

        {/* Protected Routes - HOD */}
        <Route
          path="/hod/dashboard"
          element={
            <ProtectedRoute allowedRoles={['hod']}>
              <HODDashboard />
            </ProtectedRoute>
          }
        />

        {/* Protected Routes - TPO */}
        <Route
          path="/tpo/dashboard"
          element={
            <ProtectedRoute allowedRoles={['tpo']}>
              <TPODashboard />
            </ProtectedRoute>
          }
        />

        {/* Default Route */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
