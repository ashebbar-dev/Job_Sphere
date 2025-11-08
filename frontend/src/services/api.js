import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth APIs
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getCurrentUser: () => api.get('/auth/me'),
};

// TPO APIs
export const tpoAPI = {
  createCompany: (data) => api.post('/tpo/companies', data),
  getCompanies: () => api.get('/tpo/companies'),
  createDrive: (data) => api.post('/tpo/drives', data),
  getDrives: () => api.get('/tpo/drives'),
  getDriveDetails: (id) => api.get(`/tpo/drives/${id}`),
  getDriveApplications: (id) => api.get(`/tpo/drives/${id}/applications`),
  createRound: (data) => api.post('/tpo/rounds', data),
  updateRoundResults: (id, data) => api.post(`/tpo/rounds/${id}/results`, data),
  selectCandidate: (id) => api.post(`/tpo/applications/${id}/select`),
  uploadOfferLetter: (id, file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post(`/tpo/applications/${id}/offer-letter`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

// HOD APIs
export const hodAPI = {
  getPendingStudents: () => api.get('/hod/students/pending'),
  approveStudent: (id) => api.post(`/hod/students/${id}/approve`),
  updateStudent: (id, data) => api.put(`/hod/students/${id}`, data),
  getStats: () => api.get('/hod/stats'),
  getPlacementReport: () => api.get('/hod/reports/placements'),
};

// Student APIs
export const studentAPI = {
  getProfile: () => api.get('/student/profile'),
  updateProfile: (data) => api.put('/student/profile', data),
  uploadResume: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/student/resume', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  getAvailableDrives: () => api.get('/student/drives/available'),
  getMyApplications: () => api.get('/student/applications'),
  downloadOfferLetter: (id) => api.get(`/student/applications/${id}/offer-letter`, {
    responseType: 'blob',
  }),
};

// AI APIs
export const aiAPI = {
  analyzeJobFit: (driveId) => api.get(`/ai/analyze-job/${driveId}`),
  applyToDrive: (driveId, data) => api.post(`/ai/apply/${driveId}`, data),
  getCompanyResearch: (companyId) => api.get(`/ai/research-company/${companyId}`),
  generateCoverLetter: (driveId) => api.get(`/ai/generate-cover-letter/${driveId}`),
  downloadPersonalizedResume: (driveId) =>
    api.get(`/ai/personalized-resume/${driveId}`, { responseType: 'blob' }),
};

export default api;
