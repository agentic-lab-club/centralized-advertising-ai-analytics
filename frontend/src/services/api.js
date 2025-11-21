import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API service methods
export const apiService = {
  // Analytics endpoints
  getAnalyticsSummary: () => api.get('/analytics/summary'),
  getChannelStats: () => api.get('/analytics/channels'),
  getROITrend: () => api.get('/analytics/roi-trend'),

  // Campaign endpoints
  getCampaigns: (params = {}) => api.get('/campaigns', { params }),
  getCampaignsByChannel: (channel) => api.get(`/campaigns/channel/${channel}`),

  // Recommendations endpoints
  getLatestRecommendations: () => api.get('/recommendations/latest'),
  generateRecommendations: () => api.post('/recommendations/generate'),

  // Predictions endpoints
  getPredictions: (params = {}) => api.get('/predictions', { params }),
  getLatestPredictions: () => api.get('/predictions/latest'),
  generatePredictions: () => api.post('/predictions/generate'),

  // Alerts endpoints
  getAllAlerts: (params = {}) => api.get('/alerts', { params }),
  getUnreadAlerts: () => api.get('/alerts/unread'),
  markAlertAsRead: (alertId) => api.patch(`/alerts/${alertId}/read`),
  checkAlerts: () => api.post('/alerts/check'),

  // Dashboard endpoints (if you implement ML dashboard images)
  getROIChart: () => api.get('/dashboards/roi-chart', { responseType: 'blob' }),
  getConversionChart: () => api.get('/dashboards/conversion-chart', { responseType: 'blob' }),

  // Health check
  healthCheck: () => api.get('/health'),
};

export default apiService;
