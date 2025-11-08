import React, { useState, useEffect } from 'react';
import { hodAPI } from '../../services/api';
import ModernNavbar from '../common/ModernNavbar';
import ModernCard from '../common/ModernCard';
import ModernButton from '../common/ModernButton';
import StatCard from '../common/StatCard';
import { Users, CheckCircle, TrendingUp, Award } from 'lucide-react';

const HODDashboard = () => {
  const [user, setUser] = useState(JSON.parse(localStorage.getItem('user') || '{}'));
  const [pendingStudents, setPendingStudents] = useState([]);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [studentsRes, statsRes] = await Promise.all([
        hodAPI.getPendingStudents(),
        hodAPI.getStats(),
      ]);
      setPendingStudents(studentsRes.data);
      setStats(statsRes.data);
    } catch (error) {
      console.error('Failed to load data:', error);
    }
  };

  const handleApprove = async (studentId) => {
    try {
      await hodAPI.approveStudent(studentId);
      alert('Student approved successfully!');
      loadData();
    } catch (error) {
      alert('Failed to approve student');
    }
  };

  const statCards = stats ? [
    { icon: Users, label: 'Total Students', value: stats.total_students, color: 'blue' },
    { icon: CheckCircle, label: 'Approved', value: stats.approved_students, color: 'green' },
    { icon: Award, label: 'Placed', value: stats.placed_students, color: 'purple' },
    { icon: TrendingUp, label: 'Placement %', value: `${stats.placement_percentage}%`, color: 'orange' },
  ] : [];

  return (
    <div className="min-h-screen bg-gray-50">
      <ModernNavbar user={user} />

      <div className="container mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900">HOD Dashboard</h1>
          <p className="text-gray-600">Manage department students and placements</p>
        </div>

        {/* Stats */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {statCards.map((stat, idx) => (
              <StatCard key={idx} {...stat} />
            ))}
          </div>
        )}

        {/* Pending Approvals */}
        <div className="space-y-4">
          <h3 className="text-2xl font-bold">Pending Student Approvals</h3>
          {pendingStudents.length === 0 ? (
            <ModernCard>
              <p className="text-center text-gray-500 py-8">No pending approvals</p>
            </ModernCard>
          ) : (
            pendingStudents.map((student) => (
              <ModernCard key={student.id} hover>
                <div className="flex justify-between items-center">
                  <div>
                    <h4 className="text-xl font-bold">{student.name}</h4>
                    <p className="text-gray-600">{student.enrollment_no} • {student.department}</p>
                    <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
                      <span>CGPA: {student.cgpa}</span>
                      <span>{student.email}</span>
                      <span>{student.phone}</span>
                    </div>
                  </div>
                  <ModernButton
                    onClick={() => handleApprove(student.id)}
                    variant="success"
                    icon={CheckCircle}
                  >
                    Approve
                  </ModernButton>
                </div>
              </ModernCard>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default HODDashboard;
