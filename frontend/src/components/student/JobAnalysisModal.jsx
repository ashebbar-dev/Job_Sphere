import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Sparkles, TrendingUp, Award, Target, BookOpen, FileText, Download, Check } from 'lucide-react';
import { aiAPI } from '../../services/api';
import CircularScore from '../common/CircularScore';
import ModernButton from '../common/ModernButton';
import Badge from '../common/Badge';
import ProgressBar from '../common/ProgressBar';
import ModernCard from '../common/ModernCard';

const JobAnalysisModal = ({ drive, onClose, onApply }) => {
  const [loading, setLoading] = useState(true);
  const [analysis, setAnalysis] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [downloadingResume, setDownloadingResume] = useState(false);

  useEffect(() => {
    loadAnalysis();
  }, []);

  const loadAnalysis = async () => {
    try {
      const response = await aiAPI.analyzeJobFit(drive.id);
      setAnalysis(response.data);
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
        <div className="glass p-12 rounded-3xl">
          <div className="flex flex-col items-center gap-4">
            <div className="spinner" />
            <p className="text-lg font-semibold text-gray-700">Analyzing with AI...</p>
            <p className="text-sm text-gray-500">Researching company & matching skills</p>
          </div>
        </div>
      </div>
    );
  }

  const tabs = [
    { id: 'overview', label: 'Overview', icon: Sparkles },
    { id: 'match', label: 'Match Analysis', icon: Target },
    { id: 'skills', label: 'Skills Gap', icon: TrendingUp },
    { id: 'resume', label: 'AI Resume', icon: FileText },
    { id: 'company', label: 'Company Intel', icon: Award },
  ];

  const handleDownloadResume = async () => {
    try {
      setDownloadingResume(true);
      const response = await aiAPI.downloadPersonalizedResume(drive.id);
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      const safeCompany = drive.company_name?.replace(/\s+/g, '_') || 'company';
      const safeRole = drive.job_title?.replace(/\s+/g, '_') || 'role';
      link.download = `AI-Resume-${safeCompany}-${safeRole}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Resume download failed:', error);
      alert('Could not download the personalized resume. Please try again.');
    } finally {
      setDownloadingResume(false);
    }
  };

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          onClick={(e) => e.stopPropagation()}
          className="bg-white rounded-3xl shadow-2xl max-w-6xl w-full max-h-[90vh] overflow-hidden"
        >
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-6 text-white">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h2 className="text-3xl font-bold mb-2">{drive.job_title}</h2>
                <p className="text-blue-100">{drive.company_name}</p>
              </div>
              <button
                onClick={onClose}
                className="p-2 hover:bg-white/20 rounded-xl transition-colors"
              >
                <X size={24} />
              </button>
            </div>

            {/* Score Overview */}
            <div className="grid grid-cols-3 gap-4">
              <div className="glass-dark p-4 rounded-xl text-center">
                <p className="text-sm opacity-90 mb-2">Match Score</p>
                <p className="text-4xl font-bold">{analysis?.match_analysis?.overall_match_score || 0}%</p>
              </div>
              <div className="glass-dark p-4 rounded-xl text-center">
                <p className="text-sm opacity-90 mb-2">ATS Score</p>
                <p className="text-4xl font-bold">{analysis?.ats_analysis?.ats_score || 0}%</p>
              </div>
              <div className="glass-dark p-4 rounded-xl text-center">
                <p className="text-sm opacity-90 mb-2">Readiness</p>
                <p className="text-xl font-bold">{analysis?.skills_gap?.overall_readiness || 'Good'}</p>
              </div>
            </div>
          </div>

          {/* Tabs */}
          <div className="border-b border-gray-200 px-6">
            <div className="flex gap-2">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-6 py-4 font-semibold transition-all ${
                    activeTab === tab.id
                      ? 'text-blue-600 border-b-2 border-blue-600'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  <tab.icon size={18} />
                  {tab.label}
                </button>
              ))}
            </div>
          </div>

          {/* Content */}
          <div className="p-6 overflow-y-auto max-h-[50vh]">
            {activeTab === 'overview' && (
              <div className="space-y-6">
                {/* Scores */}
                <div className="grid grid-cols-3 gap-6">
                  <CircularScore
                    score={analysis?.match_analysis?.overall_match_score || 0}
                    label="Overall Match"
                    size={140}
                  />
                  <CircularScore
                    score={analysis?.ats_analysis?.ats_score || 0}
                    label="ATS Compatibility"
                    size={140}
                  />
                  <CircularScore
                    score={analysis?.match_analysis?.skills_match?.score || 0}
                    label="Skills Match"
                    size={140}
                  />
                </div>

                {/* Key Strengths */}
                <div>
                  <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                    <Award className="text-green-600" />
                    Your Strengths
                  </h3>
                  <div className="grid grid-cols-2 gap-3">
                    {analysis?.match_analysis?.strengths?.map((strength, idx) => (
                      <motion.div
                        key={idx}
                        initial={{ x: -20, opacity: 0 }}
                        animate={{ x: 0, opacity: 1 }}
                        transition={{ delay: idx * 0.1 }}
                        className="flex items-start gap-2 bg-green-50 border border-green-200 p-3 rounded-xl"
                      >
                        <span className="text-green-600 text-xl">✓</span>
                        <span className="text-sm text-gray-700">{strength}</span>
                      </motion.div>
                    ))}
                  </div>
                </div>

                {/* Recommendation */}
                <div className="bg-gradient-to-r from-blue-50 to-purple-50 border-l-4 border-blue-600 p-6 rounded-xl">
                  <h4 className="font-bold text-lg mb-2">AI Recommendation</h4>
                  <p className="text-gray-700">{analysis?.match_analysis?.recommendation}</p>
                </div>
              </div>
            )}

            {activeTab === 'match' && (
              <div className="space-y-6">
                {/* Matching Skills */}
                <div>
                  <h3 className="text-xl font-bold mb-4 text-green-600">✓ Matching Skills</h3>
                  <div className="flex flex-wrap gap-2">
                    {analysis?.match_analysis?.skills_match?.matching_skills?.map((skill, idx) => (
                      <Badge key={idx} variant="success" size="lg">
                        {skill}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Missing Skills */}
                <div>
                  <h3 className="text-xl font-bold mb-4 text-orange-600">⚠ Missing Skills</h3>
                  <div className="flex flex-wrap gap-2">
                    {analysis?.match_analysis?.skills_match?.missing_skills?.map((skill, idx) => (
                      <Badge key={idx} variant="warning" size="lg">
                        {skill}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Score Breakdown */}
                <div className="space-y-4">
                  <ProgressBar
                    value={analysis?.match_analysis?.skills_match?.score || 0}
                    max={100}
                    label="Skills Match"
                    color="green"
                  />
                  <ProgressBar
                    value={analysis?.match_analysis?.experience_fit?.score || 0}
                    max={100}
                    label="Experience Fit"
                    color="blue"
                  />
                  <ProgressBar
                    value={analysis?.match_analysis?.cultural_fit?.score || 0}
                    max={100}
                    label="Cultural Alignment"
                    color="purple"
                  />
                </div>
              </div>
            )}

            {activeTab === 'skills' && (
              <div className="space-y-6">
                <div className="bg-gradient-to-r from-orange-50 to-red-50 border-l-4 border-orange-500 p-6 rounded-xl">
                  <h4 className="font-bold text-lg mb-2">Overall Readiness</h4>
                  <p className="text-2xl font-bold text-orange-600">
                    {analysis?.skills_gap?.overall_readiness}
                  </p>
                </div>

                {/* Critical Gaps */}
                <div>
                  <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                    <Target className="text-red-600" />
                    Skills to Acquire
                  </h3>
                  <div className="space-y-4">
                    {analysis?.skills_gap?.critical_gaps?.map((gap, idx) => (
                      <motion.div
                        key={idx}
                        initial={{ y: 20, opacity: 0 }}
                        animate={{ y: 0, opacity: 1 }}
                        transition={{ delay: idx * 0.1 }}
                        className="bg-white border-2 border-gray-200 rounded-xl p-5 hover:shadow-lg transition-all"
                      >
                        <div className="flex items-start justify-between mb-3">
                          <h4 className="font-bold text-lg">{gap.skill}</h4>
                          <Badge variant={gap.importance === 'Critical' ? 'danger' : 'warning'}>
                            {gap.importance}
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-600 mb-3">
                          <strong>Time to learn:</strong> {gap.estimated_time}
                        </p>
                        <div className="bg-blue-50 p-3 rounded-lg">
                          <p className="text-sm font-semibold mb-2">Learning Resources:</p>
                          <ul className="text-sm text-gray-700 space-y-1">
                            {gap.learning_resources?.map((resource, ridx) => (
                              <li key={ridx} className="flex items-center gap-2">
                                <BookOpen size={14} className="text-blue-600" />
                                {resource}
                              </li>
                            ))}
                          </ul>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </div>

                {/* Quick Wins */}
                <div className="bg-green-50 border-2 border-green-200 rounded-xl p-5">
                  <h4 className="font-bold mb-3 flex items-center gap-2">
                    <TrendingUp className="text-green-600" />
                    Quick Wins (Learn These Fast!)
                  </h4>
                  <ul className="space-y-2">
                    {analysis?.skills_gap?.quick_wins?.map((win, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-gray-700">
                        <span className="text-green-600 font-bold">→</span>
                        {win}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}

            {activeTab === 'resume' && (
              <div className="space-y-6">
                {!analysis?.personalized_content ? (
                  <div className="bg-blue-50 border border-blue-200 rounded-2xl p-6 text-center">
                    <p className="text-blue-700 font-semibold">
                      Generating personalized resume insights...
                    </p>
                    <p className="text-blue-500 text-sm mt-2">
                      Once ready, you’ll be able to review, download, and apply with the AI-tailored version.
                    </p>
                  </div>
                ) : (
                  <>
                    <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-6 text-white flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                      <div>
                        <p className="text-sm uppercase tracking-wide opacity-80">
                          Tailored Branding
                        </p>
                        <h3 className="text-2xl font-bold mt-2">
                          {analysis.personalized_content.branding_headline || `Tailored for ${drive.job_title}`}
                        </h3>
                        <p className="mt-3 text-blue-100 leading-relaxed">
                          {analysis.personalized_content.professional_summary || 'We are preparing a concise summary that mirrors the company voice.'}
                        </p>
                      </div>
                      <ModernButton
                        onClick={handleDownloadResume}
                        loading={downloadingResume}
                        icon={Download}
                        variant="ghost"
                        className="bg-white/20 hover:bg-white/30 text-white border border-white/40"
                        disabled={!analysis?.personalized_resume_pdf}
                      >
                        Download AI-Tailored Resume
                      </ModernButton>
                      {!analysis?.personalized_resume_pdf && (
                        <p className="text-xs text-blue-100">
                          Hang tight—your personalized PDF is finishing up.
                        </p>
                      )}
                    </div>

                    {/* Key Highlights */}
                    {analysis.personalized_content.key_highlights?.length > 0 && (
                      <div className="bg-white border border-blue-100 rounded-2xl p-6 shadow-soft">
                        <h4 className="text-lg font-bold text-blue-700 mb-4 flex items-center gap-2">
                          <Sparkles size={18} />
                          Role-Aligned Highlights
                        </h4>
                        <div className="space-y-3">
                          {analysis.personalized_content.key_highlights.map((highlight, idx) => (
                            <motion.div
                              key={idx}
                              initial={{ opacity: 0, x: -10 }}
                              animate={{ opacity: 1, x: 0 }}
                              transition={{ delay: idx * 0.1 }}
                              className="flex items-start gap-3 bg-blue-50 border border-blue-100 rounded-xl px-4 py-3"
                            >
                              <span className="text-blue-600 mt-1">•</span>
                              <span className="text-sm text-blue-900 leading-relaxed">
                                {highlight}
                              </span>
                            </motion.div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Skills Alignment */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="bg-purple-50 border border-purple-100 rounded-2xl p-5">
                        <h5 className="text-sm font-semibold text-purple-700 uppercase tracking-wide mb-2">
                          Primary Skills
                        </h5>
                        <div className="flex flex-wrap gap-2">
                          {analysis.personalized_content.skills_section?.primary_skills?.map((skill, idx) => (
                            <Badge key={idx} variant="primary" size="lg">
                              {skill}
                            </Badge>
                          ))}
                          {(!analysis.personalized_content.skills_section?.primary_skills ||
                            analysis.personalized_content.skills_section.primary_skills.length === 0) && (
                            <p className="text-sm text-purple-500">No primary skills identified.</p>
                          )}
                        </div>
                      </div>
                      <div className="bg-green-50 border border-green-100 rounded-2xl p-5">
                        <h5 className="text-sm font-semibold text-green-700 uppercase tracking-wide mb-2">
                          Secondary Skills
                        </h5>
                        <div className="flex flex-wrap gap-2">
                          {analysis.personalized_content.skills_section?.secondary_skills?.map((skill, idx) => (
                            <Badge key={idx} variant="success" size="lg">
                              {skill}
                            </Badge>
                          ))}
                          {(!analysis.personalized_content.skills_section?.secondary_skills ||
                            analysis.personalized_content.skills_section.secondary_skills.length === 0) && (
                            <p className="text-sm text-green-600">No secondary skills listed.</p>
                          )}
                        </div>
                      </div>
                      <div className="bg-blue-50 border border-blue-100 rounded-2xl p-5">
                        <h5 className="text-sm font-semibold text-blue-700 uppercase tracking-wide mb-2">
                          Tooling & Platforms
                        </h5>
                        <div className="flex flex-wrap gap-2">
                          {analysis.personalized_content.skills_section?.tooling?.map((tool, idx) => (
                            <Badge key={idx} variant="info" size="lg">
                              {tool}
                            </Badge>
                          ))}
                          {(!analysis.personalized_content.skills_section?.tooling ||
                            analysis.personalized_content.skills_section.tooling.length === 0) && (
                            <p className="text-sm text-blue-600">No tooling specified.</p>
                          )}
                        </div>
                      </div>
                    </div>

                    {/* Experience Section */}
                    {analysis.personalized_content.experience_section?.length > 0 && (
                      <div className="space-y-4">
                        <h4 className="text-lg font-bold text-gray-900">Experience Tailored for {drive.job_title}</h4>
                        <div className="grid grid-cols-1 gap-4">
                          {analysis.personalized_content.experience_section.map((exp, idx) => (
                            <ModernCard key={idx} className="border border-gray-200">
                              <div className="flex flex-col gap-2">
                                <div className="flex flex-wrap justify-between gap-2">
                                  <div>
                                    <p className="text-lg font-semibold text-gray-900">
                                      {exp.title || 'Experience'}
                                    </p>
                                    <p className="text-sm text-blue-600 font-medium">
                                      {exp.company}
                                    </p>
                                  </div>
                                  {exp.duration && (
                                    <span className="text-sm font-medium text-gray-500">
                                      {exp.duration}
                                    </span>
                                  )}
                                </div>
                                <ul className="list-disc list-inside space-y-2 text-sm text-gray-700">
                                  {exp.impact_bullets?.map((bullet, bIdx) => (
                                    <li key={bIdx}>{bullet}</li>
                                  ))}
                                </ul>
                                {exp.tech_stack?.length > 0 && (
                                  <div className="flex flex-wrap gap-2 mt-2">
                                    {exp.tech_stack.map((tech, tIdx) => (
                                      <Badge key={tIdx} variant="outline" size="sm">
                                        {tech}
                                      </Badge>
                                    ))}
                                  </div>
                                )}
                              </div>
                            </ModernCard>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Projects */}
                    {analysis.personalized_content.projects_section?.length > 0 && (
                      <div className="space-y-4">
                        <h4 className="text-lg font-bold text-gray-900">Projects to Spotlight</h4>
                        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                          {analysis.personalized_content.projects_section.map((project, idx) => (
                            <ModernCard key={idx} className="border border-purple-100 bg-purple-50/50">
                              <h5 className="text-lg font-semibold text-purple-700">{project.name}</h5>
                              <p className="text-sm text-purple-900 mt-2">{project.description}</p>
                              <ul className="list-disc list-inside mt-3 space-y-1 text-sm text-purple-800">
                                {project.impact_bullets?.map((bullet, bIdx) => (
                                  <li key={bIdx}>{bullet}</li>
                                ))}
                              </ul>
                              {project.tech_stack?.length > 0 && (
                                <div className="flex flex-wrap gap-2 mt-3">
                                  {project.tech_stack.map((tech, tIdx) => (
                                    <Badge key={tIdx} variant="purple" size="sm">
                                      {tech}
                                    </Badge>
                                  ))}
                                </div>
                              )}
                            </ModernCard>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Education & Certifications */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {analysis.personalized_content.education_section?.length > 0 && (
                        <ModernCard className="border border-blue-100">
                          <h4 className="text-lg font-semibold text-blue-700 mb-3">Education Alignment</h4>
                          <div className="space-y-3">
                            {analysis.personalized_content.education_section.map((edu, idx) => (
                              <div key={idx} className="border border-blue-50 rounded-xl p-3 bg-blue-50/40">
                                <p className="font-semibold text-blue-900">{edu.degree}</p>
                                <p className="text-sm text-blue-700">{edu.institution}</p>
                                {edu.year && (
                                  <p className="text-xs text-blue-500 mt-1">Graduated: {edu.year}</p>
                                )}
                                {edu.highlights?.length > 0 && (
                                  <ul className="list-disc list-inside text-xs text-blue-600 mt-2 space-y-1">
                                    {edu.highlights.map((highlight, hIdx) => (
                                      <li key={hIdx}>{highlight}</li>
                                    ))}
                                  </ul>
                                )}
                              </div>
                            ))}
                          </div>
                        </ModernCard>
                      )}

                      {analysis.personalized_content.certifications?.length > 0 && (
                        <ModernCard className="border border-green-100">
                          <h4 className="text-lg font-semibold text-green-700 mb-3">Certifications</h4>
                          <ul className="space-y-2 text-sm text-green-900">
                            {analysis.personalized_content.certifications.map((cert, idx) => (
                              <li key={idx} className="flex items-center gap-2">
                                <Check size={16} className="text-green-600" />
                                {cert}
                              </li>
                            ))}
                          </ul>
                        </ModernCard>
                      )}
                    </div>

                    {/* Tailoring Notes */}
                    {(analysis.personalized_content.tailoring_notes?.culture_fit?.length > 0 ||
                      analysis.personalized_content.tailoring_notes?.interview_talking_points?.length > 0 ||
                      analysis.personalized_content.tailoring_notes?.ats_keywords?.length > 0) && (
                      <ModernCard className="border border-orange-200 bg-orange-50/60">
                        <h4 className="text-lg font-semibold text-orange-700 mb-3 flex items-center gap-2">
                          <Target size={18} />
                          Tailoring Notes
                        </h4>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                          {analysis.personalized_content.tailoring_notes?.culture_fit?.length > 0 && (
                            <div>
                              <h5 className="text-sm font-semibold text-orange-600 uppercase mb-2">
                                Culture Fit
                              </h5>
                              <ul className="list-disc list-inside space-y-1 text-sm text-orange-700">
                                {analysis.personalized_content.tailoring_notes.culture_fit.map((item, idx) => (
                                  <li key={idx}>{item}</li>
                                ))}
                              </ul>
                            </div>
                          )}
                          {analysis.personalized_content.tailoring_notes?.interview_talking_points?.length > 0 && (
                            <div>
                              <h5 className="text-sm font-semibold text-orange-600 uppercase mb-2">
                                Interview Talking Points
                              </h5>
                              <ul className="list-disc list-inside space-y-1 text-sm text-orange-700">
                                {analysis.personalized_content.tailoring_notes.interview_talking_points.map((item, idx) => (
                                  <li key={idx}>{item}</li>
                                ))}
                              </ul>
                            </div>
                          )}
                          {analysis.personalized_content.tailoring_notes?.ats_keywords?.length > 0 && (
                            <div>
                              <h5 className="text-sm font-semibold text-orange-600 uppercase mb-2">
                                ATS Keywords
                              </h5>
                              <div className="flex flex-wrap gap-2">
                                {analysis.personalized_content.tailoring_notes.ats_keywords.map((keyword, idx) => (
                                  <Badge key={idx} variant="warning" size="sm">
                                    {keyword}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      </ModernCard>
                    )}
                  </>
                )}
              </div>
            )}

            {activeTab === 'company' && (
              <div className="space-y-6">
                {/* Company Overview */}
                <div>
                  <h3 className="text-2xl font-bold mb-3">{drive.company_name}</h3>
                  <p className="text-gray-700 leading-relaxed">
                    {analysis?.company_research?.company_overview}
                  </p>
                </div>

                {/* Company Details */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-blue-50 p-4 rounded-xl">
                    <p className="text-sm text-gray-600 mb-1">Industry</p>
                    <p className="font-bold">{analysis?.company_research?.industry}</p>
                  </div>
                  <div className="bg-purple-50 p-4 rounded-xl">
                    <p className="text-sm text-gray-600 mb-1">Company Size</p>
                    <p className="font-bold">{analysis?.company_research?.company_size}</p>
                  </div>
                </div>

                {/* Culture & Values */}
                <div>
                  <h4 className="font-bold text-lg mb-3">Culture & Values</h4>
                  <div className="flex flex-wrap gap-2">
                    {analysis?.company_research?.culture_values?.map((value, idx) => (
                      <Badge key={idx} variant="purple" size="lg">
                        {value}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Tech Stack */}
                <div>
                  <h4 className="font-bold text-lg mb-3">Tech Stack</h4>
                  <div className="flex flex-wrap gap-2">
                    {analysis?.company_research?.tech_stack?.map((tech, idx) => (
                      <Badge key={idx} variant="primary" size="lg">
                        {tech}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Role Insights */}
                {analysis?.company_research?.role_insights && (
                  <div className="bg-indigo-50 border border-indigo-100 rounded-2xl p-5 space-y-3">
                    <h4 className="text-lg font-bold text-indigo-700">Role Intelligence</h4>
                    <p className="text-sm text-indigo-900">
                      {analysis.company_research.role_insights.role_summary}
                    </p>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div>
                        <h5 className="text-xs font-semibold text-indigo-600 uppercase mb-2">Key Responsibilities</h5>
                        <ul className="list-disc list-inside text-sm text-indigo-800 space-y-1">
                          {analysis.company_research.role_insights.key_responsibilities?.map((item, idx) => (
                            <li key={idx}>{item}</li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <h5 className="text-xs font-semibold text-indigo-600 uppercase mb-2">Success Profile</h5>
                        <ul className="list-disc list-inside text-sm text-indigo-800 space-y-1">
                          {analysis.company_research.role_insights.success_profile?.map((item, idx) => (
                            <li key={idx}>{item}</li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <h5 className="text-xs font-semibold text-indigo-600 uppercase mb-2">Emerging Trends</h5>
                        <ul className="list-disc list-inside text-sm text-indigo-800 space-y-1">
                          {analysis.company_research.role_insights.emerging_trends?.map((item, idx) => (
                            <li key={idx}>{item}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                )}

                {/* Tailoring Recommendations */}
                {analysis?.company_research?.tailoring_recommendations && (
                  <div className="bg-emerald-50 border border-emerald-100 rounded-2xl p-5 space-y-3">
                    <h4 className="text-lg font-bold text-emerald-700">How to Stand Out</h4>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div>
                        <h5 className="text-xs font-semibold text-emerald-600 uppercase mb-2">Resume Focus</h5>
                        <ul className="list-disc list-inside text-sm text-emerald-800 space-y-1">
                          {analysis.company_research.tailoring_recommendations.resume_focus?.map((item, idx) => (
                            <li key={idx}>{item}</li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <h5 className="text-xs font-semibold text-emerald-600 uppercase mb-2">Culture Alignment</h5>
                        <ul className="list-disc list-inside text-sm text-emerald-800 space-y-1">
                          {analysis.company_research.tailoring_recommendations.culture_alignment?.map((item, idx) => (
                            <li key={idx}>{item}</li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <h5 className="text-xs font-semibold text-emerald-600 uppercase mb-2">Projects to Spotlight</h5>
                        <ul className="list-disc list-inside text-sm text-emerald-800 space-y-1">
                          {analysis.company_research.tailoring_recommendations.project_highlights?.map((item, idx) => (
                            <li key={idx}>{item}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                    {analysis.company_research.source_notes?.length > 0 && (
                      <p className="text-xs text-emerald-600">
                        Sources referenced: {analysis.company_research.source_notes.join(', ')}
                      </p>
                    )}
                  </div>
                )}

                {/* Recent News */}
                {analysis?.company_research?.recent_news?.length > 0 && (
                  <div>
                    <h4 className="font-bold text-lg mb-3">Recent News</h4>
                    <div className="space-y-3">
                      {analysis?.company_research?.recent_news?.map((news, idx) => (
                        <div key={idx} className="bg-gray-50 p-4 rounded-xl border-l-4 border-blue-500">
                          <p className="text-gray-700">{news}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Footer Actions */}
          <div className="border-t border-gray-200 p-6 bg-gray-50">
            <div className="flex gap-4">
              <ModernButton
                onClick={onClose}
                variant="ghost"
                className="flex-1"
              >
                Close
              </ModernButton>
              <ModernButton
                onClick={() => onApply(analysis)}
                variant="primary"
                icon={FileText}
                className="flex-1"
              >
                Apply with AI-Enhanced Resume
              </ModernButton>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

export default JobAnalysisModal;
