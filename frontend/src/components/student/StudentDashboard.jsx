import React, { useState, useEffect, useRef } from 'react';
import { studentAPI, aiAPI } from '../../services/api';
import ModernNavbar from '../common/ModernNavbar';
import ModernCard from '../common/ModernCard';
import ModernButton from '../common/ModernButton';
import Badge from '../common/Badge';
import JobAnalysisModal from './JobAnalysisModal';
import { Sparkles, Briefcase, Calendar, DollarSign, Upload, Check } from 'lucide-react';
import { motion } from 'framer-motion';

const StudentDashboard = () => {
  const [user, setUser] = useState(JSON.parse(localStorage.getItem('user') || '{}'));
  const [drives, setDrives] = useState([]);
  const [selectedDrive, setSelectedDrive] = useState(null);
  const [loading, setLoading] = useState(true);
  const [uploadingResume, setUploadingResume] = useState(false);
  const fileInputRef = useRef(null);

  useEffect(() => {
    loadDrives();
  }, []);

  const loadDrives = async () => {
    try {
      const response = await studentAPI.getAvailableDrives();
      setDrives(response.data);
    } catch (error) {
      console.error('Failed to load drives:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleResumeUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploadingResume(true);
    try {
      await studentAPI.uploadResume(file);
      alert('Resume uploaded successfully!');
    } catch (error) {
      alert('Failed to upload resume');
    } finally {
      setUploadingResume(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleApply = async (drive, analysis) => {
    try {
      await aiAPI.applyToDrive(drive.id, {
        match_score: analysis?.match_analysis?.overall_match_score,
        ats_score: analysis?.ats_analysis?.ats_score,
        skills_gap: analysis?.skills_gap,
        personalized_resume_path: analysis?.personalized_resume_pdf,
      });
      alert('Application submitted successfully!');
      setSelectedDrive(null);
      loadDrives();
    } catch (error) {
      alert('Failed to submit application');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <ModernNavbar user={user} />

      <div className="container mx-auto px-6 py-8">
        {/* Header with Resume Upload */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              Welcome, {user.name}
            </h1>
            <p className="text-gray-600">Discover AI-powered job opportunities</p>
          </div>
          <div>
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf"
              onChange={handleResumeUpload}
              className="hidden"
            />
            <ModernButton
              onClick={() => fileInputRef.current?.click()}
              loading={uploadingResume}
              icon={Upload}
              variant="secondary"
            >
              Upload Resume
            </ModernButton>
          </div>
        </div>

        {/* Drives Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {loading ? (
            <div className="col-span-full flex justify-center py-20">
              <div className="spinner" />
            </div>
          ) : drives.length === 0 ? (
            <div className="col-span-full text-center py-20">
              <p className="text-gray-500 text-lg">No placement drives available</p>
            </div>
          ) : (
            drives.map((drive, idx) => (
              <motion.div
                key={drive.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.1 }}
              >
                <ModernCard hover className="h-full">
                  <div className="flex flex-col h-full">
                    {/* Company Header */}
                    <div className="mb-4">
                      <h3 className="text-2xl font-bold text-gray-900 mb-1">
                        {drive.job_title}
                      </h3>
                      <p className="text-blue-600 font-semibold">{drive.company_name}</p>
                    </div>

                    {/* Details */}
                    <div className="space-y-3 mb-4 flex-grow">
                      <div className="flex items-center gap-2 text-gray-600">
                        <DollarSign size={18} className="text-green-600" />
                        <span className="font-medium">{drive.ctc || 'Not specified'}</span>
                      </div>
                      <div className="flex items-center gap-2 text-gray-600">
                        <Briefcase size={18} className="text-purple-600" />
                        <span>{drive.location || 'Multiple locations'}</span>
                      </div>
                      {drive.drive_date && (
                        <div className="flex items-center gap-2 text-gray-600">
                          <Calendar size={18} className="text-orange-600" />
                          <span>{new Date(drive.drive_date).toLocaleDateString()}</span>
                        </div>
                      )}
                    </div>

                    {/* Status Badge */}
                    <div className="mb-4">
                      <Badge variant={drive.status === 'active' ? 'success' : 'warning'} pulse>
                        {drive.status}
                      </Badge>
                    </div>

                    {/* Action Button */}
                    <ModernButton
                      onClick={() => setSelectedDrive(drive)}
                      variant="primary"
                      icon={Sparkles}
                      className="w-full"
                    >
                      Analyze Fit with AI
                    </ModernButton>
                  </div>
                </ModernCard>
              </motion.div>
            ))
          )}
        </div>
      </div>

      {/* Job Analysis Modal */}
      {selectedDrive && (
        <JobAnalysisModal
          drive={selectedDrive}
          onClose={() => setSelectedDrive(null)}
          onApply={(analysis) => handleApply(selectedDrive, analysis)}
        />
      )}
    </div>
  );
};

export default StudentDashboard;
