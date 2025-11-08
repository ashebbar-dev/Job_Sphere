import React, { useState, useEffect } from 'react';
import { tpoAPI } from '../../services/api';
import ModernNavbar from '../common/ModernNavbar';
import ModernCard from '../common/ModernCard';
import ModernButton from '../common/ModernButton';
import StatCard from '../common/StatCard';
import { Briefcase, Building2, Users, TrendingUp, Plus } from 'lucide-react';

const TPODashboard = () => {
  const [user, setUser] = useState(JSON.parse(localStorage.getItem('user') || '{}'));
  const [drives, setDrives] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [showCreateDrive, setShowCreateDrive] = useState(false);
  const [showCreateCompany, setShowCreateCompany] = useState(false);
  const [newDrive, setNewDrive] = useState({
    company_id: '',
    job_title: '',
    job_description: '',
    ctc: '',
    location: '',
    drive_date: '',
  });
  const [newCompany, setNewCompany] = useState({
    name: '',
    website: '',
    industry: '',
    description: '',
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [drivesRes, companiesRes] = await Promise.all([
        tpoAPI.getDrives(),
        tpoAPI.getCompanies(),
      ]);
      setDrives(drivesRes.data);
      setCompanies(companiesRes.data);
    } catch (error) {
      console.error('Failed to load data:', error);
    }
  };

  const handleCreateCompany = async (e) => {
    e.preventDefault();
    try {
      await tpoAPI.createCompany(newCompany);
      alert('Company created successfully!');
      setShowCreateCompany(false);
      setNewCompany({ name: '', website: '', industry: '', description: '' });
      loadData();
    } catch (error) {
      alert('Failed to create company');
    }
  };

  const handleCreateDrive = async (e) => {
    e.preventDefault();
    try {
      await tpoAPI.createDrive(newDrive);
      alert('Drive created successfully!');
      setShowCreateDrive(false);
      setNewDrive({ company_id: '', job_title: '', job_description: '', ctc: '', location: '', drive_date: '' });
      loadData();
    } catch (error) {
      alert('Failed to create drive');
    }
  };

  const stats = [
    { icon: Briefcase, label: 'Active Drives', value: drives.filter(d => d.status === 'active').length, color: 'blue' },
    { icon: Building2, label: 'Companies', value: companies.length, color: 'purple' },
    { icon: Users, label: 'Total Applications', value: drives.reduce((sum, d) => sum + (d.applications_count || 0), 0), color: 'green' },
    { icon: TrendingUp, label: 'Completed Drives', value: drives.filter(d => d.status === 'completed').length, color: 'orange' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <ModernNavbar user={user} />

      <div className="container mx-auto px-6 py-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-gray-900">TPO Dashboard</h1>
            <p className="text-gray-600">Manage placement drives and companies</p>
          </div>
          <div className="flex gap-3">
            <ModernButton
              onClick={() => setShowCreateCompany(!showCreateCompany)}
              icon={Building2}
              variant="secondary"
            >
              Add Company
            </ModernButton>
            <ModernButton
              onClick={() => setShowCreateDrive(!showCreateDrive)}
              icon={Plus}
              variant="primary"
            >
              Create New Drive
            </ModernButton>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, idx) => (
            <StatCard key={idx} {...stat} />
          ))}
        </div>

        {/* Create Company Form */}
        {showCreateCompany && (
          <ModernCard className="mb-8">
            <h3 className="text-2xl font-bold mb-4">Add New Company</h3>
            <form onSubmit={handleCreateCompany} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Company Name *</label>
                  <input
                    type="text"
                    value={newCompany.name}
                    onChange={(e) => setNewCompany({ ...newCompany, name: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="e.g., Google"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Website</label>
                  <input
                    type="url"
                    value={newCompany.website}
                    onChange={(e) => setNewCompany({ ...newCompany, website: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="https://www.google.com"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Industry</label>
                  <input
                    type="text"
                    value={newCompany.industry}
                    onChange={(e) => setNewCompany({ ...newCompany, industry: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="e.g., Technology"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Description</label>
                  <input
                    type="text"
                    value={newCompany.description}
                    onChange={(e) => setNewCompany({ ...newCompany, description: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Brief description"
                  />
                </div>
              </div>
              <div className="flex gap-3">
                <ModernButton type="submit" variant="success">
                  Add Company
                </ModernButton>
                <ModernButton type="button" variant="ghost" onClick={() => setShowCreateCompany(false)}>
                  Cancel
                </ModernButton>
              </div>
            </form>
          </ModernCard>
        )}

        {/* Create Drive Form */}
        {showCreateDrive && (
          <ModernCard className="mb-8">
            <h3 className="text-2xl font-bold mb-4">Create New Drive</h3>
            <form onSubmit={handleCreateDrive} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Company *</label>
                  <select
                    value={newDrive.company_id}
                    onChange={(e) => setNewDrive({ ...newDrive, company_id: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  >
                    <option value="">Select Company</option>
                    {companies.map((c) => (
                      <option key={c.id} value={c.id}>{c.name}</option>
                    ))}
                  </select>
                  {companies.length === 0 && (
                    <p className="text-sm text-orange-600 mt-1">⚠️ Please add a company first!</p>
                  )}
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Job Title *</label>
                  <input
                    type="text"
                    value={newDrive.job_title}
                    onChange={(e) => setNewDrive({ ...newDrive, job_title: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="e.g., Software Engineer"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">CTC</label>
                  <input
                    type="text"
                    value={newDrive.ctc}
                    onChange={(e) => setNewDrive({ ...newDrive, ctc: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="e.g., 12 LPA"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Location</label>
                  <input
                    type="text"
                    value={newDrive.location}
                    onChange={(e) => setNewDrive({ ...newDrive, location: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="e.g., Bangalore"
                  />
                </div>
                <div className="col-span-2">
                  <label className="block text-sm font-medium mb-1">Job Description *</label>
                  <textarea
                    value={newDrive.job_description}
                    onChange={(e) => setNewDrive({ ...newDrive, job_description: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows={3}
                    placeholder="Full stack development role requiring React and Node.js..."
                    required
                  />
                </div>
              </div>
              <div className="flex gap-3">
                <ModernButton type="submit" variant="success">
                  Create Drive
                </ModernButton>
                <ModernButton type="button" variant="ghost" onClick={() => setShowCreateDrive(false)}>
                  Cancel
                </ModernButton>
              </div>
            </form>
          </ModernCard>
        )}

        {/* Drives List */}
        <div className="space-y-4">
          <h3 className="text-2xl font-bold">Recent Drives</h3>
          {drives.map((drive) => (
            <ModernCard key={drive.id} hover>
              <div className="flex justify-between items-start">
                <div>
                  <h4 className="text-xl font-bold">{drive.job_title}</h4>
                  <p className="text-gray-600">{drive.company_name}</p>
                  <p className="text-sm text-gray-500 mt-2">
                    {drive.applications_count} applications • {drive.status}
                  </p>
                </div>
                <div className="text-right">
                  <p className="font-bold text-green-600">{drive.ctc}</p>
                  <p className="text-sm text-gray-500">{drive.location}</p>
                </div>
              </div>
            </ModernCard>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TPODashboard;
